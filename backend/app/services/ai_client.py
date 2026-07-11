from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

from app.core.config import settings
from app.exceptions.ai import (
    AIAuthenticationException,
    AIConfigurationException,
    AIConnectionException,
    AIQuotaExceededException,
    AIRateLimitException,
    AIResponseException,
    AITimeoutException,
)


class AIClient:
    """
    Reusable OpenAI client for NeuroTwin AI.
    """

    def __init__(self):

        if not settings.openai_api_key:
            raise AIConfigurationException(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.ai_timeout_seconds,
        )

        self.model = settings.ai_model

        self.temperature = (
            settings.ai_temperature
        )

        self.max_tokens = (
            settings.ai_max_tokens
        )


    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Generate an AI response and convert
        provider errors into application errors.
        """

        try:

            response = (
                self.client
                .chat
                .completions
                .create(
                    model=self.model,
                    messages=messages,
                    temperature=(
                        self.temperature
                    ),
                    max_tokens=(
                        self.max_tokens
                    ),
                )
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            if not content:
                raise AIResponseException()

            return content.strip()

        except AuthenticationError as exc:

            raise AIAuthenticationException() from exc

        except RateLimitError as exc:

            error_text = str(
                exc
            ).lower()

            if (
                "insufficient_quota"
                in error_text
                or "quota"
                in error_text
            ):
                raise (
                    AIQuotaExceededException()
                ) from exc

            raise AIRateLimitException() from exc

        except APITimeoutError as exc:

            raise AITimeoutException() from exc

        except APIConnectionError as exc:

            raise AIConnectionException() from exc

        except (
            AIAuthenticationException,
            AIConfigurationException,
            AIConnectionException,
            AIQuotaExceededException,
            AIRateLimitException,
            AIResponseException,
            AITimeoutException,
        ):

            raise

        except Exception as exc:

            raise AIResponseException(
                "AI response generation failed."
            ) from exc


ai_client = AIClient()