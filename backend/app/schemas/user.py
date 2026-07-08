from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "anshul",
                "email": "anshul@gmail.com",
                "password": "Pass@123",
                "role": "user"
            }
        }
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)