import typing
from concurrent import futures

import grpc

import route_guide_pb2
import route_guide_pb2_grpc


class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    def RecordRoute(self, request_iterator: typing.Iterator[route_guide_pb2.Point],
                    context: grpc.ServicerContext) -> route_guide_pb2.RouteSummary:
        summary = route_guide_pb2.RouteSummary()
        for point in request_iterator:
            summary.point_count += 1
            if point.latitude == 0:
                print(f"Return early: {summary.point_count}")
                return summary
        print(f"Return normal: {summary}")
        return summary


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
