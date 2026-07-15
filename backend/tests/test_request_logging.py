from uuid import UUID

from app.core.request_context import (
    get_request_id,
)


def test_response_contains_request_id(
    client,
):
    """
    Verify that every response contains
    a valid generated request ID.
    """

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    request_id = (
        response.headers.get(
            "X-Request-ID"
        )
    )

    assert request_id is not None

    UUID(
        request_id
    )


def test_client_request_id_is_preserved(
    client,
):
    """
    Verify that a client-provided
    request ID is returned unchanged.
    """

    custom_request_id = (
        "neurotwin-test-request-001"
    )

    response = client.get(
        "/health",
        headers={
            "X-Request-ID": (
                custom_request_id
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        response.headers[
            "X-Request-ID"
        ]
        == custom_request_id
    )


def test_different_requests_receive_different_ids(
    client,
):
    """
    Verify that independent requests
    receive different generated IDs.
    """

    first_response = client.get(
        "/health"
    )

    second_response = client.get(
        "/health"
    )

    first_request_id = (
        first_response.headers[
            "X-Request-ID"
        ]
    )

    second_request_id = (
        second_response.headers[
            "X-Request-ID"
        ]
    )

    assert (
        first_request_id
        != second_request_id
    )


def test_request_context_is_empty_outside_request():
    """
    Verify that request context does not
    leak after request processing.
    """

    assert (
        get_request_id()
        is None
    )