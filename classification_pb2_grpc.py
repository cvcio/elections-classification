# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import classification_pb2 as classification__pb2


class ClassificationStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Classify = channel.unary_unary(
        '/elections.mediawatch.io.Classification/Classify',
        request_serializer=classification__pb2.UserFeatures.SerializeToString,
        response_deserializer=classification__pb2.UserClass.FromString,
        )


class ClassificationServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Classify(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ClassificationServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Classify': grpc.unary_unary_rpc_method_handler(
          servicer.Classify,
          request_deserializer=classification__pb2.UserFeatures.FromString,
          response_serializer=classification__pb2.UserClass.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'elections.mediawatch.io.Classification', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))