import math

from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions import (
    ConversationNotFoundException,
    DigitalTwinNotFoundException,
    EmptyConversationUpdateException,
)
from app.models.conversation import Conversation
from app.models.digital_twin import DigitalTwin
from app.models.user import User
from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
)


def get_user_digital_twin(
    db: Session,
    current_user: User,
) -> DigitalTwin:
    """
    Retrieve the authenticated user's Digital Twin.

    Raises:
        DigitalTwinNotFoundException:
            If the user has no Digital Twin.
    """

    digital_twin = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.user_id
            == current_user.id
        )
        .first()
    )

    if digital_twin is None:
        raise DigitalTwinNotFoundException()

    return digital_twin


def create_conversation(
    db: Session,
    current_user: User,
    conversation_data: ConversationCreate,
) -> Conversation:
    """
    Create a Conversation for the authenticated
    user's Digital Twin.
    """

    digital_twin = get_user_digital_twin(
        db=db,
        current_user=current_user,
    )

    conversation = Conversation(
        user_id=current_user.id,
        digital_twin_id=digital_twin.id,
        title=conversation_data.title,
        is_archived=False,
    )

    db.add(
        conversation
    )

    db.commit()

    db.refresh(
        conversation
    )

    return conversation


def get_conversation_by_id(
    db: Session,
    current_user: User,
    conversation_id: str,
) -> Conversation:
    """
    Retrieve one Conversation owned by the
    authenticated user.
    """

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id
            == conversation_id,
            Conversation.user_id
            == current_user.id,
        )
        .first()
    )

    if conversation is None:
        raise ConversationNotFoundException()

    return conversation


def get_conversations(
    db: Session,
    current_user: User,
    search: str | None = None,
    is_archived: bool | None = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "updated_at",
    sort_order: str = "desc",
) -> dict:
    """
    Retrieve the authenticated user's Conversations
    with search, filtering, pagination, and sorting.
    """

    query = (
        db.query(Conversation)
        .filter(
            Conversation.user_id
            == current_user.id
        )
    )

    if search:

        search_value = (
            f"%{search.strip()}%"
        )

        query = query.filter(
            or_(
                Conversation.title.ilike(
                    search_value
                ),
            )
        )

    if is_archived is not None:

        query = query.filter(
            Conversation.is_archived
            == is_archived
        )

    total = (
        query.with_entities(
            func.count(
                Conversation.id
            )
        )
        .scalar()
        or 0
    )

    sortable_fields = {
        "created_at": (
            Conversation.created_at
        ),
        "updated_at": (
            Conversation.updated_at
        ),
        "title": (
            Conversation.title
        ),
    }

    sort_column = sortable_fields.get(
        sort_by,
        Conversation.updated_at,
    )

    if sort_order == "asc":

        query = query.order_by(
            asc(
                sort_column
            )
        )

    else:

        query = query.order_by(
            desc(
                sort_column
            )
        )

    offset = (
        page - 1
    ) * page_size

    conversations = (
        query.offset(
            offset
        )
        .limit(
            page_size
        )
        .all()
    )

    total_pages = (
        math.ceil(
            total / page_size
        )
        if total > 0
        else 0
    )

    return {
        "items": conversations,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def update_conversation(
    db: Session,
    current_user: User,
    conversation_id: str,
    conversation_data: ConversationUpdate,
) -> Conversation:
    """
    Update a Conversation owned by the
    authenticated user.
    """

    conversation = get_conversation_by_id(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
    )

    update_data = (
        conversation_data.model_dump(
            exclude_unset=True
        )
    )

    if not update_data:
        raise (
            EmptyConversationUpdateException()
        )

    for field, value in (
        update_data.items()
    ):
        setattr(
            conversation,
            field,
            value,
        )

    db.commit()

    db.refresh(
        conversation
    )

    return conversation


def delete_conversation(
    db: Session,
    current_user: User,
    conversation_id: str,
) -> dict:
    """
    Delete a Conversation owned by the
    authenticated user.
    """

    conversation = get_conversation_by_id(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
    )

    db.delete(
        conversation
    )

    db.commit()

    return {
        "message": (
            "Conversation deleted successfully."
        )
    }