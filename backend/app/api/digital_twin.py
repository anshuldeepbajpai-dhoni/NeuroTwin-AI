from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.digital_twin import (
    DigitalTwinCreate,
    DigitalTwinUpdate,
    DigitalTwinResponse
)

from app.crud.digital_twin import (
    create_digital_twin,
    get_digital_twin,
    update_digital_twin,
    delete_digital_twin
)

from app.exceptions import (
    DigitalTwinAlreadyExistsException,
    DigitalTwinNotFoundException,
    EmptyUpdateException,
)

router = APIRouter(
    prefix="/digital-twin",
    tags=["Digital Twin"]
)

@router.post(
    "/",
    response_model=DigitalTwinResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Digital Twin",
    description="Create a Digital Twin for the authenticated user.",
    responses={
        201: {
            "description": "Digital Twin created successfully."
        },
        401: {
            "description": "User is not authenticated."
        },
        409: {
            "description": "Digital Twin already exists."
        }
    }
)

def create_twin(
    twin: DigitalTwinCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_digital_twin(
            db,
            current_user,
            twin
        )

    except DigitalTwinAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=DigitalTwinResponse,
    summary="Get Digital Twin",
    description="Retrieve the authenticated user's Digital Twin.",
    responses={
        200: {
            "description": "Digital Twin retrieved successfully."
        },
        401: {
            "description": "User is not authenticated."
        },
        404: {
            "description": "Digital Twin not found."
        }
    }
)

def get_twin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_digital_twin(
            db,
            current_user
        )

    except DigitalTwinNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/",
    response_model=DigitalTwinResponse,
    summary="Update Digital Twin",
    description="Update the authenticated user's Digital Twin.",
    responses={
        200: {
            "description": "Digital Twin updated successfully."
        },
        400: {
            "description": "No fields provided for update."
        },
        401: {
            "description": "User is not authenticated."
        },
        404: {
            "description": "Digital Twin not found."
        }
    }
)

def update_twin(
    twin: DigitalTwinUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_digital_twin(
            db,
            current_user,
            twin
        )

    except EmptyUpdateException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except DigitalTwinNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/",
    summary="Delete Digital Twin",
    description="Delete the authenticated user's Digital Twin.",
    responses={
        200: {
            "description": "Digital Twin deleted successfully."
        },
        401: {
            "description": "User is not authenticated."
        },
        404: {
            "description": "Digital Twin not found."
        }
    }
)

def delete_twin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return delete_digital_twin(
            db,
            current_user
        )

    except DigitalTwinNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )