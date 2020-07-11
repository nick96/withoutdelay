GATEWAY_FLAGS := -I/usr/local/include -Iprotos/third_party/googleapis -Iprotos

GRPC_FLAGS := --python_out=temporal --grpc_python_out=temporal

code:
	poetry run python -m grpc_tools.protoc $(GRPC_FLAGS) $(GATEWAY_FLAGS) protos/*.proto

gw-protos:
	mkdir -p ./gateway/gen/go
	protoc $(GATEWAY_FLAGS) --go_out=plugins=grpc,paths=source_relative:./gateway/gen/go/ protos/*.proto
	protoc $(GATEWAY_FLAGS) --grpc-gateway_out=logtostderr=true,paths=source_relative:./gateway/gen/go protos/*.proto
	protoc $(GATEWAY_FLAGS) --swagger_out=logtostderr=true:./gateway/gen/go protos/*.proto

gw: gw-protos
	cd ./gateway && go build
