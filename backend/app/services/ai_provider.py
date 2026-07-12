import logging

from app.core.config import settings
from app.services.ai_client import (
    ai_client,
)
from app.services.ollama_client import (
    ollama_client,
)


logger = logging.getLogger(
    __name__
)


class AIProviderService:
    """
    Generate AI responses using OpenAI
    with Ollama as a local fallback.
    """

    def generate_response(
        self,
        messages: list[
            dict[str, str]
        ],
    ) -> str:
        """
        Try the configured primary AI
        provider and use Ollama if the
        primary provider fails.
        """

        if not messages:

            raise ValueError(
                "Messages cannot be empty."
            )

        try:

            return (
                ai_client
                .generate_response(
                    messages=messages
                )
            )

        except Exception as error:

            if not (
                settings
                .ai_fallback_enabled
            ):

                raise

            logger.warning(
                (
                    "Primary AI provider "
                    "failed. Using Ollama "
                    "fallback. Error: %s"
                ),
                error,
            )

            return (
                ollama_client
                .generate_response(
                    messages=messages
                )
            )


ai_provider_service = (
    AIProviderService()
)