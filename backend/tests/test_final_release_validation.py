"""
Final backend release-validation tests.

These tests verify the production-critical
configuration required for the NeuroTwin AI
backend release.
"""

from pathlib import Path

import yaml

from app.main import app


# ======================================================
# Project Paths
# ======================================================

BACKEND_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)

PROJECT_ROOT = (
    BACKEND_DIR.parent
)

DOCKERFILE_PATH = (
    BACKEND_DIR
    / "Dockerfile"
)

STARTUP_SCRIPT_PATH = (
    BACKEND_DIR
    / "start.sh"
)

ALEMBIC_CONFIG_PATH = (
    BACKEND_DIR
    / "alembic.ini"
)

MIGRATIONS_DIRECTORY = (
    BACKEND_DIR
    / "migrations"
)

MIGRATION_VERSIONS_DIRECTORY = (
    MIGRATIONS_DIRECTORY
    / "versions"
)

COMPOSE_PATH = (
    PROJECT_ROOT
    / "docker-compose.yml"
)

GITIGNORE_PATH = (
    PROJECT_ROOT
    / ".gitignore"
)


# ======================================================
# Application Validation
# ======================================================

def test_application_metadata():

    assert (
        app.title
        == "NeuroTwin AI Backend API"
    )

    assert app.version

    assert app.description


def test_openapi_schema_is_generated():

    schema = app.openapi()

    assert (
        schema["info"]["title"]
        == app.title
    )

    assert (
        schema["info"]["version"]
        == app.version
    )

    assert "paths" in schema

    assert len(
        schema["paths"]
    ) > 0

def test_required_release_routes_exist():

    openapi_schema = app.openapi()

    registered_paths = {
        (
            path.rstrip("/")
            or "/"
        )
        for path
        in openapi_schema[
            "paths"
        ]
    }

    required_route_groups = {
        "authentication": {
            "/auth/register",
            "/auth/login",
        },
        "digital twin": {
            "/digital-twin",
        },
        "conversations": {
            "/conversations",
        },
    }

    missing_groups = []

    for (
        group_name,
        expected_paths,
    ) in required_route_groups.items():

        normalized_paths = {
            (
                path.rstrip("/")
                or "/"
            )
            for path
            in expected_paths
        }

        if not (
            registered_paths
            & normalized_paths
        ):

            missing_groups.append(
                group_name
            )

    assert not missing_groups, (
        "MISSING RELEASE API GROUPS: "
        f"{missing_groups}\n"
        "OPENAPI PATHS: "
        f"{sorted(registered_paths)}"
    )
    
# ======================================================
# Docker Validation
# ======================================================

def test_dockerfile_exists():

    assert (
        DOCKERFILE_PATH.exists()
    )


def test_dockerfile_uses_supported_python():

    content = (
        DOCKERFILE_PATH
        .read_text(
            encoding="utf-8"
        )
        .lower()
    )

    assert (
        "from python:3.11"
        in content
    )

def test_production_server_is_configured():

    dockerfile_content = (
        DOCKERFILE_PATH
        .read_text(
            encoding="utf-8"
        )
        .lower()
    )

    startup_content = (
        STARTUP_SCRIPT_PATH
        .read_text(
            encoding="utf-8"
        )
        .lower()
    )

    combined_content = (
        dockerfile_content
        + "\n"
        + startup_content
    )

    assert (
        "uvicorn"
        in combined_content
    ), (
        "UVICORN IS NOT CONFIGURED "
        "IN THE DOCKER STARTUP FLOW"
    )



def test_startup_script_exists():

    assert (
        STARTUP_SCRIPT_PATH.exists()
    )


def test_startup_runs_migrations():

    content = (
        STARTUP_SCRIPT_PATH
        .read_text(
            encoding="utf-8"
        )
        .lower()
    )

    assert (
        "alembic upgrade head"
        in content
    )


def test_startup_uses_exec():

    content = (
        STARTUP_SCRIPT_PATH
        .read_text(
            encoding="utf-8"
        )
        .lower()
    )

    assert "exec" in content


def test_compose_configuration_exists():

    assert (
        COMPOSE_PATH.exists()
    )


