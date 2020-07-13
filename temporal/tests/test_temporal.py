from typing import List, Any
from datetime import datetime, timedelta

import pytest
import grpc_testing

from temporal import __version__
from temporal import temporal_service_pb2
from temporal.server import TemporalServiceServicer

BASE_TIME = datetime.now()


def to_start_of_day(dt: datetime) -> datetime:
    date = dt.date()
    return datetime.combine(date, datetime.min.time())


@pytest.fixture(scope="module")
def server():
    servicers = {
        temporal_service_pb2.DESCRIPTOR.services_by_name[
            "TemporalService"
        ]: TemporalServiceServicer()
    }
    return grpc_testing.server_from_dictionary(
        servicers, grpc_testing.strict_real_time()
    )


def test_version():
    assert __version__ == "0.0.1"


def take_all_responses(method: grpc_testing.UnaryStreamServerRpc) -> List[Any]:
    responses = []
    try:
        while True:
            response = method.take_response()
            responses.append(response)
    except ValueError:
        return responses


@pytest.mark.parametrize(
    ("text", "expected_tags"),
    (
        (
            "yesterday I went to the shops",
            [temporal_service_pb2.TimexTag(timex="yesterday", pos=0,)],
        ),
    ),
)
def test_tag_timex(text, expected_tags, server):
    request = temporal_service_pb2.TagTimexRequest(text=text)
    method = server.invoke_unary_stream(
        method_descriptor=(
            temporal_service_pb2.DESCRIPTOR.services_by_name[
                "TemporalService"
            ].methods_by_name["TagTimex"]
        ),
        invocation_metadata={},
        request=request,
        timeout=1,
    )
    metadata, status_code, details = method.termination()

    assert status_code.value == (0, "ok"), details

    actual_tags = take_all_responses(method)
    assert actual_tags == expected_tags


@pytest.mark.parametrize(
    ("timex", "tag"),
    (
        (
            "yesterday",
            temporal_service_pb2.TimexToAbsoluteResponse(
                input="yesterday",
                absoluteDateTime=int(
                    to_start_of_day(BASE_TIME - timedelta(days=1)).timestamp()
                ),
            ),
        ),
    ),
)
def test_timex_to_absolute_time(timex, tag, server):
    request = temporal_service_pb2.TimexToAbsoluteRequest(
        timex=timex, baseTime=int(BASE_TIME.timestamp())
    )
    method = server.invoke_unary_unary(
        method_descriptor=temporal_service_pb2.DESCRIPTOR.services_by_name[
            "TemporalService"
        ].methods_by_name["TimexToAbsolute"],
        invocation_metadata={},
        request=request,
        timeout=1,
    )
    response, metadata, status_code, details = method.termination()
    assert status_code.value == (0, "ok"), details
    assert response == tag
