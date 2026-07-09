import uuid

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class DigitalTwin(Base):

    __tablename__ = "digital_twins"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    twin_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    personality: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    communication_style: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    goals: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    interests: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="digital_twin"
    )

    memories = relationship(
    "Memory",
    back_populates="digital_twin",
    cascade="all, delete-orphan"
    )