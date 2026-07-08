from sqlalchemy.orm import Session

from backend.app.models.user import User

from backend.app.schemas.auth import LoginRequest

from backend.app.core.security import (
    verify_password,
    create_access_token,
)


def authenticate_user(
    db: Session,
    login_data: LoginRequest
):
    # Find user by email
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if not user:
        raise ValueError("Invalid email or password")

    # Verify password
    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise ValueError("Invalid email or password")

    # Generate JWT
    token = create_access_token(
        {
            "sub": user.email,
            "id": str(user.id)
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }