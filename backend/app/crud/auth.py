from sqlalchemy.orm import Session

from backend.app.models.user import User

from backend.app.core.security import (
    verify_password,
    create_access_token
)


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
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

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