from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdate,
    AvatarUpdate,
    AvatarResponse,
)

from app.crud.profile import (
    get_profile,
    update_profile,
    update_avatar,
    delete_avatar,
)
from fastapi import UploadFile
from fastapi import File

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/profile",
    response_model=ProfileResponse,
    summary="Get User Profile",
    description="Returns the profile of the currently authenticated user."
)
def profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_profile(db, current_user)


@router.put(
    "/profile",
    response_model=ProfileResponse,
    summary="Update User Profile",
    description="Update the profile information of the authenticated user."
)

@router.patch(
    "/profile/avatar",
    response_model=AvatarResponse,
    summary="Upload Profile Avatar",
    description="Upload or replace the authenticated user's profile picture."
)
def avatar(
    avatar: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    summary="Upload Avatar",
    description="Upload a profile picture for the authenticated user."
):
    return update_avatar(
        db,
        current_user,
        avatar
    )

def update(
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    summary="Update Profile",
    description="Update profile information such as phone, bio, timezone, and language."
):
    return update_profile(
        db,
        current_user,
        profile
    )



@router.delete(
    "/profile/avatar",
    response_model=AvatarResponse,
    summary="Delete Avatar",
    description="Remove the avatar of the authenticated user."
)
def remove_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_avatar(
        db,
        current_user
    )