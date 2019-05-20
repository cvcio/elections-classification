REGISTRY=reg.plagiari.sm
PROJECT=elections-classification
ORG=cvcio
PROTO_PATH=$(GOPATH)/src/github.com/cvcio/elections-api/proto
TAG=`cat ./VERSION`

REG_PROJ=$(REGISTRY)/$(PROJECT)
REG_TAG=$(REGISTRY)/$(PROJECT):$(TAG)

protocols:
		python -m grpc_tools.protoc -I$(PROTO_PATH) --python_out=. --grpc_python_out=. $(PROTO_PATH)/classification.proto

docker:
	echo ${GITHUB_TOKEN}
	docker build -t $(REG_TAG) .

docker-latest: docker
	docker tag $(REG_TAG) $(REG_PROJ):latest

docker-push:
	docker push $(REG_TAG)

docker-push-latest:
	docker push $(REG_PROJ):latest

# This included makefile should define the 'custom' target rule which is called here.
include $(INCLUDE_MAKEFILE)

.PHONY: release
release: custom
