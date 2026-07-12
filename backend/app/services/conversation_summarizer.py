import logging

from app.core.config import settings
from app.services.ai_provider import (
    ai_provider_service,
)


logger = logging.getLogger(__name__)


class ConversationSummarizer:
    """
    Generate a concise summary of a
    sufficiently long conversation.
    """

    SYSTEM_PROMPT = """
Summarize the conversation accurately and
concisely for future AI context.

Preserve:

- Important user goals
- Stable preferences
- User interests
- Skills and learning progress
- Projects and decisions
- Important facts
- Unresolved tasks
- Useful conversation context

Do not include:

- Greetings
- Repeated information
- Unimportant small talk
- Passwords
- API keys
- Access tokens
- Sensitive authentication information

Do not invent information.

Return only the summary as plain text.
""".strip()

    def summarize(
        self,
        messages: list,
    ) -> str | None:
        """
        Summarize a conversation only when
        enough valid messages are available.
        """

        valid_messages = (
            self.prepare_messages(
                messages
            )
        )

        if (
            len(valid_messages)
            < settings.ai_summary_min_messages
        ):
            return None

        conversation_text = (
            self.build_conversation_text(
                valid_messages
            )
        )

        summary_messages = [
            {
                "role": "system",
                "content": (
                    self.SYSTEM_PROMPT
                ),
            },
            {
                "role": "user",
                "content": (
                    "Summarize this "
                    "conversation:\n\n"
                    f"{conversation_text}"
                ),
            },
        ]

        try:
            summary = (
                ai_provider_service
                .generate_response(
                    messages=summary_messages
                )
            )

        except Exception as error:
            logger.warning(
                "Conversation summarization "
                "failed: %s",
                error,
            )

            return None

        clean_summary = summary.strip()

        if not clean_summary:
            return None

        return clean_summary[
            :settings
            .ai_summary_max_characters
        ]

    @staticmethod
    def prepare_messages(
        messages: list,
    ) -> list[dict[str, str]]:
        """
        Convert Message models or dictionaries
        into a consistent chat-message format.
        """

        prepared_messages = []

        for message in messages:

            if isinstance(
                message,
                dict,
            ):
                role = message.get(
                    "role"
                )

                content = message.get(
                    "content"
                )

            else:
                role = getattr(
                    message,
                    "role",
                    None,
                )

                content = getattr(
                    message,
                    "content",
                    None,
                )

            if (
                role not in {
                    "user",
                    "assistant",
                }
                or not isinstance(
                    content,
                    str,
                )
                or not content.strip()
            ):
                continue

            prepared_messages.append(
                {
                    "role": role,
                    "content": (
                        content.strip()
                    ),
                }
            )

        return prepared_messages

    @staticmethod
    def build_conversation_text(
        messages: list[
            dict[str, str]
        ],
    ) -> str:
        """
        Convert prepared chat messages into
        readable conversation text.
        """

        conversation_lines = []

        for message in messages:

            role = (
                message["role"]
                .capitalize()
            )

            content = (
                message["content"]
            )

            conversation_lines.append(
                f"{role}: {content}"
            )

        return "\n".join(
            conversation_lines
        )


conversation_summarizer = (
    ConversationSummarizer()
)