def test_compose_contains_release_services():

    with COMPOSE_PATH.open(
        encoding="utf-8"
    ) as compose_file:

        compose = yaml.safe_load(
            compose_file
        )

    services = (
        compose.get(
            "services",
            {},
        )
    )

    assert "backend" in services

    assert "db" in services


def test_backend_depends_on_database():

    with COMPOSE_PATH.open(
        encoding="utf-8"
    ) as compose_file:

        compose = yaml.safe_load(
            compose_file
        )

    backend = (
        compose[
            "services"
        ][
            "backend"
        ]
    )

    dependencies = (
        backend.get(
            "depends_on",
            {}
        )
    )

    assert "db" in dependencies


def test_backend_port_is_published():

    with COMPOSE_PATH.open(
        encoding="utf-8"
    ) as compose_file:

        compose = yaml.safe_load(
            compose_file
        )

    backend = (
        compose[
            "services"
        ][
            "backend"
        ]
    )

    ports = backend.get(
        "ports",
        []
    )

    published_ports = set()

    for port in ports:

        if isinstance(
            port,
            str,
        ):

            published_ports.add(
                port
            )

        elif isinstance(
            port,
            int,
        ):

            published_ports.add(
                str(port)
            )

        elif isinstance(
            port,
            dict,
        ):

            published = port.get(
                "published"
            )

            target = port.get(
                "target"
            )

            published_ports.add(
                f"{published}:{target}"
            )

    assert any(
        (
            port == "8000"
            or port.startswith(
                "8000:"
            )
            or port.endswith(
                ":8000"
            )
        )
        for port
        in published_ports
    ), (
        "BACKEND PORT 8000 IS "
        "NOT PUBLISHED: "
        f"{ports}"
    )

# ======================================================
# Alembic Validation
# ======================================================

def test_alembic_configuration_exists():

    assert (
        ALEMBIC_CONFIG_PATH.exists()
    )


def test_migration_environment_exists():

    assert (
        (
            MIGRATIONS_DIRECTORY
            / "env.py"
        ).exists()
    )


def test_migration_versions_exist():

    migration_files = [
        path
        for path
        in (
            MIGRATION_VERSIONS_DIRECTORY
            .glob("*.py")
        )
        if (
            path.name
            != "__init__.py"
        )
    ]

    assert migration_files, (
        "NO ALEMBIC MIGRATIONS FOUND"
    )


def test_initial_migration_is_not_empty():

    migration_files = [
        path
        for path
        in (
            MIGRATION_VERSIONS_DIRECTORY
            .glob("*.py")
        )
        if (
            path.name
            != "__init__.py"
        )
    ]

    migration_content = "\n".join(
        migration_file.read_text(
            encoding="utf-8"
        )
        for migration_file
        in migration_files
    )

    assert (
        "op.create_table"
        in migration_content
    ), (
        "INITIAL MIGRATION DOES NOT "
        "CREATE DATABASE TABLES"
    )


# ======================================================
# Repository Security Validation
# ======================================================

def test_gitignore_exists():

    assert (
        GITIGNORE_PATH.exists()
    )


def test_environment_files_are_ignored():

    content = (
        GITIGNORE_PATH
        .read_text(
            encoding="utf-8"
        )
        .lower()
    )

    assert (
        ".env"
        in content
    )


def test_private_keys_are_ignored():

    content = (
        GITIGNORE_PATH
        .read_text(
            encoding="utf-8"
        )
        .lower()
    )

    assert any(
        pattern
        in content
        for pattern in {
            "*.pem",
            "*.key",
            ".pem",
            ".key",
        }
    )


# ======================================================
# Release Validation
# ======================================================

def test_backend_release_requirements():

    required_files = {
        DOCKERFILE_PATH,
        STARTUP_SCRIPT_PATH,
        ALEMBIC_CONFIG_PATH,
        (
            MIGRATIONS_DIRECTORY
            / "env.py"
        ),
        COMPOSE_PATH,
        GITIGNORE_PATH,
    }

    missing_files = {
        str(path)
        for path
        in required_files
        if not path.exists()
    }

    assert not missing_files, (
        "MISSING BACKEND RELEASE FILES: "
        f"{missing_files}"
    )