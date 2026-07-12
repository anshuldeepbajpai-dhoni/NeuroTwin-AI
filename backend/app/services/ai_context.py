from sqlalchemy.orm import Session

from app.crud.conversation import (
    get_conversation_by_id,
)
from app.models.digital_twin import DigitalTwin
from app.models.user import User
from app.services.conversation_context import (
    conversation_context_builder,
)
from app.services.memory_context import (
    memory_context_builder,
)
from app.services.prompt_builder import (
    prompt_builder,
)


class AIContextBuilder:
    """
    Build the complete context sent
    to the AI provider.
    """

    def build_context(
        self,
        db: Session,
        digital_twin: DigitalTwin,
        conversation_id: str,
        user_id: str,
    ) -> list[dict[str, str]]:
        """
        Combine the Digital Twin prompt,
        saved memories, conversation summary,
        and recent conversation history.
        """

        system_prompt = (
            prompt_builder.build_system_prompt(
                digital_twin
            )
        )

        memory_context = (
            memory_context_builder.build_context(
                db=db,
                user_id=user_id,
                digital_twin_id=(
                    digital_twin.id
                ),
            )
        )

        complete_system_prompt = (
            f"{system_prompt}\n\n"
            "Relevant user memory context:\n"
            f"{memory_context}\n\n"
            "Memory usage rules:\n"
            "- Use memories only when relevant.\n"
            "- Do not say that memories came "
            "from a database.\n"
            "- Do not reveal memory metadata "
            "unless requested.\n"
            "- Do not invent information that "
            "is absent from the memories.\n"
            "- If an old memory conflicts with "
            "the user's latest message, follow "
            "the latest message."
        )

        conversation = (
            db.query(
                __import__(
                    "app.models.conversation",
                    fromlist=[
                        "Conversation"
                    ],
                ).Conversation
            )
            .filter(
                __import__(
                    "app.models.conversation",
                    fromlist=[
                        "Conversation"
                    ],
                ).Conversation.id
                == conversation_id,
                __import__(
                    "app.models.conversation",
                    fromlist=[
                        "Conversation"
                    ],
                ).Conversation.user_id
                == user_id,
            )
            .first()
        )

        messages = [
            {
                "role": "system",
                "content": (
                    complete_system_prompt
                ),
            }
        ]

        if (
            conversation
            and conversation.summary
        ):
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "Previous conversation "
                        "summary:\n"
                        f"{conversation.summary}"
                    ),
                }
            )

        conversation_history = (
            conversation_context_builder
            .build_context(
                db=db,
                conversation_id=(
                    conversation_id
                ),
                user_id=user_id,
            )
        )

        messages.extend(
            conversation_history
        )

        return messages


ai_context_builder = (
    AIContextBuilder()
)