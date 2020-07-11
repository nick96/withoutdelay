GATEWAY_FLAGS := -I/usr/local/include -I. -I$(GOPATH)/src -I$(GOPATH)/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis

GRPC_FLAGS := --python_out=temporal --grpc_python_out=temporal

code:
	python -m grpc_tools.protoc $(GRPC_FLAGS) $(GATEWAY_FLAGS) *.proto

gw-protos:
	mkdir -p ./gateway/gen/go
	protoc $(GATEWAY_FLAGS) --go_out=plugins=grpc,paths=source_relative:./gateway/gen/go/ *.proto
	protoc $(GATEWAY_FLAGS) --grpc-gateway_out=logtostderr=true,paths=source_relative:./gateway/gen/go *.proto

gw: gw-protos
	cd ./gateway && go build
