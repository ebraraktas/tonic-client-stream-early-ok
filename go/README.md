# go

## Setup

```shell
mkdir -p src/route_guide
protoc --go_out=src/route_guide --go_opt=paths=source_relative \
--go-grpc_out=src/route_guide --go-grpc_opt=paths=source_relative \
-I ../proto/    ../proto/route_guide.proto
```

## Build

```shell
go build server.go # build server
go build client.go # build client
```

## Run

```shell
./server [-port 5000]
./client [-addr localhost:5000]
```