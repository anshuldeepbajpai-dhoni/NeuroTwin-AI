from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.core.security import hash_password


def create_user(db: Session, user: UserCreate):

    if db.query(User).filter(User.email == user.email).first():
        raise ValueError("Email already registered")

    if db.query(User).filter(User.username == user.username).first():
        raise ValueError("Username already exists")

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user