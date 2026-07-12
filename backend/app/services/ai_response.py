from sqlalchemy.orm import Session

from app.models.digital_twin import DigitalTwin
from app.services.ai_provider import (
    ai_provider_service,
)
from app.services.ai_context import (
    ai_context_builder,
)


class AIResponseService:
    """
    Generate AI responses using the
    Digital Twin context, saved memories,
    and recent conversation history.
    """

    def generate_response(
        self,
        db: Session,
        digital_twin: DigitalTwin,
        conversation_id: str,
        user_id: str,
        user_message: str,
    ) -> str:
        """
        Build the complete AI context,
        append the current user message,
        and generate an AI response.
        """

        clean_message = (
            user_message.strip()
        )

        if not clean_message:
            raise ValueError(
                "User message cannot be empty."
            )

        messages = (
            ai_context_builder.build_context(
                db=db,
                digital_twin=digital_twin,
                conversation_id=(
                    conversation_id
                ),
                user_id=user_id,
            )
        )

        messages.append(
            {
                "role": "user",
                "content": clean_message,
            }
        )

        ai_response = (
            ai_provider_service
            .generate_response(
                messages=messages
            )
        )
        return ai_response


ai_response_service = (
    AIResponseService()
)