import httpx

from app.core.config import settings


class OllamaClient:
    """
    Generate AI responses using a local
    Ollama model.
    """

    def __init__(self) -> None:

        self.base_url = (
            settings.ollama_base_url.rstrip(
                "/"
            )
        )

        self.model = (
            settings.ollama_model
        )

        self.timeout = (
            settings.ai_timeout_seconds
        )

    def generate_response(
        self,
        messages: list[
            dict[str, str]
        ],
    ) -> str:
        """
        Send chat messages to Ollama and
        return the generated response.
        """

        if not messages:

            raise ValueError(
                "Messages cannot be empty."
            )

        response = httpx.post(
            url=(
                f"{self.base_url}"
                "/api/chat"
            ),
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": (
                        settings
                        .ai_temperature
                    ),
                    "num_predict": (
                        settings
                        .ai_max_tokens
                    ),
                },
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        response_data = (
            response.json()
        )

        content = (
            response_data
            .get(
                "message",
                {},
            )
            .get(
                "content",
                "",
            )
            .strip()
        )

        if not content:

            raise RuntimeError(
                "Ollama returned an "
                "empty response."
            )

        return content


ollama_client = OllamaClient()