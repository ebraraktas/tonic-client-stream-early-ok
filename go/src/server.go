/*
 *
 * Copyright 2015 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

// Package main implements a simple gRPC server that demonstrates how to use gRPC-Go libraries
// to perform client streaming RPCs.
//
// It implements the route guide service whose definition can be found in ../proto/route_guide.proto.
package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"google.golang.org/grpc"

	pb "gorouteguide/src/route_guide"
)

var (
	port = flag.Int("port", 50051, "The server port")
)

type routeGuideServer struct {
	pb.UnimplementedRouteGuideServer
}

// RecordRoute records a route composited of a sequence of points.
//
// It gets a stream of points, and responds with statistics about the "trip":
// number of points,  number of known features visited, total distance traveled, and
// total time spent.
func (s *routeGuideServer) RecordRoute(stream pb.RouteGuide_RecordRouteServer) error {
	var pointCount int32
	for {
		point, err := stream.Recv()
		if err == io.EOF {
			return stream.SendAndClose(&pb.RouteSummary{
				PointCount:   pointCount,
			})
		}
		if err != nil {
			return err
		}
		pointCount++
		if point.Latitude == 0 {
			log.Println("Return early: ", pointCount)
			return stream.SendAndClose(&pb.RouteSummary{
				PointCount:   pointCount,
			})
		}
	}
}

func serialize(point *pb.Point) string {
	return fmt.Sprintf("%d %d", point.Latitude, point.Longitude)
}

func newServer() *routeGuideServer {
	s := &routeGuideServer{}
	return s
}

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)
	pb.RegisterRouteGuideServer(grpcServer, newServer())
	grpcServer.Serve(lis)
}
