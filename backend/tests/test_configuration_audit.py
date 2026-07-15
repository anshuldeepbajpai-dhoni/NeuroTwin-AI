from unittest.mock import patch

from app.services.configuration_audit import (
    ConfigurationAuditService,
)


def test_valid_development_configuration():
    """
    Verify that a valid development
    configuration passes the audit.
    """

    service = (
        ConfigurationAuditService()
    )

    values = {
        "environment": "development",
        "database_url": (
            "postgresql://"
            "user:password@localhost/"
            "neurotwin"
        ),
        "secret_key": (
            "development-secret-key-"
            "with-more-than-32-characters"
        ),
        "openai_api_key": (
            "test-api-key"
        ),
        "ollama_base_url": "",
    }

    with patch.object(
        service,
        "get_setting",
        side_effect=lambda name, default=None: (
            values.get(
                name,
                default,
            )
        ),
    ):

        result = (
            service.run_audit()
        )

    assert result.is_valid is True

    assert result.errors == []

    assert (
        result.environment
        == "development"
    )


def test_missing_database_url_fails():
    """
    Verify that a missing database URL
    fails configuration validation.
    """

    service = (
        ConfigurationAuditService()
    )

    values = {
        "environment": "development",
        "database_url": "",
        "secret_key": (
            "development-secret-key-"
            "with-more-than-32-characters"
        ),
        "openai_api_key": (
            "test-api-key"
        ),
        "ollama_base_url": "",
    }

    with patch.object(
        service,
        "get_setting",
        side_effect=lambda name, default=None: (
            values.get(
                name,
                default,
            )
        ),
    ):

        result = (
            service.run_audit()
        )

    assert result.is_valid is False

    assert (
        "DATABASE_URL is missing."
        in result.errors
    )


def test_unsupported_database_fails():
    """
    Verify rejection of unsupported
    database connection schemes.
    """

    service = (
        ConfigurationAuditService()
    )

    values = {
        "environment": "development",
        "database_url": (
            "mysql://localhost/"
            "neurotwin"
        ),
        "secret_key": (
            "development-secret-key-"
            "with-more-than-32-characters"
        ),
        "openai_api_key": (
            "test-api-key"
        ),
        "ollama_base_url": "",
    }

    with patch.object(
        service,
        "get_setting",
        side_effect=lambda name, default=None: (
            values.get(
                name,
                default,
            )
        ),
    ):

        result = (
            service.run_audit()
        )

    assert result.is_valid is False

    assert any(
        "unsupported database scheme"
        in error
        for error in result.errors
    )


def test_weak_production_secret_fails():
    """
    Verify that production rejects weak
    JWT secrets.
    """

    service = (
        ConfigurationAuditService()
    )

    values = {
        "environment": "production",
        "database_url": (
            "postgresql://"
            "user:password@database/"
            "neurotwin"
        ),
        "secret_key": "change-me",
        "openai_api_key": (
            "test-api-key"
        ),
        "ollama_base_url": "",
    }

    with patch.object(
        service,
        "get_setting",
        side_effect=lambda name, default=None: (
            values.get(
                name,
                default,
            )
        ),
    ):

        result = (
            service.run_audit()
        )

    assert result.is_valid is False

    assert any(
        "Production SECRET_KEY"
        in error
        for error in result.errors
    )


def test_weak_development_secret_warns():
    """
    Verify that a weak development
    secret creates a warning.
    """

    service = (
        ConfigurationAuditService()
    )

    values = {
        "environment": "development",
        "database_url": (
            "sqlite:///./test.db"
        ),
        "secret_key": "short-secret",
        "openai_api_key": (
            "test-api-key"
        ),
        "ollama_base_url": "",
    }

    with patch.object(
        service,
        "get_setting",
        side_effect=lambda name, default=None: (
            values.get(
                name,
                default,
            )
        ),
    ):

        result = (
            service.run_audit()
        )

    assert result.is_valid is True

    assert any(
        "32 characters"
        in warning
        for warning in result.warnings
    )


def test_missing_ai_provider_warns():
    """
    Verify that missing AI-provider
    configuration creates a warning.
    """

    service = (
        ConfigurationAuditService()
    )

    values = {
        "environment": "development",
        "database_url": (
            "sqlite:///./test.db"
        ),
        "secret_key": (
            "development-secret-key-"
            "with-more-than-32-characters"
        ),
        "openai_api_key": "",
        "ollama_base_url": "",
    }

    with patch.object(
        service,
        "get_setting",
        side_effect=lambda name, default=None: (
            values.get(
                name,
                default,
            )
        ),
    ):

        result = (
            service.run_audit()
        )

    assert result.is_valid is True

    assert any(
        "AI provider"
        in warning
        for warning in result.warnings
    )


def test_invalid_environment_fails():
    """
    Verify rejection of unsupported
    environment names.
    """

    service = (
        ConfigurationAuditService()
    )

    values = {
        "environment": "unknown",
        "database_url": (
            "sqlite:///./test.db"
        ),
        "secret_key": (
            "development-secret-key-"
            "with-more-than-32-characters"
        ),
        "openai_api_key": (
            "test-api-key"
        ),
        "ollama_base_url": "",
    }

    with patch.object(
        service,
        "get_setting",
        side_effect=lambda name, default=None: (
            values.get(
                name,
                default,
            )
        ),
    ):

        result = (
            service.run_audit()
        )

    assert result.is_valid is False

    assert any(
        "Unsupported application"
        in error
        for error in result.errors
    )