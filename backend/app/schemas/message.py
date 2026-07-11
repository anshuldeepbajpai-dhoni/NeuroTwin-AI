from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


MessageRole = Literal[
    "user",
    "assistant",
    "system",
]


class MessageBase(BaseModel):

    role: MessageRole = Field(
        json_schema_extra={
            "example": "user"
        },
    )

    content: str = Field(
        min_length=1,
        max_length=10000,
        json_schema_extra={
            "example": (
                "How can I learn FastAPI?"
            )
        },
    )


class MessageCreate(MessageBase):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "user",
                "content": (
                    "How can I learn FastAPI?"
                ),
            }
        }
    )


class MessageResponse(MessageBase):

    id: str

    conversation_id: str

    user_id: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class PaginatedMessageResponse(BaseModel):

    items: list[MessageResponse]

    total: int = Field(
        ge=0,
        json_schema_extra={
            "example": 25
        },
    )

    page: int = Field(
        ge=1,
        json_schema_extra={
            "example": 1
        },
    )

    page_size: int = Field(
        ge=1,
        le=100,
        json_schema_extra={
            "example": 10
        },
    )

    total_pages: int = Field(
        ge=0,
        json_schema_extra={
            "example": 3
        },
    )