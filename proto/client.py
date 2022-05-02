import random
import sys
import time

import grpc

import route_guide_pb2
import route_guide_pb2_grpc


def random_point():
    latitude = (random.randint(0, 180) - 90) * 10_000_000
    longitude = (random.randint(0, 360) - 180) * 10_000_000
    return route_guide_pb2.Point(latitude=latitude, longitude=longitude)


def call_stream(client: route_guide_pb2_grpc.RouteGuideStub):
    point_count = 5
    points = [random_point() for _ in range(point_count)]
    early_return_index = random.randint(0, len(points) - 2)
    points[early_return_index].latitude = 0
    print(f"{early_return_index = }")

    def iter_points():
        for p in points:
            yield p
            print(f"Sleep 500 ms")
            time.sleep(0.5)

    # Async
    # future = client.RecordRoute.future(iter_points())
    # print(future.result())

    # Sync
    print(client.RecordRoute(iter_points()))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"{port = }")
    channel = grpc.insecure_channel(f"localhost:{port}")
    client = route_guide_pb2_grpc.RouteGuideStub(channel)
    call_stream(client)


if __name__ == '__main__':
    main()
