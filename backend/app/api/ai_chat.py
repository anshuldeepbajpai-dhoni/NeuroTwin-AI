from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.crud.conversation import (
    get_conversation_by_id,
)
from app.crud.digital_twin import (
    get_digital_twin,
)
from app.crud.message import (
    create_message,
)
from app.database.session import (
    get_db,
)
from app.dependencies.auth import (
    get_current_user,
)
from app.models.user import User
from app.schemas.ai_chat import (
    AIChatRequest,
    AIChatResponse,
)
from app.schemas.message import (
    MessageCreate,
)
from app.services.ai_chat import (
    ai_chat_service,
)
from app.services.conversation_title import (
    conversation_title_service,
)
from app.services.automatic_memory import (
    automatic_memory_service,
)


router = APIRouter(
    prefix="/conversations",
    tags=["AI Chat"],
)


@router.post(
    "/{conversation_id}/chat",
    response_model=AIChatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Chat with Digital Twin",
    description=(
        "Send a message to the authenticated "
        "user's Digital Twin and receive an "
        "AI-generated response."
    ),
)
def chat_with_digital_twin(
    conversation_id: str,
    chat_data: AIChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Save the user message, generate an AI
    response, save the assistant message,
    and return both messages.
    """

    conversation = (
        get_conversation_by_id(
            db=db,
            current_user=current_user,
            conversation_id=(
                conversation_id
            ),
        )
    )

    digital_twin = (
        get_digital_twin(
            db=db,
            current_user=current_user,
        )
    )

    user_message = create_message(
        db=db,
        current_user=current_user,
        conversation_id=(
            conversation.id
        ),
        message_data=MessageCreate(
            role="user",
            content=chat_data.message,
        ),
    )

    default_titles = {
    "new conversation",
    "untitled conversation",
    }

    current_title = (
        conversation.title
        .strip()
        .lower()
    )

    if current_title in default_titles:

        conversation.title = (
            conversation_title_service
            .generate_title(
                chat_data.message
            )
        )

        db.commit()

        db.refresh(
            conversation
        )

    try:

        assistant_message = (
            ai_chat_service.generate_reply(
                db=db,
                conversation=conversation,
                digital_twin=digital_twin,
                user_id=current_user.id,
                user_message=user_message,
            )
        )

    except Exception:

        db.rollback()

        saved_user_message = (
            db.query(
                type(user_message)
            )
            .filter(
                type(user_message).id
                == user_message.id
            )
            .first()
        )

        if saved_user_message:

            db.delete(
                saved_user_message
            )

            db.commit()

        raise

    automatic_memory_service.process_message(
    db=db,
    current_user=current_user,
    user_message=chat_data.message,
    )         

    return AIChatResponse(
        user_message=user_message,
        assistant_message=(
            assistant_message
        ),
    )