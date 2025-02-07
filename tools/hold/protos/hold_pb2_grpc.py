# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import hold_pb2 as hold__pb2


class HoldStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetInfo = channel.unary_unary(
            "/hold.Hold/GetInfo",
            request_serializer=hold__pb2.GetInfoRequest.SerializeToString,
            response_deserializer=hold__pb2.GetInfoResponse.FromString,
        )
        self.Invoice = channel.unary_unary(
            "/hold.Hold/Invoice",
            request_serializer=hold__pb2.InvoiceRequest.SerializeToString,
            response_deserializer=hold__pb2.InvoiceResponse.FromString,
        )
        self.RoutingHints = channel.unary_unary(
            "/hold.Hold/RoutingHints",
            request_serializer=hold__pb2.RoutingHintsRequest.SerializeToString,
            response_deserializer=hold__pb2.RoutingHintsResponse.FromString,
        )
        self.List = channel.unary_unary(
            "/hold.Hold/List",
            request_serializer=hold__pb2.ListRequest.SerializeToString,
            response_deserializer=hold__pb2.ListResponse.FromString,
        )
        self.Settle = channel.unary_unary(
            "/hold.Hold/Settle",
            request_serializer=hold__pb2.SettleRequest.SerializeToString,
            response_deserializer=hold__pb2.SettleResponse.FromString,
        )
        self.Cancel = channel.unary_unary(
            "/hold.Hold/Cancel",
            request_serializer=hold__pb2.CancelRequest.SerializeToString,
            response_deserializer=hold__pb2.CancelResponse.FromString,
        )
        self.Track = channel.unary_stream(
            "/hold.Hold/Track",
            request_serializer=hold__pb2.TrackRequest.SerializeToString,
            response_deserializer=hold__pb2.TrackResponse.FromString,
        )
        self.TrackAll = channel.unary_stream(
            "/hold.Hold/TrackAll",
            request_serializer=hold__pb2.TrackAllRequest.SerializeToString,
            response_deserializer=hold__pb2.TrackAllResponse.FromString,
        )
        self.PayStatus = channel.unary_unary(
            "/hold.Hold/PayStatus",
            request_serializer=hold__pb2.PayStatusRequest.SerializeToString,
            response_deserializer=hold__pb2.PayStatusResponse.FromString,
        )
        self.GetRoute = channel.unary_unary(
            "/hold.Hold/GetRoute",
            request_serializer=hold__pb2.GetRouteRequest.SerializeToString,
            response_deserializer=hold__pb2.GetRouteResponse.FromString,
        )


class HoldServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Invoice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def RoutingHints(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def List(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Settle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Cancel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Track(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def TrackAll(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def PayStatus(self, request, context):
        """Workaround to expose the paystatus command via gRPC, since CLN doesn't"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetRoute(self, request, context):
        """Custom algorithm that allows specifying a max delay"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_HoldServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetInfo": grpc.unary_unary_rpc_method_handler(
            servicer.GetInfo,
            request_deserializer=hold__pb2.GetInfoRequest.FromString,
            response_serializer=hold__pb2.GetInfoResponse.SerializeToString,
        ),
        "Invoice": grpc.unary_unary_rpc_method_handler(
            servicer.Invoice,
            request_deserializer=hold__pb2.InvoiceRequest.FromString,
            response_serializer=hold__pb2.InvoiceResponse.SerializeToString,
        ),
        "RoutingHints": grpc.unary_unary_rpc_method_handler(
            servicer.RoutingHints,
            request_deserializer=hold__pb2.RoutingHintsRequest.FromString,
            response_serializer=hold__pb2.RoutingHintsResponse.SerializeToString,
        ),
        "List": grpc.unary_unary_rpc_method_handler(
            servicer.List,
            request_deserializer=hold__pb2.ListRequest.FromString,
            response_serializer=hold__pb2.ListResponse.SerializeToString,
        ),
        "Settle": grpc.unary_unary_rpc_method_handler(
            servicer.Settle,
            request_deserializer=hold__pb2.SettleRequest.FromString,
            response_serializer=hold__pb2.SettleResponse.SerializeToString,
        ),
        "Cancel": grpc.unary_unary_rpc_method_handler(
            servicer.Cancel,
            request_deserializer=hold__pb2.CancelRequest.FromString,
            response_serializer=hold__pb2.CancelResponse.SerializeToString,
        ),
        "Track": grpc.unary_stream_rpc_method_handler(
            servicer.Track,
            request_deserializer=hold__pb2.TrackRequest.FromString,
            response_serializer=hold__pb2.TrackResponse.SerializeToString,
        ),
        "TrackAll": grpc.unary_stream_rpc_method_handler(
            servicer.TrackAll,
            request_deserializer=hold__pb2.TrackAllRequest.FromString,
            response_serializer=hold__pb2.TrackAllResponse.SerializeToString,
        ),
        "PayStatus": grpc.unary_unary_rpc_method_handler(
            servicer.PayStatus,
            request_deserializer=hold__pb2.PayStatusRequest.FromString,
            response_serializer=hold__pb2.PayStatusResponse.SerializeToString,
        ),
        "GetRoute": grpc.unary_unary_rpc_method_handler(
            servicer.GetRoute,
            request_deserializer=hold__pb2.GetRouteRequest.FromString,
            response_serializer=hold__pb2.GetRouteResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "hold.Hold", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Hold(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetInfo(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hold.Hold/GetInfo",
            hold__pb2.GetInfoRequest.SerializeToString,
            hold__pb2.GetInfoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Invoice(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hold.Hold/Invoice",
            hold__pb2.InvoiceRequest.SerializeToString,
            hold__pb2.InvoiceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def RoutingHints(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hold.Hold/RoutingHints",
            hold__pb2.RoutingHintsRequest.SerializeToString,
            hold__pb2.RoutingHintsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def List(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hold.Hold/List",
            hold__pb2.ListRequest.SerializeToString,
            hold__pb2.ListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Settle(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hold.Hold/Settle",
            hold__pb2.SettleRequest.SerializeToString,
            hold__pb2.SettleResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Cancel(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hold.Hold/Cancel",
            hold__pb2.CancelRequest.SerializeToString,
            hold__pb2.CancelResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Track(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/hold.Hold/Track",
            hold__pb2.TrackRequest.SerializeToString,
            hold__pb2.TrackResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def TrackAll(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/hold.Hold/TrackAll",
            hold__pb2.TrackAllRequest.SerializeToString,
            hold__pb2.TrackAllResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def PayStatus(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hold.Hold/PayStatus",
            hold__pb2.PayStatusRequest.SerializeToString,
            hold__pb2.PayStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetRoute(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hold.Hold/GetRoute",
            hold__pb2.GetRouteRequest.SerializeToString,
            hold__pb2.GetRouteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
