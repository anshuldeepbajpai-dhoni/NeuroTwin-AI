from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class MemoryBase(BaseModel):

    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Title of the memory.",
        example="Favorite Programming Language"
    )

    content: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        description="Detailed memory content.",
        example="The user enjoys working with Python and FastAPI."
    )

    category: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Category of the memory.",
        example="Programming"
    )

    importance: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Importance level (1-5)."
    )

    is_favorite: bool = Field(
        default=False,
        description="Marks whether this memory is a favorite."
    )


class MemoryCreate(MemoryBase):

    model_config = ConfigDict(
        title="Create Memory",
        json_schema_extra={
            "example": {
                "title": "Favorite Programming Language",
                "content": "The user enjoys working with Python and FastAPI.",
                "category": "Programming",
                "importance": 5,
                "is_favorite": True
            }
        }
    )


class MemoryUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=200
    )

    content: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=5000
    )

    category: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    importance: Optional[int] = Field(
        default=None,
        ge=1,
        le=5
    )

    is_favorite: Optional[bool] = None

    model_config = ConfigDict(
        title="Update Memory",
        json_schema_extra={
            "example": {
                "importance": 4,
                "is_favorite": True
            }
        }
    )


class MemoryResponse(MemoryBase):

    id: str

    user_id: str

    digital_twin_id: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        title="Memory Response"
    )

class PaginatedMemoryResponse(BaseModel):

    items: List[MemoryResponse]

    total: int = Field(
        ge=0,
        description="Total number of memories matching the filters."
    )

    page: int = Field(
        ge=1,
        description="Current page number."
    )

    page_size: int = Field(
        ge=1,
        description="Maximum number of memories per page."
    )

    total_pages: int = Field(
        ge=0,
        description="Total number of available pages."
    )

    model_config = ConfigDict(
        title="Paginated Memory Response",
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": "memory-id",
                        "user_id": "user-id",
                        "digital_twin_id": "digital-twin-id",
                        "title": "Python Development",
                        "content": (
                            "The user enjoys building APIs "
                            "with Python and FastAPI."
                        ),
                        "category": "Programming",
                        "importance": 5,
                        "is_favorite": True,
                        "created_at": (
                            "2026-07-10T10:00:00+00:00"
                        ),
                        "updated_at": (
                            "2026-07-10T10:00:00+00:00"
                        )
                    }
                ],
                "total": 1,
                "page": 1,
                "page_size": 10,
                "total_pages": 1
            }
        }
    )