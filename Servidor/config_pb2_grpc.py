# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import config_pb2 as config__pb2


class ReclamosServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetReclamoById = channel.unary_unary(
                '/reclamos.ReclamosService/GetReclamoById',
                request_serializer=config__pb2.ReclamoRequest.SerializeToString,
                response_deserializer=config__pb2.ReclamoResponse.FromString,
                )


class ReclamosServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetReclamoById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReclamosServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetReclamoById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReclamoById,
                    request_deserializer=config__pb2.ReclamoRequest.FromString,
                    response_serializer=config__pb2.ReclamoResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'reclamos.ReclamosService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


class ReclamosService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetReclamoById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/reclamos.ReclamosService/GetReclamoById',
            config__pb2.ReclamoRequest.SerializeToString,
            config__pb2.ReclamoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
