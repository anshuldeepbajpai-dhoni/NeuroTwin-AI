from unittest.mock import patch

from app.middleware.request_logging import (
    RequestLoggingMiddleware,
)


def test_response_contains_process_time(
    client,
):
    """
    Verify that API responses contain
    request-processing duration.
    """

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    process_time = (
        response.headers.get(
            "X-Process-Time-MS"
        )
    )

    assert (
        process_time is not None
    )

    duration_ms = float(
        process_time
    )

    assert (
        duration_ms >= 0
    )


def test_process_time_uses_two_decimals(
    client,
):
    """
    Verify that process duration uses
    a consistent two-decimal format.
    """

    response = client.get(
        "/health"
    )

    process_time = (
        response.headers[
            "X-Process-Time-MS"
        ]
    )

    whole_part, decimal_part = (
        process_time.split(
            "."
        )
    )

    assert (
        whole_part.isdigit()
    )

    assert (
        decimal_part.isdigit()
    )

    assert (
        len(
            decimal_part
        )
        == 2
    )


def test_request_id_and_process_time_exist(
    client,
):
    """
    Verify that request tracing and
    performance headers coexist.
    """

    response = client.get(
        "/health/liveness"
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        "X-Request-ID"
        in response.headers
    )

    assert (
        "X-Process-Time-MS"
        in response.headers
    )


@patch(
    "app.middleware.request_logging."
    "logger.warning"
)
def test_slow_request_generates_warning(
    mock_warning,
    client,
    monkeypatch,
):
    """
    Verify that requests exceeding the
    configured threshold generate a
    warning log.
    """

    monkeypatch.setattr(
        RequestLoggingMiddleware,
        "SLOW_REQUEST_THRESHOLD_MS",
        0.0,
    )

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    mock_warning.assert_called_once()

    warning_message = (
        mock_warning
        .call_args
        .args[0]
    )

    assert (
        "Slow request detected"
        in warning_message
    )


@patch(
    "app.middleware.request_logging."
    "logger.warning"
)
def test_fast_request_does_not_generate_warning(
    mock_warning,
    client,
    monkeypatch,
):
    """
    Verify that a request below a high
    threshold does not generate a slow
    request warning.
    """

    monkeypatch.setattr(
        RequestLoggingMiddleware,
        "SLOW_REQUEST_THRESHOLD_MS",
        999999.0,
    )

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    mock_warning.assert_not_called()