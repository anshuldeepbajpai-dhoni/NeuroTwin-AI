from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class ProfileResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    avatar_url: Optional[str] = None
    timezone: str
    language: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class ProfileUpdate(BaseModel):
    phone: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    timezone: Optional[str] = None
    language: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone": "+919876543210",
                "bio": "AI & ML Enthusiast",
                "date_of_birth": "2003-05-15",
                "timezone": "Asia/Kolkata",
                "language": "English"
            }
        }
    )


class AvatarUpdate(BaseModel):
    avatar_url: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "avatar_url": "https://example.com/avatar.png"
            }
        }
    )


class AvatarResponse(BaseModel):
    message: str
    avatar_url: str