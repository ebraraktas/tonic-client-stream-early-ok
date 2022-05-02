# tonic-client-stream-early-ok

Demo code to demonstrate an issue when server returns
early OK to a streaming request.

## Rust

`src/server.rs` implements
very simple and pruned version of well known `routeguide`
service (only client-side streaming endpoint, 
see `proto/route_guide.proto`) in rust using `tonic-rs`.

It takes stream of `Point`s, and returns early if `latitude` 
of a point is `0`.

```shell
cargo run --bin routeguide-server # runs server on localhost:5000
```

`src/client.rs` is a simple binary calling streaming endpoint 
of the service defined in `proto/route_guide.proto`. It generates
random 5 points, and sets `latitude` of a random point to `0`. 
Then, sends those points to a stream with 500 ms interval.

```shell
cargo run --bin routeguide-server -- [PORT]
# default value of the PORT is 5000, if omitted
```

## Python

`proto` directory has python generated code for `proto/route_guide.proto`.
In addition, `proto/server.py` and `proto/client.py` implement 
what `server.rs` and `client.rs` do in python. Both require `grpcio`. 

```shell
# Install dependency if required
pip install grpcio==1.44.0

cd proto
python server.py # runs server on localhost:5001
python client.py [PORT]
# default value of the PORT is 5001, if omitted
```

## Issue

It works OK if I call server in `server.rs` from `client.rs`, or call 
server in `server.py` from `client.py`. However, Python client fails 
if I call server in `server.rs` from `client.py` with the exception below 
(grpcio version `1.44.0`):

```shell
# python client.py 5000
port = 5000
early_return_index = 2
Sleep 500 ms
Sleep 500 ms
Sleep 500 ms
Traceback (most recent call last):
  File "client.py", line 46, in <module>
    main()
  File "client.py", line 42, in main
    call_stream(client)
  File "client.py", line 34, in call_stream
    print(client.RecordRoute(iter_points()))
  File "/usr/local/lib/python3.8/site-packages/grpc/_channel.py", line 1131, in __call__
    return _end_unary_response_blocking(state, call, False, None)
  File "/usr/local/lib/python3.8/site-packages/grpc/_channel.py", line 849, in _end_unary_response_blocking
    raise _InactiveRpcError(state)
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.CANCELLED
        details = "Received RST_STREAM with error code 8"
        debug_error_string = "{"created":"@1651470233.217719000","description":"Error received from peer ipv6:[::1]:5000","file":"src/core/lib/surface/call.cc","file_line":1075,"grpc_message":"Received RST_STREAM with error code 8","grpc_status":1}"
>
```