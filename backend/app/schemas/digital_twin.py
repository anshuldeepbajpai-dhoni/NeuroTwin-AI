from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class DigitalTwinBase(BaseModel):

    twin_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Name of your Digital Twin.",
        example="Anshul AI"
    )

    personality: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Describe the personality of your Digital Twin.",
        example="Friendly, analytical and curious."
    )

    communication_style: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Preferred communication style.",
        example="Professional"
    )

    goals: str = Field(
        ...,
        min_length=10,
        max_length=3000,
        description="Primary goals of the Digital Twin.",
        example="Help users solve AI and software engineering problems."
    )

    interests: str = Field(
        ...,
        min_length=3,
        max_length=3000,
        description="Topics the Digital Twin is interested in.",
        example="Artificial Intelligence, Machine Learning, Python, Data Science"
    )


class DigitalTwinCreate(DigitalTwinBase):

    model_config = ConfigDict(
        title="Create Digital Twin",
        json_schema_extra={
            "example": {
                "twin_name": "Anshul AI",
                "personality": "Friendly, analytical and curious.",
                "communication_style": "Professional",
                "goals": "Help users solve AI and software engineering problems.",
                "interests": "Artificial Intelligence, Machine Learning, Python, Data Science"
            }
        }
    )


class DigitalTwinUpdate(BaseModel):

    twin_name: Optional[str] = Field(
        default=None,
        description="Updated Digital Twin name."
    )

    personality: Optional[str] = Field(
        default=None,
        description="Updated personality."
    )

    communication_style: Optional[str] = Field(
        default=None,
        description="Updated communication style."
    )

    goals: Optional[str] = Field(
        default=None,
        description="Updated goals."
    )

    interests: Optional[str] = Field(
        default=None,
        description="Updated interests."
    )

    model_config = ConfigDict(
        title="Update Digital Twin",
        json_schema_extra={
            "example": {
                "communication_style": "Casual"
            }
        }
    )


class DigitalTwinResponse(DigitalTwinBase):

    id: str = Field(
        description="Unique Digital Twin ID."
    )

    user_id: str = Field(
        description="Owner user ID."
    )

    created_at: datetime = Field(
        description="Timestamp when the Digital Twin was created."
    )

    updated_at: datetime = Field(
        description="Timestamp when the Digital Twin was last updated."
    )

    model_config = ConfigDict(
        from_attributes=True,
        title="Digital Twin Response"
    )