from pathlib import Path


BACKEND_DIRECTORY = (
    Path(
        __file__
    )
    .resolve()
    .parents[1]
)

PROJECT_DIRECTORY = (
    BACKEND_DIRECTORY.parent
)


def test_dockerfile_exists():
    """
    Verify that the backend Dockerfile
    exists.
    """

    dockerfile = (
        BACKEND_DIRECTORY
        / "Dockerfile"
    )

    assert (
        dockerfile.exists()
    ), (
        "Backend Dockerfile is missing."
    )


def test_dockerfile_uses_python_311():
    """
    Verify use of the supported Python
    runtime.
    """

    content = (
        BACKEND_DIRECTORY
        .joinpath(
            "Dockerfile"
        )
        .read_text(
            encoding="utf-8"
        )
    )

    assert (
        "FROM python:3.11-slim"
        in content
    )


def test_dockerfile_uses_production_server():
    """
    Verify that Docker uses the startup
    script and that the script starts
    the FastAPI application with Uvicorn.
    """

    dockerfile_content = (
        BACKEND_DIRECTORY
        .joinpath(
            "Dockerfile"
        )
        .read_text(
            encoding="utf-8"
        )
    )

    startup_script_content = (
        BACKEND_DIRECTORY
        .joinpath(
            "start.sh"
        )
        .read_text(
            encoding="utf-8"
        )
    )

    assert (
        "COPY start.sh"
        in dockerfile_content
    )

    assert (
        'CMD ["/app/start.sh"]'
        in dockerfile_content
    )

    assert (
        "uvicorn"
        in startup_script_content
    )

    assert (
        "app.main:app"
        in startup_script_content
    )

    assert (
        "0.0.0.0"
        in startup_script_content
    )


def test_dockerfile_has_healthcheck():
    """
    Verify container health monitoring.
    """

    content = (
        BACKEND_DIRECTORY
        .joinpath(
            "Dockerfile"
        )
        .read_text(
            encoding="utf-8"
        )
    )

    assert (
        "HEALTHCHECK"
        in content
    )

    assert (
        "/health/liveness"
        in content
    )


def test_dockerignore_protects_environment():
    """
    Verify that environment secrets are
    excluded from the Docker context.
    """

    content = (
        BACKEND_DIRECTORY
        .joinpath(
            ".dockerignore"
        )
        .read_text(
            encoding="utf-8"
        )
    )

    assert (
        ".env"
        in content
    )

    assert (
        ".venv/"
        in content
    )

    assert (
        "__pycache__/"
        in content
    )


def test_environment_example_exists():
    """
    Verify deployment environment
    documentation.
    """

    environment_example = (
        BACKEND_DIRECTORY
        / ".env.example"
    )

    assert (
        environment_example.exists()
    )


def test_compose_configuration_exists():
    """
    Verify that Docker Compose
    configuration exists.
    """

    compose_file = (
        PROJECT_DIRECTORY
        / "docker-compose.yml"
    )

    assert (
        compose_file.exists()
    )


def test_compose_contains_required_services():
    """
    Verify backend and PostgreSQL
    service definitions.
    """

    content = (
        PROJECT_DIRECTORY
        .joinpath(
            "docker-compose.yml"
        )
        .read_text(
            encoding="utf-8"
        )
    )

    assert (
        "backend:"
        in content
    )

    assert (
        "db:"
        in content
    )

    assert (
        "postgres:16-alpine"
        in content
    )

    assert (
        "service_healthy"
        in content
    )