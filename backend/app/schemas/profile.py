from datetime import date
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    field_validator,
)


class ProfileResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    avatar_url: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class ProfileUpdate(BaseModel):

    phone: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15
    )

    bio: Optional[str] = Field(
        default=None,
        max_length=500
    )

    date_of_birth: Optional[date] = None

    timezone: Optional[str] = None

    language: Optional[
        Literal[
            "English",
            "Hindi",
            "Spanish",
            "French",
            "German"
        ]
    ] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone": "+919876543210",
                "bio": "AI Engineer",
                "date_of_birth": "2003-05-15",
                "timezone": "Asia/Kolkata",
                "language": "English"
            }
        }
    )

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if value is None:
            return value

        value = value.replace(" ", "")

        if value.startswith("+"):
            digits = value[1:]
        else:
            digits = value

        if not digits.isdigit():
            raise ValueError(
                "Phone number must contain only digits."
            )

        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value):

        if value is None:
            return value

        if value > date.today():
            raise ValueError(
                "Date of birth cannot be in the future."
            )

        return value


class AvatarUpdate(BaseModel):

    avatar_url: HttpUrl

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