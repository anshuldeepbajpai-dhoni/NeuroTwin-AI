from uuid import UUID

from app.api.health import (
    router as health_router,
)
from app.core.request_context import (
    get_request_id,
)
from app.middleware.request_logging import (
    RequestLoggingMiddleware,
)


def get_router_paths(
    router,
) -> set[str]:
    """
    Return all endpoint paths registered
    directly in an API router.
    """

    return {
        route.path
        for route in router.routes
    }

def test_health_observability_routes_exist():
    """
    Verify that health, liveness, and
    readiness routes are configured.
    """

    health_paths = (
        get_router_paths(
            health_router
        )
    )

    assert (
        "/health"
        in health_paths
    )

    assert (
        "/health/liveness"
        in health_paths
    )

    assert (
        "/health/readiness"
        in health_paths
    )


def test_health_endpoint_has_observability_headers(
    client,
):
    """
    Verify that a normal health request
    receives tracing and performance
    headers.
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

    process_time = (
        response.headers.get(
            "X-Process-Time-MS"
        )
    )

    assert request_id is not None

    assert process_time is not None

    UUID(
        request_id
    )

    assert (
        float(
            process_time
        )
        >= 0
    )


def test_liveness_endpoint_is_operational(
    client,
):
    """
    Verify that the liveness endpoint
    reports a healthy application
    process.
    """

    response = client.get(
        "/health/liveness"
    )

    assert (
        response.status_code
        == 200
    )

    assert response.json() == {
        "status": "alive",
    }

    assert (
        "X-Request-ID"
        in response.headers
    )

    assert (
        "X-Process-Time-MS"
        in response.headers
    )


def test_readiness_endpoint_is_operational(
    client,
):
    """
    Verify that the application and
    database are operational.
    """

    response = client.get(
        "/health/readiness"
    )

    assert (
        response.status_code
        == 200
    ), (
        "READINESS CHECK FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )

    response_data = (
        response.json()
    )

    assert (
        response_data["status"]
        == "ready"
    )

    assert (
        response_data["application"]
        == "healthy"
    )

    assert (
        response_data["database"]
        == "connected"
    )


def test_client_trace_id_is_preserved(
    client,
):
    """
    Verify end-to-end preservation of a
    client-provided request ID.
    """

    trace_id = (
        "neurotwin-operational-"
        "audit-001"
    )

    response = client.get(
        "/health",
        headers={
            "X-Request-ID": (
                trace_id
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
        == trace_id
    )


def test_generated_request_ids_are_unique(
    client,
):
    """
    Verify that separate requests
    receive independent trace IDs.
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


def test_request_context_is_isolated(
    client,
):
    """
    Verify that request context is
    cleared after request completion.
    """

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        get_request_id()
        is None
    )


def test_performance_configuration_is_valid():
    """
    Verify that slow-request monitoring
    uses a valid positive threshold.
    """

    threshold = (
        RequestLoggingMiddleware
        .SLOW_REQUEST_THRESHOLD_MS
    )

    assert isinstance(
        threshold,
        (
            int,
            float,
        ),
    )

    assert (
        threshold > 0
    )


def test_observability_stack_is_release_ready(
    client,
):
    """
    Perform a final operational smoke
    test of the observability stack.
    """

    endpoints = [
        "/health",
        "/health/liveness",
        "/health/readiness",
    ]

    for endpoint in endpoints:

        response = client.get(
            endpoint
        )

        assert (
            response.status_code
            == 200
        ), (
            "OPERATIONAL ENDPOINT "
            f"FAILED: {endpoint} | "
            f"{response.status_code} | "
            f"{response.json()}"
        )

        assert (
            response.headers.get(
                "X-Request-ID"
            )
            is not None
        )

        process_time = (
            response.headers.get(
                "X-Process-Time-MS"
            )
        )

        assert (
            process_time
            is not None
        )

        assert (
            float(
                process_time
            )
            >= 0
        )