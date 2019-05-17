REGISTRY=reg.plagiari.sm
PROJECT=elections-classification
ORG=cvcio
PROTO_PATH=$(GOPATH)/src/github.com/cvcio/elections-api/proto
TAG=`cat ./VERSION`

protocols:
		python -m grpc_tools.protoc -I$(PROTO_PATH) --python_out=. --grpc_python_out=. $(PROTO_PATH)/classification.proto

# This included makefile should define the 'custom' target rule which is called here.
include $(INCLUDE_MAKEFILE)

.PHONY: release
release: custom 
