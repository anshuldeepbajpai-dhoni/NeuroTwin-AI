import json
import logging

from app.services.ai_provider import (
    ai_provider_service,
)
from pydantic import ValidationError

from app.schemas.memory_extraction import (
    MemoryExtractionResult,
)


logger = logging.getLogger(
    __name__
)


class MemoryExtractor:
    """
    Extract useful long-term memories
    from user messages using AI.
    """

    EXTRACTION_PROMPT = """
Analyze the user's message and identify useful
long-term information that could improve future
personalized responses.

Extract only stable and meaningful information,
such as:

- Goals
- Preferences
- Interests
- Skills
- Education
- Career information
- Projects
- Important personal facts

Do not extract:

- Greetings
- Temporary requests
- One-time questions
- Passwords
- API keys
- Access tokens
- Financial account details
- Highly sensitive information
- Information that is uncertain

Return only valid JSON.

If useful information exists, return:

{
  "should_save": true,
  "title": "Short memory title",
  "content": "Clear memory statement",
  "category": "goal",
  "importance": 8
}

If no useful information exists, return:

{
  "should_save": false,
  "title": null,
  "content": null,
  "category": null,
  "importance": null
}

Allowed categories:

goal
preference
interest
skill
education
career
project
personal
""".strip()

    def extract(
        self,
        user_message: str,
    ) -> dict:
        """
        Analyze a user message and return
        structured memory information.
        """

        clean_message = (
            user_message.strip()
        )

        if not clean_message:

            raise ValueError(
                "User message cannot be empty."
            )

        messages = [
            {
                "role": "system",
                "content": (
                    self.EXTRACTION_PROMPT
                ),
            },
            {
                "role": "user",
                "content": clean_message,
            },
        ]

        ai_response = (
            ai_provider_service
            .generate_response(
                messages=messages
            )
        )

        clean_response = (
            self._clean_json_response(
                ai_response
            )
        )

        try:

            extracted_memory = (
                json.loads(
                    clean_response
                )
            )

        except json.JSONDecodeError:

            logger.warning(
                "Memory extraction returned "
                "invalid JSON."
            )

            return self.empty_result()

        try:

            validated_memory = (
                MemoryExtractionResult
                .model_validate(
                    extracted_memory
                )
            )

        except ValidationError as error:

            logger.warning(
                "Invalid extracted memory "
                "structure: %s",
                error,
            )

            return self.empty_result()

        return validated_memory.model_dump()

@staticmethod
def _clean_json_response(
    response: str,
) -> str:
    """
    Extract the JSON object from an
    AI-generated response.
    """

    clean_response = response.strip()

    if clean_response.startswith(
        "```json"
    ):
        clean_response = (
            clean_response[7:]
        )

    elif clean_response.startswith(
        "```"
    ):
        clean_response = (
            clean_response[3:]
        )

    if clean_response.endswith(
        "```"
    ):
        clean_response = (
            clean_response[:-3]
        )

    clean_response = (
        clean_response.strip()
    )

    json_start = (
        clean_response.find("{")
    )

    json_end = (
        clean_response.rfind("}")
    )

    if (
        json_start == -1
        or json_end == -1
        or json_end < json_start
    ):
        return clean_response

    return clean_response[
        json_start:json_end + 1
    ]

    @staticmethod
    def empty_result() -> dict:
        """
        Return the default result when no
        useful memory can be extracted.
        """

        return {
            "should_save": False,
            "title": None,
            "content": None,
            "category": None,
            "importance": None,
        }


memory_extractor = MemoryExtractor()