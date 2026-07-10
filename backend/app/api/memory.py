from typing import Literal
from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from sqlalchemy.orm import Session

from app.crud.memory import (
    create_memory,
    delete_memory,
    get_memories,
    get_memory,
    update_memory,
)
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.memory import (
    MemoryCreate,
    MemoryResponse,
    MemoryUpdate,
    PaginatedMemoryResponse,
)

from app.exceptions import (
    DigitalTwinNotFoundException,
    EmptyMemoryUpdateException,
    MemoryNotFoundException,
)


router = APIRouter(
    prefix="/memories",
    tags=["Memories"],
)


@router.post(
    "/",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Memory",
    description=(
        "Create a new memory for the authenticated user's "
        "Digital Twin."
    ),
    responses={
        201: {
            "description": "Memory created successfully."
        },
        401: {
            "description": "Authentication is required."
        },
        404: {
            "description": "Digital Twin not found."
        },
        422: {
            "description": "Request validation failed."
        },
    },
)


def create(
    memory: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_memory(
            db=db,
            current_user=current_user,
            memory=memory,
        )

    except DigitalTwinNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.get(
    "/",
    response_model=PaginatedMemoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Memories",
    description=(
        "Retrieve all memories belonging to the "
        "authenticated user."
    ),
    responses={
        200: {
            "description": "Memories retrieved successfully."
        },
        401: {
            "description": "Authentication is required."
        },
    },
)

def get_all(
    search: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=200,
        description=(
            "Search memories by title or content."
        ),
    ),
    category: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=100,
        description=(
            "Filter memories by category."
        ),
    ),
    importance: Optional[int] = Query(
        default=None,
        ge=1,
        le=5,
        description=(
            "Filter memories by importance level."
        ),
    ),
    is_favorite: Optional[bool] = Query(
        default=None,
        description=(
            "Filter favorite or non-favorite memories."
        ),
    ),
    page: int = Query(
        default=1,
        ge=1,
        description=(
            "Page number. Pagination starts from page 1."
        ),
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description=(
            "Number of memories returned per page."
        ),
    ),
    sort_by: Literal[
        "created_at",
        "updated_at",
        "title",
        "category",
        "importance",
    ] = Query(
        default="created_at",
        description=(
            "Memory field used for sorting."
        ),
    ),
    sort_order: Literal[
        "asc",
        "desc",
    ] = Query(
        default="desc",
        description=(
            "Sort results in ascending or descending order."
        ),
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_memories(
        db=db,
        current_user=current_user,
        search=search,
        category=category,
        importance=importance,
        is_favorite=is_favorite,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )

@router.get(
    "/{memory_id}",
    response_model=MemoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Memory",
    description=(
        "Retrieve one memory by its ID. The authenticated "
        "user can access only their own memory."
    ),
    responses={
        200: {
            "description": "Memory retrieved successfully."
        },
        401: {
            "description": "Authentication is required."
        },
        404: {
            "description": "Memory not found."
        },
    },
)
def get_one(
    memory_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_memory(
            db=db,
            current_user=current_user,
            memory_id=memory_id,
        )

    except MemoryNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.put(
    "/{memory_id}",
    response_model=MemoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Memory",
    description=(
        "Update one or more fields of a memory belonging "
        "to the authenticated user."
    ),
    responses={
        200: {
            "description": "Memory updated successfully."
        },
        400: {
            "description": "No fields were provided for update."
        },
        401: {
            "description": "Authentication is required."
        },
        404: {
            "description": "Memory not found."
        },
        422: {
            "description": "Request validation failed."
        },
    },
)
def update(
    memory_id: str,
    memory_update: MemoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_memory(
            db=db,
            current_user=current_user,
            memory_id=memory_id,
            memory_update=memory_update,
        )

    except MemoryNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except EmptyMemoryUpdateException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.delete(
    "/{memory_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Memory",
    description=(
        "Permanently delete a memory belonging to the "
        "authenticated user."
    ),
    responses={
        200: {
            "description": "Memory deleted successfully."
        },
        401: {
            "description": "Authentication is required."
        },
        404: {
            "description": "Memory not found."
        },
    },
)
def delete(
    memory_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return delete_memory(
            db=db,
            current_user=current_user,
            memory_id=memory_id,
        )

    except MemoryNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error