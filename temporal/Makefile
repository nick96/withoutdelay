GATEWAY_FLAGS := -I/usr/local/include -Iprotos/third_party/googleapis -Iprotos

GRPC_FLAGS := --python_out=temporal --grpc_python_out=temporal

lint:
	poetry run black --version
	poetry run black --check .
	poetry run mypy --version
	poetry run mypy temporal

test:
	poetry run pytest

server-protos:
	poetry run python -m grpc_tools.protoc $(GRPC_FLAGS) $(GATEWAY_FLAGS) protos/*.proto

gw-protos:
	docker build -t protoc-builder --target builder -f Dockerfile.gateway .
	mkdir -p ./gateway/gen/go
	docker run -v $(PWD):/gw -it protoc-builder $(GATEWAY_FLAGS) --go_out=plugins=grpc,paths=source_relative:./gateway/gen/go/ protos/*.proto
	docker run -v $(PWD):/gw -it protoc-builder $(GATEWAY_FLAGS) --grpc-gateway_out=logtostderr=true,paths=source_relative:./gateway/gen/go protos/*.proto
	docker run -v $(PWD):/gw -it protoc-builder $(GATEWAY_FLAGS) --swagger_out=logtostderr=true:./gateway/gen/go protos/*.proto

gw-protos-no-docker:
	mkdir -p ./gateway/gen/go
	protoc $(GATEWAY_FLAGS) --go_out=plugins=grpc,paths=source_relative:./gateway/gen/go/ protos/*.proto
	protoc $(GATEWAY_FLAGS) --grpc-gateway_out=logtostderr=true,paths=source_relative:./gateway/gen/go protos/*.proto
	protoc $(GATEWAY_FLAGS) --swagger_out=logtostderr=true:./gateway/gen/go protos/*.proto

gw: gw-protos
	cd ./gateway && go build

gw-no-docker: gw-protos-no-docker
	cd ./gateway && go build


protos: server-protos gw-protos


