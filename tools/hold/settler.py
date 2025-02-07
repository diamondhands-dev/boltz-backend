from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar

from invoice import HoldInvoice, InvoiceState
from pyln.client.plugin import Request
from tracker import Tracker
from utils import partition, time_now


class HtlcFailureMessage(str, Enum):
    MppTimeout = "0017"
    IncorrectPaymentDetails = "400F"


@dataclass
class Htlc:
    msat: int
    request: Request
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        self_without_request = {
            k: v for k, v in self.__dict__.items() if not isinstance(v, Request)
        }
        return {
            k: int(v.timestamp()) if isinstance(v, datetime) else v
            for k, v in self_without_request.items()
        }


# TODO: save information about HTLCs
class Htlcs:
    htlcs: list[Htlc]

    def __init__(self, invoice_amount: int) -> None:
        self.htlcs = []
        self.invoice_amount = invoice_amount

    def add_htlc(self, htlc_msat: int, req: Request) -> None:
        self.htlcs.append(Htlc(htlc_msat, req, time_now()))

    def is_fully_paid(self) -> bool:
        return self.invoice_amount <= sum(h.msat for h in self.htlcs)

    def requests(self) -> list[Request]:
        return [h.request for h in self.htlcs]

    def cancel_expired(self, expiry: int) -> None:
        expired, not_expired = partition(
            self.htlcs,
            lambda htlc: (time_now() - htlc.created_at).total_seconds() > expiry,
        )

        self.htlcs = not_expired
        for h in expired:
            Settler.fail_callback(h.request, HtlcFailureMessage.MppTimeout)


class Settler:
    htlcs: ClassVar[dict[str, Htlcs]] = {}

    def __init__(self, tracker: Tracker) -> None:
        self._tracker = tracker

    def settle(self, invoice: HoldInvoice) -> None:
        invoice.set_state(self._tracker, InvoiceState.Paid)
        for req in self._pop_requests(invoice.payment_hash):
            self.settle_callback(req, invoice.payment_preimage)

    def cancel(self, invoice: HoldInvoice) -> None:
        invoice.set_state(self._tracker, InvoiceState.Cancelled)
        for req in self._pop_requests(invoice.payment_hash):
            self.fail_callback(req, HtlcFailureMessage.IncorrectPaymentDetails)

    def _pop_requests(self, payment_hash: str) -> list[Request]:
        return self.htlcs.pop(payment_hash, Htlcs(0)).requests()

    @staticmethod
    def fail_callback(req: Request, message: HtlcFailureMessage) -> None:
        req.set_result(
            {
                "result": "fail",
                "failure_message": message,
            }
        )

    @staticmethod
    def continue_callback(req: Request) -> None:
        req.set_result(
            {
                "result": "continue",
            }
        )

    @staticmethod
    def settle_callback(req: Request, preimage: str) -> None:
        req.set_result(
            {
                "result": "resolve",
                "payment_key": preimage,
            }
        )
