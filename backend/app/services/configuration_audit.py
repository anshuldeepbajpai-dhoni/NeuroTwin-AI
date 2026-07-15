from dataclasses import (
    dataclass,
)
from urllib.parse import (
    urlparse,
)

from app.core.config import (
    settings,
)


@dataclass
class ConfigurationAuditResult:
    """
    Store the result of one complete
    application-configuration audit.
    """

    is_valid: bool

    environment: str

    errors: list[str]

    warnings: list[str]


class ConfigurationAuditService:
    """
    Validate deployment configuration
    without exposing secret values.
    """

    DEVELOPMENT_SECRET_VALUES = {
        "",
        "secret",
        "secret-key",
        "change-me",
        "your-secret-key",
        "development-secret",
    }

    SUPPORTED_ENVIRONMENTS = {
        "development",
        "testing",
        "staging",
        "production",
    }

    @staticmethod
    def get_setting(
        name: str,
        default=None,
    ):
        """
        Read an optional setting without
        breaking older configurations.
        """

        return getattr(
            settings,
            name,
            default,
        )

    def validate_environment(
        self,
        errors: list[str],
    ) -> str:
        """
        Validate the deployment
        environment name.
        """

        environment = str(
            self.get_setting(
                "environment",
                "development",
            )
        ).strip().lower()

        if (
            environment
            not in self
            .SUPPORTED_ENVIRONMENTS
        ):

            errors.append(
                "Unsupported application "
                "environment."
            )

        return environment

    def validate_database(
        self,
        errors: list[str],
    ) -> None:
        """
        Validate the configured database
        connection URL.
        """

        database_url = str(
            self.get_setting(
                "database_url",
                "",
            )
        ).strip()

        if not database_url:

            errors.append(
                "DATABASE_URL is missing."
            )

            return

        parsed_url = urlparse(
            database_url
        )

        supported_schemes = {
            "postgresql",
            "postgresql+psycopg2",
            "postgresql+psycopg",
            "sqlite",
        }

        if (
            parsed_url.scheme
            not in supported_schemes
        ):

            errors.append(
                "DATABASE_URL uses an "
                "unsupported database scheme."
            )

    def validate_secret(
        self,
        environment: str,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        """
        Validate JWT secret configuration
        without exposing its value.
        """

        secret_key = str(
            self.get_setting(
                "secret_key",
                "",
            )
        ).strip()

        normalized_secret = (
            secret_key.lower()
        )

        if not secret_key:

            errors.append(
                "SECRET_KEY is missing."
            )

            return

        if (
            environment
            == "production"
            and (
                normalized_secret
                in self
                .DEVELOPMENT_SECRET_VALUES
                or len(
                    secret_key
                ) < 32
            )
        ):

            errors.append(
                "Production SECRET_KEY must "
                "be unique and at least "
                "32 characters long."
            )

        elif (
            len(
                secret_key
            )
            < 32
        ):

            warnings.append(
                "SECRET_KEY should be at "
                "least 32 characters long."
            )

    def validate_ai_configuration(
        self,
        warnings: list[str],
    ) -> None:
        """
        Check whether an AI provider is
        configured.
        """

        openai_api_key = str(
            self.get_setting(
                "openai_api_key",
                "",
            )
            or ""
        ).strip()

        ollama_base_url = str(
            self.get_setting(
                "ollama_base_url",
                "",
            )
            or ""
        ).strip()

        if (
            not openai_api_key
            and not ollama_base_url
        ):

            warnings.append(
                "No external or local AI "
                "provider is configured."
            )

    def run_audit(
        self,
    ) -> ConfigurationAuditResult:
        """
        Execute the complete deployment
        configuration audit.
        """

        errors = []

        warnings = []

        environment = (
            self.validate_environment(
                errors=errors
            )
        )

        self.validate_database(
            errors=errors
        )

        self.validate_secret(
            environment=environment,
            errors=errors,
            warnings=warnings,
        )

        self.validate_ai_configuration(
            warnings=warnings
        )

        return ConfigurationAuditResult(
            is_valid=(
                len(
                    errors
                )
                == 0
            ),
            environment=environment,
            errors=errors,
            warnings=warnings,
        )


configuration_audit_service = (
    ConfigurationAuditService()
)