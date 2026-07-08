from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.auth import require_admin

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse
)

from app.schemas.auth import (
    Token,
    CurrentUserResponse,
)

from app.crud.user import create_user
from app.crud.auth import authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register User",
    description="Create a new user account.",
    response_description="User created successfully."
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)


@router.post(
    "/login",
    response_model=Token,
    summary="User Login",
    description="Authenticate user and return JWT access token.",
    response_description="JWT access token."
)

def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    summary="Current User",
    description="Returns details of the authenticated user."
) 

def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active
    }


@router.get(
    "/admin",
    summary="Admin Dashboard",
    description="Accessible only to users with the admin role."
)
def admin_dashboard(
    current_user: User = Depends(require_admin)
):
    return {
        "message": "Welcome Admin",
        "username": current_user.username
    }