from unittest.mock import patch


def test_application_health(
    client,
):
    """
    Verify the basic application
    health endpoint.
    """

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    assert response.json() == {
        "status": "healthy",
        "application": "running",
    }


def test_application_liveness(
    client,
):
    """
    Verify the application liveness
    endpoint.
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


@patch(
    "app.api.health."
    "health_service."
    "check_database"
)
def test_application_is_ready(
    mock_check_database,
    client,
):
    """
    Verify successful application
    readiness.
    """

    mock_check_database.return_value = (
        True
    )

    response = client.get(
        "/health/readiness"
    )

    assert (
        response.status_code
        == 200
    )

    assert response.json() == {
        "status": "ready",
        "application": "healthy",
        "database": "connected",
    }

    mock_check_database\
        .assert_called_once()


@patch(
    "app.api.health."
    "health_service."
    "check_database"
)
def test_application_is_not_ready(
    mock_check_database,
    client,
):
    """
    Verify database failure returns
    HTTP 503.
    """

    mock_check_database.return_value = (
        False
    )

    response = client.get(
        "/health/readiness"
    )

    assert (
        response.status_code
        == 503
    )

    assert response.json() == {
        "status": "not_ready",
        "application": "healthy",
        "database": "disconnected",
    }

    mock_check_database\
        .assert_called_once()