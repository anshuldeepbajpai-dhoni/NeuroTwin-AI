from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.exceptions import InvalidCredentialsException


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise InvalidCredentialsException(
            "Invalid email or password"
        )

    if not verify_password(
        password,
        user.password_hash
    ):
        raise InvalidCredentialsException(
            "Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": user.email,
            "id": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }