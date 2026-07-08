from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.profile import (
    ProfileUpdate,
    AvatarUpdate,
)

def get_profile(
    db: Session,
    current_user: User
):
    return (
        db.query(User)
        .filter(User.id == current_user.id)
        .first()
    )

def update_profile(
    db: Session,
    current_user: User,
    profile: ProfileUpdate
):

    user = (
        db.query(User)
        .filter(User.id == current_user.id)
        .first()
    )

    update_data = profile.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            user,
            key,
            value
        )

    db.commit()
    db.refresh(user)

    return user

def update_avatar(
    db: Session,
    current_user: User,
    avatar: AvatarUpdate
):

    user = (
        db.query(User)
        .filter(User.id == current_user.id)
        .first()
    )

    user.avatar_url = str(avatar.avatar_url)

    db.commit()
    db.refresh(user)

    return {
        "message": "Avatar updated successfully",
        "avatar_url": user.avatar_url
    }

def delete_avatar(
    db: Session,
    current_user: User
):

    user = (
        db.query(User)
        .filter(User.id == current_user.id)
        .first()
    )

    user.avatar_url = None

    db.commit()

    return {
        "message": "Avatar removed successfully",
        "avatar_url": ""
    }