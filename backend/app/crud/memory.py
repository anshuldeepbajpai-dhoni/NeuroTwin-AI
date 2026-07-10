from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions import (
    DigitalTwinNotFoundException,
    EmptyMemoryUpdateException,
    MemoryNotFoundException,
)
from app.models.digital_twin import DigitalTwin
from app.models.memory import Memory
from app.models.user import User
from app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
)


def create_memory(
    db: Session,
    current_user: User,
    memory: MemoryCreate,
):
    twin = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.user_id == current_user.id
        )
        .first()
    )

    if not twin:
        raise DigitalTwinNotFoundException(
            "Digital Twin not found."
        )

    new_memory = Memory(
        user_id=current_user.id,
        digital_twin_id=twin.id,
        title=memory.title,
        content=memory.content,
        category=memory.category,
        importance=memory.importance,
        is_favorite=memory.is_favorite,
    )

    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)

    return new_memory

def get_memories(
    db: Session,
    current_user: User,
    search: Optional[str] = None,
    category: Optional[str] = None,
    importance: Optional[int] = None,
    is_favorite: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    query = (
        db.query(Memory)
        .filter(
            Memory.user_id == current_user.id
        )
    )

    if search:
        search_value = f"%{search.strip()}%"

        query = query.filter(
            or_(
                Memory.title.ilike(search_value),
                Memory.content.ilike(search_value),
            )
        )

    if category:
        query = query.filter(
            Memory.category.ilike(
                category.strip()
            )
        )

    if importance is not None:
        query = query.filter(
            Memory.importance == importance
        )

    if is_favorite is not None:
        query = query.filter(
            Memory.is_favorite == is_favorite
        )

    total = query.count()

    sort_columns = {
        "created_at": Memory.created_at,
        "updated_at": Memory.updated_at,
        "title": Memory.title,
        "category": Memory.category,
        "importance": Memory.importance,
    }

    sort_column = sort_columns.get(
        sort_by,
        Memory.created_at,
    )

    if sort_order == "asc":
        query = query.order_by(
            sort_column.asc()
        )

    else:
        query = query.order_by(
            sort_column.desc()
        )

    offset = (
        page - 1
    ) * page_size

    items = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total_pages = (
        total + page_size - 1
    ) // page_size

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }

def get_memory(
    db: Session,
    current_user: User,
    memory_id: str,
):
    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == current_user.id,
        )
        .first()
    )

    if not memory:
        raise MemoryNotFoundException(
            "Memory not found."
        )

    return memory


def update_memory(
    db: Session,
    current_user: User,
    memory_id: str,
    memory_update: MemoryUpdate,
):
    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == current_user.id,
        )
        .first()
    )

    if not memory:
        raise MemoryNotFoundException(
            "Memory not found."
        )

    update_data = memory_update.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise EmptyMemoryUpdateException(
            "No fields provided for update."
        )

    for key, value in update_data.items():
        setattr(
            memory,
            key,
            value,
        )

    db.commit()
    db.refresh(memory)

    return memory


def delete_memory(
    db: Session,
    current_user: User,
    memory_id: str,
):
    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == current_user.id,
        )
        .first()
    )

    if not memory:
        raise MemoryNotFoundException(
            "Memory not found."
        )

    db.delete(memory)
    db.commit()

    return {
        "message": "Memory deleted successfully."
    }