"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import route_guide_pb2
import typing

class RouteGuideStub:
    """Interface exported by the server."""
    def __init__(self, channel: grpc.Channel) -> None: ...
    RecordRoute: grpc.StreamUnaryMultiCallable[
        route_guide_pb2.Point,
        route_guide_pb2.RouteSummary]
    """A client-to-server streaming RPC.

    Accepts a stream of Points on a route being traversed, returning a
    RouteSummary when traversal is completed.
    """


class RouteGuideServicer(metaclass=abc.ABCMeta):
    """Interface exported by the server."""
    @abc.abstractmethod
    def RecordRoute(self,
        request_iterator: typing.Iterator[route_guide_pb2.Point],
        context: grpc.ServicerContext,
    ) -> route_guide_pb2.RouteSummary:
        """A client-to-server streaming RPC.

        Accepts a stream of Points on a route being traversed, returning a
        RouteSummary when traversal is completed.
        """
        pass


def add_RouteGuideServicer_to_server(servicer: RouteGuideServicer, server: grpc.Server) -> None: ...
