import fs from 'fs';
import { Arguments } from 'yargs';
import { Networks } from 'boltz-core';
import { generateMnemonic } from 'bip39';
import { Networks as LiquidNetworks } from 'boltz-core/dist/lib/liquid';
import Api from './api/Api';
import Logger from './Logger';
import { setup } from './Core';
import Database from './db/Database';
import Prometheus from './Prometheus';
import Service from './service/Service';
import VersionCheck from './VersionCheck';
import GrpcServer from './grpc/GrpcServer';
import NodeSwitch from './swap/NodeSwitch';
import ChainTip from './db/models/ChainTip';
import GrpcService from './grpc/GrpcService';
import ClnClient from './lightning/ClnClient';
import LndClient from './lightning/LndClient';
import ChainClient from './chain/ChainClient';
import Config, { ConfigType } from './Config';
import { CurrencyType } from './consts/Enums';
import { formatError, getVersion } from './Utils';
import ElementsClient from './chain/ElementsClient';
import { registerExitHandler } from './ExitHandler';
import BackupScheduler from './backup/BackupScheduler';
import { LightningClient } from './lightning/LightningClient';
import EthereumManager from './wallet/ethereum/EthereumManager';
import WalletManager, { Currency } from './wallet/WalletManager';
import ChainTipRepository from './db/repositories/ChainTipRepository';
import NotificationProvider from './notifications/NotificationProvider';

class Boltz {
  private readonly logger: Logger;
  private readonly config: ConfigType;

  private readonly service!: Service;
  private readonly backup: BackupScheduler;
  private readonly walletManager: WalletManager;

  private readonly currencies: Map<string, Currency>;

  private db: Database;
  private notifications!: NotificationProvider;

  private api!: Api;
  private readonly prometheus: Prometheus;
  private grpcServer!: GrpcServer;

  private readonly ethereumManager?: EthereumManager;

  constructor(config: Arguments<any>) {
    this.config = new Config().load(config);
    this.logger = new Logger(
      this.config.loglevel,
      this.config.logpath,
      this.config.lokiHost,
      this.config.lokiNetwork,
    );

    this.logger.info(`Starting Boltz ${getVersion()}`);

    registerExitHandler(async () => {
      await this.db.close();
      await this.logger.close();
    });

    process.on('unhandledRejection', (reason, promise) => {
      console.log(promise);
      this.logger.error(`Unhandled rejection: ${formatError(reason)}`);
    });

    process.on('uncaughtException', (error) => {
      this.logger.error(`Uncaught exception: ${formatError(error)}`);
    });

    process.on('exit', (code) => {
      (code === 0 ? this.logger.debug : this.logger.error)(
        `Application shutting down with code: ${code}`,
      );
    });

    this.db = new Database(this.logger, this.config.dbpath);

    try {
      this.ethereumManager = new EthereumManager(
        this.logger,
        this.config.ethereum,
      );
    } catch (error) {
      this.logger.warn(
        `Disabled Ethereum integration because: ${formatError(error)}`,
      );
    }

    this.currencies = this.parseCurrencies();

    const walletCurrencies = Array.from(this.currencies.values());

    if (fs.existsSync(this.config.mnemonicpath)) {
      this.walletManager = new WalletManager(
        this.logger,
        this.config.mnemonicpath,
        walletCurrencies,
        this.ethereumManager,
      );
    } else {
      const mnemonic = generateMnemonic();
      this.logger.info(`Generated new mnemonic: ${mnemonic}`);

      this.walletManager = WalletManager.fromMnemonic(
        this.logger,
        mnemonic,
        this.config.mnemonicpath,
        walletCurrencies,
        this.ethereumManager,
      );
    }

    try {
      this.service = new Service(
        this.logger,
        this.config,
        this.walletManager,
        new NodeSwitch(this.logger, this.config.nodeSwitch),
        this.currencies,
      );

      this.backup = new BackupScheduler(
        this.logger,
        this.config.dbpath,
        this.config.backup,
        this.service.eventHandler,
      );

      this.notifications = new NotificationProvider(
        this.logger,
        this.service,
        this.backup,
        this.config.notification,
        [this.config.liquid].concat(this.config.currencies),
        this.config.ethereum.tokens,
      );

      this.grpcServer = new GrpcServer(
        this.logger,
        this.config.grpc,
        new GrpcService(this.service),
      );

      this.prometheus = new Prometheus(this.logger, this.config.prometheus);

      this.api = new Api(this.logger, this.config.api, this.service);
    } catch (error) {
      this.logger.error(`Could not start Boltz: ${formatError(error)}`);
      // eslint-disable-next-line no-process-exit
      process.exit(1);
    }
  }

