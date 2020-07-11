"""GRPC server for temporal service."""

from concurrent import futures
import logging

import grpc

from temporal import temporal_service_pb2
from temporal import temporal_service_pb2_grpc


class TemporalServiceServicer(temporal_service_pb2_grpc.TemporalServiceServicer):
    """Implementation of GRPC service methods."""

    def TagTimex(self, request, context):
        yield temporal_service_pb2.TimexTag(
            timex="", pos=0,
        )

    def TimexToAbsolute(self, request, context):
        return temporal_service_pb2.TimexToAbsoluteResponse(
            input=request.timex, absoluteDateTime=0,
        )


def serve():
    logger = logging.getLogger("temporal")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    temporal_service_pb2_grpc.add_TemporalServiceServicer_to_server(
        TemporalServiceServicer(), server
    )
    port = "8000"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"Started on port {port}")
    server.wait_for_termination()

