from sqlalchemy.orm import Session

from app.crud.message import (
    create_assistant_message,
)
from app.models.conversation import (
    Conversation,
)
from app.models.digital_twin import (
    DigitalTwin,
)
from app.models.message import Message
from app.services.ai_response import (
    ai_response_service,
)


class AIChatService:
    """
    Coordinate AI response generation
    and assistant-message storage.
    """

    def generate_reply(
        self,
        db: Session,
        conversation: Conversation,
        digital_twin: DigitalTwin,
        user_id: str,
        user_message: Message,
    ) -> Message:
        """
        Generate a Digital Twin response
        and save it as an assistant message.
        """

        assistant_content = (
            ai_response_service
            .generate_response(
                db=db,
                digital_twin=digital_twin,
                conversation_id=(
                    conversation.id
                ),
                user_id=user_id,
                user_message=(
                    user_message.content
                ),
            )
        )

        assistant_message = (
            create_assistant_message(
                db=db,
                conversation_id=(
                    conversation.id
                ),
                user_id=user_id,
                content=assistant_content,
            )
        )

        return assistant_message


ai_chat_service = AIChatService()