  public start = async (): Promise<void> => {
    await setup();

    try {
      await this.db.migrate(this.currencies);
      await this.db.init();
      await this.backup.init();

      await this.prometheus.start();

      // Query the chain tips now to avoid them being updated after the chain clients are initialized
      const chainTips = await ChainTipRepository.getChainTips();

      await Promise.all(
        Array.from(this.currencies.values()).flatMap((currency) => {
          const prms: Promise<void>[] = [];

          if (currency.chainClient) {
            prms.push(this.connectChainClient(currency.chainClient));
          }

          prms.concat(
            [currency.lndClient, currency.clnClient]
              .filter(
                (client): client is ClnClient | LndClient =>
                  client !== undefined,
              )
              .map((client) => this.connectLightningClient(client)),
          );

          return prms;
        }),
      );

      await this.walletManager.init(this.config.currencies);
      await this.service.init(this.config.pairs);

      await this.service.swapManager.init(Array.from(this.currencies.values()));

      await this.notifications.init();

      await this.grpcServer.listen();

      await this.api.init();

      // Rescan chains after everything else was initialized to avoid race conditions
      if (chainTips.length === 0) {
        return;
      }

      this.logger.verbose(
        `Starting rescan of chains: ${chainTips
          .map((chainTip) => chainTip.symbol)
          .join(', ')}`,
      );

      const logRescan = (chainTip: ChainTip) => {
        this.logger.debug(
          `Rescanning ${chainTip.symbol} from height: ${chainTip.height}`,
        );
      };

      const rescanPromises: Promise<void>[] = [];

      for (const chainTip of chainTips) {
        if (chainTip.symbol === 'ETH') {
          if (this.walletManager.ethereumManager) {
            logRescan(chainTip);
            rescanPromises.push(
              this.walletManager.ethereumManager.contractEventHandler.rescan(
                chainTip.height,
              ),
            );
          }
        } else {
          if (!this.currencies.has(chainTip.symbol)) {
            this.logger.warn(
              `Not rescanning ${chainTip.symbol} because no chain client was configured`,
            );
            continue;
          }

          const { chainClient } = this.currencies.get(chainTip.symbol)!;

          if (chainClient) {
            logRescan(chainTip);
            rescanPromises.push(chainClient.rescanChain(chainTip.height));
          }
        }
      }

      await Promise.all(rescanPromises);
      this.logger.verbose('Finished rescanning');
    } catch (error) {
      this.logger.error(`Could not initialize Boltz: ${formatError(error)}`);
      console.log(error);
      // eslint-disable-next-line no-process-exit
      process.exit(1);
    }
  };

  private connectChainClient = async (client: ChainClient) => {
    const service = `${client.symbol} chain`;

    try {
      await client.connect();

      const blockchainInfo = await client.getBlockchainInfo();
      const networkInfo = await client.getNetworkInfo();

      VersionCheck.checkChainClientVersion(client.symbol, networkInfo.version);

      this.logStatus(service, {
        version: networkInfo.version,
        protocolversion: networkInfo.protocolversion,
        connections: networkInfo.connections,
        blocks: blockchainInfo.blocks,
        bestblockhash: blockchainInfo.bestblockhash,
        verificationprogress: blockchainInfo.verificationprogress,
      });
    } catch (error) {
      this.logCouldNotConnect(service, error);
    }
  };

  private connectLightningClient = async (client: LightningClient) => {
    const service = `${client.symbol} ${client.serviceName()}`;

    try {
      await client.connect();

      const info = await client.getInfo();
      VersionCheck.checkLightningVersion(
        client.serviceName(),
        client.symbol,
        info.version,
      );

      if (client instanceof ClnClient) {
        const holdInfo = await client.getHoldInfo();
        this.logger.verbose(
          `${client.symbol} ${ClnClient.serviceNameHold} version: ${holdInfo.version}`,
        );
        VersionCheck.checkLightningVersion(
          ClnClient.serviceNameHold,
          client.symbol,
          holdInfo.version,
        );
      }

      this.logStatus(service, info);
    } catch (error) {
      this.logCouldNotConnect(service, error);
    }
  };

  private parseCurrencies = (): Map<string, Currency> => {
    const result = new Map<string, Currency>();

    this.config.currencies.forEach((currency) => {
      try {
        const chainClient = new ChainClient(
          this.logger,
          currency.chain,
          currency.symbol,
        );

        result.set(currency.symbol, {
          chainClient,
          symbol: currency.symbol,
          type: CurrencyType.BitcoinLike,
          network: Networks[currency.network],
          lndClient:
            currency.lnd !== undefined
              ? new LndClient(this.logger, currency.symbol, currency.lnd)
              : undefined,
          clnClient:
            currency.cln !== undefined
              ? new ClnClient(this.logger, currency.symbol, currency.cln)
              : undefined,
          limits: {
            ...currency,
          },
        });
      } catch (error) {
        this.logger.error(
          `Could not initialize currency ${currency.symbol}: ${
            (error as any).message
          }`,
        );
      }
    });

    this.config.ethereum.tokens.forEach((token) => {
      result.set(token.symbol, {
        symbol: token.symbol,
        type: token.symbol === 'ETH' ? CurrencyType.Ether : CurrencyType.ERC20,
        limits: {
          ...token,
        },
        provider: this.ethereumManager?.provider,
      });
    });

    if (this.config.liquid) {
      const { symbol, chain, network } = this.config.liquid;
      result.set(symbol, {
        type: CurrencyType.Liquid,
        symbol: symbol,
        network: LiquidNetworks[network],
        chainClient: new ElementsClient(this.logger, chain),
        limits: {
          ...this.config.liquid,
        },
      });
    }

    return result;
  };

  private logStatus = (service: string, status: unknown) => {
    this.logger.verbose(
      `${service} status: ${JSON.stringify(status, undefined, 2)}`,
    );
  };

  private logCouldNotConnect = (service: string, error: any) => {
    this.logger.error(`Could not connect to ${service}: ${formatError(error)}`);
  };
}

export default Boltz;
