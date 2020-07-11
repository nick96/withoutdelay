"""GRPC server for temporal service."""

from concurrent import futures
import logging
import re
from datetime import datetime

import grpc

from temporal import temporal_service_pb2
from temporal import temporal_service_pb2_grpc
from temporal.timex import tag, ground


class TemporalServiceServicer(temporal_service_pb2_grpc.TemporalServiceServicer):
    """Implementation of GRPC service methods."""

    def TagTimex(self, request, context):
        tagged = tag(request.text)
        timex_matches = re.finditer(r"<TIMEX2>(.+)<\/TIMEX2>", tagged)
        for timex_match in timex_matches:
            timex = timex_match.group(1)
            pos = timex_match.pos
            yield temporal_service_pb2.TimexTag(
                timex=timex, pos=pos,
            )

    def TimexToAbsolute(self, request, context):
        logger = logging.getLogger("timex_to_abs")

        base_time = datetime.now()
        ground = ground(tagged, base_time)
        
        match = re.match(r"<TIMEX2 val=(.+)>(.+)<\/TIMEX2>")

        logger.info(f"Grounded time: {match.group(1)}")
        logger.info(f"Timex: {match.group(2)}")

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

