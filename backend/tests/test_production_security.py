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


def test_security_headers_exist(
    client,
):
    """
    Verify defensive HTTP headers.
    """

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        response.headers[
            "X-Content-Type-Options"
        ]
        == "nosniff"
    )

    assert (
        response.headers[
            "X-Frame-Options"
        ]
        == "DENY"
    )

    assert (
        response.headers[
            "Referrer-Policy"
        ]
        == (
            "strict-origin-"
            "when-cross-origin"
        )
    )

    assert (
        response.headers[
            "Permissions-Policy"
        ]
        == (
            "camera=(), "
            "microphone=(), "
            "geolocation=()"
        )
    )


def test_observability_headers_remain(
    client,
):
    """
    Verify security middleware does not
    remove observability headers.
    """

    response = client.get(
        "/health"
    )

    assert (
        "X-Request-ID"
        in response.headers
    )

    assert (
        "X-Process-Time-MS"
        in response.headers
    )


def test_untrusted_host_is_rejected(
    client,
):
    """
    Verify trusted-host protection.
    """

    response = client.get(
        "/health",
        headers={
            "Host": (
                "malicious.example"
            )
        },
    )

    assert (
        response.status_code
        == 400
    )


def test_cors_allows_local_frontend(
    client,
):
    """
    Verify configured frontend CORS.
    """

    response = client.options(
        "/health",
        headers={
            "Origin": (
                "http://localhost:5173"
            ),
            "Access-Control-Request-Method": (
                "GET"
            ),
        },
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        response.headers[
            "Access-Control-Allow-Origin"
        ]
        == "http://localhost:5173"
    )


def test_cors_rejects_unknown_origin(
    client,
):
    """
    Verify unknown origins do not receive
    CORS authorization.
    """

    response = client.options(
        "/health",
        headers={
            "Origin": (
                "https://malicious.example"
            ),
            "Access-Control-Request-Method": (
                "GET"
            ),
        },
    )

    assert (
        "Access-Control-Allow-Origin"
        not in response.headers
    )


def test_startup_script_exists():
    """
    Verify deployment startup script.
    """

    startup_script = (
        BACKEND_DIRECTORY
        / "start.sh"
    )

    assert (
        startup_script.exists()
    )


def test_startup_script_runs_migrations():
    """
    Verify migrations run before Uvicorn.
    """

    content = (
        BACKEND_DIRECTORY
        .joinpath(
            "start.sh"
        )
        .read_text(
            encoding="utf-8"
        )
    )

    migration_position = (
        content.find(
            "alembic upgrade head"
        )
    )

    server_position = (
        content.find(
            "exec uvicorn"
        )
    )

    assert (
        migration_position
        != -1
    )

    assert (
        server_position
        != -1
    )

    assert (
        migration_position
        < server_position
    )


def test_dockerfile_uses_startup_script():
    """
    Verify container startup uses the
    deployment script.
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
        "COPY start.sh"
        in content
    )

    assert (
        "chmod +x"
        in content
    )

    assert (
        'CMD ["/app/start.sh"]'
        in content
    )


def test_environment_files_are_ignored():
    """
    Verify Git excludes secret files.
    """

    gitignore = (
        PROJECT_DIRECTORY
        / ".gitignore"
    )

    assert (
        gitignore.exists()
    )

    content = (
        gitignore.read_text(
            encoding="utf-8"
        )
    )

    assert (
        ".env"
        in content
    )