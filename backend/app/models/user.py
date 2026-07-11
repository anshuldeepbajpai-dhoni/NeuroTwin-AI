import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy import Text
from sqlalchemy import Date
from app.database.base import Base
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    phone = Column(
    String(20),
    nullable=True
    )

    bio = Column(
        Text,
        nullable=True
    )

    date_of_birth = Column(
        Date,
        nullable=True
    )

    avatar_url = Column(
        String(255),
        nullable=True
    )

    timezone = Column(
        String(50),
        default="UTC"
    )

    language = Column(
        String(30),
        default="English"
    )

    role = Column(
        String(20),
        default="user",
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )

    digital_twin = relationship(
        "DigitalTwin",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
    )

    memories = relationship(
        "Memory",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    messages = relationship(
        "Message",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )