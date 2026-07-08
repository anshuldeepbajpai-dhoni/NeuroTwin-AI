from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic import BaseModel
from pydantic import EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer"
            }
        }
    )


class TokenData(BaseModel):
    email: str | None = None


class CurrentUser(BaseModel):
    id: str
    username: str
    email: EmailStr

class CurrentUserResponse(BaseModel):

    id: str

    username: str

    email: EmailStr

    is_active: bool