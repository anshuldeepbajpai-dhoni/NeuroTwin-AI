import math

from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.exceptions import (
    ConversationNotFoundException,
    InvalidMessageRoleException,
    MessageNotFoundException,
)
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate


def get_owned_conversation(
    db: Session,
    current_user: User,
    conversation_id: str,
) -> Conversation:
    """
    Retrieve a Conversation only when it belongs
    to the authenticated user.

    Raises:
        ConversationNotFoundException:
            If the Conversation does not exist or
            belongs to another user.
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


def create_message(
    db: Session,
    current_user: User,
    conversation_id: str,
    message_data: MessageCreate,
) -> Message:
    """
    Create a user Message inside an owned
    Conversation.

    Public users are allowed to create only
    messages with the user role.
    """

    get_owned_conversation(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
    )

    if message_data.role != "user":
        raise InvalidMessageRoleException()

    message = Message(
        conversation_id=conversation_id,
        user_id=current_user.id,
        role=message_data.role,
        content=message_data.content,
    )

    db.add(
        message
    )

    db.commit()

    db.refresh(
        message
    )

    return message


def create_internal_message(
    db: Session,
    current_user: User,
    conversation_id: str,
    role: str,
    content: str,
) -> Message:
    """
    Create an internal assistant or system Message.

    This function is intended for future AI and
    system services. It should not be exposed
    directly through a public API endpoint.
    """

    get_owned_conversation(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
    )

    allowed_roles = {
        "assistant",
        "system",
    }

    if role not in allowed_roles:
        raise InvalidMessageRoleException(
            message=(
                "Internal messages must use "
                "the assistant or system role."
            )
        )

    message = Message(
        conversation_id=conversation_id,
        user_id=current_user.id,
        role=role,
        content=content,
    )

    db.add(
        message
    )

    db.commit()

    db.refresh(
        message
    )

    return message


def get_message_by_id(
    db: Session,
    current_user: User,
    conversation_id: str,
    message_id: str,
) -> Message:
    """
    Retrieve one Message owned by the
    authenticated user and belonging to the
    specified Conversation.
    """

    get_owned_conversation(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
    )

    message = (
        db.query(Message)
        .filter(
            Message.id
            == message_id,
            Message.conversation_id
            == conversation_id,
            Message.user_id
            == current_user.id,
        )
        .first()
    )

    if message is None:
        raise MessageNotFoundException()

    return message


def get_messages(
    db: Session,
    current_user: User,
    conversation_id: str,
    role: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort_order: str = "asc",
) -> dict:
    """
    Retrieve paginated Message history from an
    owned Conversation.

    Messages are sorted chronologically by
    created_at.
    """

    get_owned_conversation(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
    )

    query = (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation_id,
            Message.user_id
            == current_user.id,
        )
    )

    if role is not None:
        query = query.filter(
            Message.role
            == role
        )

    total = (
        query.with_entities(
            func.count(
                Message.id
            )
        )
        .scalar()
        or 0
    )

    if sort_order == "desc":
        query = query.order_by(
            desc(
                Message.created_at
            ),
            desc(
                Message.id
            ),
        )

    else:
        query = query.order_by(
            asc(
                Message.created_at
            ),
            asc(
                Message.id
            ),
        )

    offset = (
        page - 1
    ) * page_size

    messages = (
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
        "items": messages,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def delete_message(
    db: Session,
    current_user: User,
    conversation_id: str,
    message_id: str,
) -> dict:
    """
    Delete one Message owned by the
    authenticated user.
    """

    message = get_message_by_id(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
        message_id=message_id,
    )

    db.delete(
        message
    )

    db.commit()

    return {
        "message": (
            "Message deleted successfully."
        )
    }