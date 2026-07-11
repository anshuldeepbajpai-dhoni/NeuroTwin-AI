from typing import Literal

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.crud.message import (
    create_message,
    delete_message,
    get_message_by_id,
    get_messages,
)
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    PaginatedMessageResponse,
)


router = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["Messages"],
)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=201,
    summary="Create Message",
    description=(
        "Create a user Message inside an owned "
        "Conversation. Public users can create "
        "only Messages with the user role."
    ),
)
def create(
    conversation_id: str,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return create_message(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
        message_data=message_data,
    )


@router.get(
    "",
    response_model=PaginatedMessageResponse,
    summary="Get Conversation Messages",
    description=(
        "Retrieve paginated Message history from "
        "an owned Conversation with optional role "
        "filtering and chronological sorting."
    ),
)
def list_messages(
    conversation_id: str,
    role: Literal[
        "user",
        "assistant",
        "system",
    ] | None = Query(
        default=None,
        description=(
            "Filter Messages by role."
        ),
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number.",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description=(
            "Number of Messages per page."
        ),
    ),
    sort_order: Literal[
        "asc",
        "desc",
    ] = Query(
        default="asc",
        description=(
            "Message sorting direction."
        ),
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_messages(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
        role=role,
        page=page,
        page_size=page_size,
        sort_order=sort_order,
    )


@router.get(
    "/{message_id}",
    response_model=MessageResponse,
    summary="Get Message",
    description=(
        "Retrieve one Message from an owned "
        "Conversation."
    ),
)
def get_one(
    conversation_id: str,
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_message_by_id(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
        message_id=message_id,
    )


@router.delete(
    "/{message_id}",
    summary="Delete Message",
    description=(
        "Delete one Message from an owned "
        "Conversation."
    ),
)
def remove(
    conversation_id: str,
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return delete_message(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
        message_id=message_id,
    )