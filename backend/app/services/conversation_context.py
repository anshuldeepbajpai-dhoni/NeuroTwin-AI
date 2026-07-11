from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.message import Message


class ConversationContextBuilder:
    """
    Loads and formats recent Conversation
    Messages for the AI model.
    """

    @staticmethod
    def get_recent_messages(
        db: Session,
        conversation_id: str,
        user_id: str,
    ) -> list[Message]:
        """
        Retrieve the latest Messages from
        the authenticated user's Conversation.
        """

        messages = (
            db.query(
                Message
            )
            .filter(
                Message.conversation_id
                == conversation_id,
                Message.user_id
                == user_id,
            )
            .order_by(
                desc(
                    Message.created_at
                ),
                desc(
                    Message.id
                ),
            )
            .limit(
                settings
                .ai_max_history_messages
            )
            .all()
        )

        # The database query returns newest first.
        # Reverse it for chronological AI context.

        messages.reverse()

        return messages

    @staticmethod
    def build_history(
        messages: list[Message],
    ) -> list[dict[str, str]]:
        """
        Convert database Messages into
        OpenAI-compatible chat Messages.
        """

        history = []

        allowed_roles = {
            "user",
            "assistant",
            "system",
        }

        for message in messages:

            role = (
                message.role
                .strip()
                .lower()
            )

            content = (
                message.content
                .strip()
            )

            if (
                role not in allowed_roles
                or not content
            ):
                continue

            history.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        return history

    def build_context(
        self,
        db: Session,
        conversation_id: str,
        user_id: str,
    ) -> list[dict[str, str]]:
        """
        Load and format recent Conversation
        history for the AI model.
        """

        messages = (
            self.get_recent_messages(
                db=db,
                conversation_id=(
                    conversation_id
                ),
                user_id=user_id,
            )
        )

        return self.build_history(
            messages
        )


conversation_context_builder = (
    ConversationContextBuilder()
)