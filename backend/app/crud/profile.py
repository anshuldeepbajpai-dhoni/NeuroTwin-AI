from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.profile import (
    ProfileUpdate,
    AvatarUpdate,
)
import os
import shutil
from uuid import uuid4

from fastapi import UploadFile

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
    avatar: UploadFile
):

    user = (
        db.query(User)
        .filter(User.id == current_user.id)
        .first()
    )

    extension = avatar.filename.split(".")[-1]

    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(
        "uploads",
        "avatars",
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            avatar.file,
            buffer
        )

    user.avatar_url = f"/uploads/avatars/{filename}"

    db.commit()
    db.refresh(user)

    return {
        "message": "Avatar uploaded successfully",
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