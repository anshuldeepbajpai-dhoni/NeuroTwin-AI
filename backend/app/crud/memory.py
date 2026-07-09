from sqlalchemy.orm import Session

from app.models.user import User
from app.models.memory import Memory
from app.models.digital_twin import DigitalTwin

from app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
)

def create_memory(
    db: Session,
    current_user: User,
    memory: MemoryCreate
):
    twin = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.user_id == current_user.id
        )
        .first()
    )

    if not twin:
        raise ValueError(
            "Digital Twin not found."
        )

    new_memory = Memory(
        user_id=current_user.id,
        digital_twin_id=twin.id,
        title=memory.title,
        content=memory.content,
        category=memory.category,
        importance=memory.importance,
        is_favorite=memory.is_favorite
    )

    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)

    return new_memory


def get_memories(
    db: Session,
    current_user: User
):
    return (
        db.query(Memory)
        .filter(
            Memory.user_id == current_user.id
        )
        .order_by(
            Memory.created_at.desc()
        )
        .all()
    )

def get_memory(
    db: Session,
    current_user: User,
    memory_id: str
):
    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == current_user.id
        )
        .first()
    )

    if not memory:
        raise ValueError(
            "Memory not found."
        )

    return memory

def update_memory(
    db: Session,
    current_user: User,
    memory_id: str,
    memory_update: MemoryUpdate
):
    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == current_user.id
        )
        .first()
    )

    if not memory:
        raise ValueError(
            "Memory not found."
        )

    update_data = memory_update.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise ValueError(
            "No fields provided for update."
        )

    for key, value in update_data.items():
        setattr(
            memory,
            key,
            value
        )

    db.commit()
    db.refresh(memory)

    return memory

def delete_memory(
    db: Session,
    current_user: User,
    memory_id: str
):
    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == current_user.id
        )
        .first()
    )

    if not memory:
        raise ValueError(
            "Memory not found."
        )

    db.delete(memory)
    db.commit()

    return {
        "message": "Memory deleted successfully."
    }