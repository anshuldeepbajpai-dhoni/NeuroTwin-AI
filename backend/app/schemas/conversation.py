from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ConversationBase(BaseModel):

    title: str = Field(
        min_length=3,
        max_length=200,
        json_schema_extra={
            "example": "Python Learning Discussion"
        },
    )


class ConversationCreate(ConversationBase):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Python Learning Discussion"
            }
        }
    )


class ConversationUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=200,
        json_schema_extra={
            "example": "Advanced FastAPI Discussion"
        },
    )

    is_archived: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "example": False
        },
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Advanced FastAPI Discussion",
                "is_archived": False
            }
        }
    )


class ConversationResponse(ConversationBase):

    id: str

    user_id: str

    digital_twin_id: str

    is_archived: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class PaginatedConversationResponse(BaseModel):

    items: list[ConversationResponse]

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