from typing import Literal

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.crud.conversation import (
    create_conversation,
    delete_conversation,
    get_conversation_by_id,
    get_conversations,
    update_conversation,
)
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationUpdate,
    PaginatedConversationResponse,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=201,
    summary="Create Conversation",
    description=(
        "Create a new Conversation for the "
        "authenticated user's Digital Twin."
    ),
)
def create(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return create_conversation(
        db=db,
        current_user=current_user,
        conversation_data=conversation_data,
    )


@router.get(
    "",
    response_model=PaginatedConversationResponse,
    summary="Get Conversations",
    description=(
        "Retrieve the authenticated user's "
        "Conversations with search, filtering, "
        "pagination, and sorting."
    ),
)
def list_conversations(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
        description=(
            "Search Conversations by title."
        ),
    ),
    is_archived: bool | None = Query(
        default=None,
        description=(
            "Filter by archived status."
        ),
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number.",
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description=(
            "Number of Conversations per page."
        ),
    ),
    sort_by: Literal[
        "created_at",
        "updated_at",
        "title",
    ] = Query(
        default="updated_at",
        description=(
            "Field used to sort Conversations."
        ),
    ),
    sort_order: Literal[
        "asc",
        "desc",
    ] = Query(
        default="desc",
        description=(
            "Conversation sorting direction."
        ),
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_conversations(
        db=db,
        current_user=current_user,
        search=search,
        is_archived=is_archived,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Get Conversation",
    description=(
        "Retrieve one Conversation owned by "
        "the authenticated user."
    ),
)
def get_one(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_conversation_by_id(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
    )


@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Update Conversation",
    description=(
        "Update the title or archived status "
        "of an owned Conversation."
    ),
)
def update(
    conversation_id: str,
    conversation_data: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return update_conversation(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
        conversation_data=conversation_data,
    )


@router.delete(
    "/{conversation_id}",
    summary="Delete Conversation",
    description=(
        "Permanently delete an owned Conversation "
        "and all Messages associated with it."
    ),
)
def remove(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return delete_conversation(
        db=db,
        current_user=current_user,
        conversation_id=conversation_id,
    )