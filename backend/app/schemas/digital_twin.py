from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class DigitalTwinBase(BaseModel):

    twin_name: str = Field(
        min_length=3,
        max_length=100
    )

    personality: str = Field(
        min_length=10,
        max_length=2000
    )

    communication_style: str = Field(
        min_length=3,
        max_length=100
    )

    goals: str = Field(
        min_length=10,
        max_length=3000
    )

    interests: str = Field(
        min_length=3,
        max_length=3000
    )


class DigitalTwinCreate(DigitalTwinBase):

    model_config = ConfigDict(
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

    twin_name: Optional[str] = None
    personality: Optional[str] = None
    communication_style: Optional[str] = None
    goals: Optional[str] = None
    interests: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "communication_style": "Casual"
            }
        }
    )


class DigitalTwinResponse(DigitalTwinBase):

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )