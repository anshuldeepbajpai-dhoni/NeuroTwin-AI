from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.user import UserCreate
from backend.app.schemas.user import UserResponse

from backend.app.crud.user import create_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        return create_user(db, user)

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )