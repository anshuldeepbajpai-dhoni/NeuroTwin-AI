from sqlalchemy.orm import Session

from app.models.user import User
from app.models.digital_twin import DigitalTwin

from app.schemas.digital_twin import (
    DigitalTwinCreate,
    DigitalTwinUpdate
)

from app.exceptions import (
    DigitalTwinAlreadyExistsException,
    DigitalTwinNotFoundException,
    EmptyUpdateException,
)


def create_digital_twin(
    db: Session,
    current_user: User,
    twin: DigitalTwinCreate
):

    existing = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.user_id == current_user.id
        )
        .first()
    )

    if existing:
        raise DigitalTwinAlreadyExistsException(
            "Digital Twin already exists."
        )

    digital_twin = DigitalTwin(
        user_id=current_user.id,
        twin_name=twin.twin_name,
        personality=twin.personality,
        communication_style=twin.communication_style,
        goals=twin.goals,
        interests=twin.interests
    )

    db.add(digital_twin)
    db.commit()
    db.refresh(digital_twin)

    return digital_twin


def get_digital_twin(
    db: Session,
    current_user: User
):

    twin = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.user_id == current_user.id
        )
        .first()
    )

    if not twin:
        raise DigitalTwinNotFoundException(
            "Digital Twin not found."
        )

    return twin


def update_digital_twin(
    db: Session,
    current_user: User,
    twin_update: DigitalTwinUpdate
):

    twin = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.user_id == current_user.id
        )
        .first()
    )

    if not twin:
        raise DigitalTwinNotFoundException(
            "Digital Twin not found."
        )

    update_data = twin_update.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise EmptyUpdateException(
            "No fields provided for update."
        )

    for key, value in update_data.items():
        setattr(
            twin,
            key,
            value
        )

    db.commit()
    db.refresh(twin)

    return twin


def delete_digital_twin(
    db: Session,
    current_user: User
):

    twin = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.user_id == current_user.id
        )
        .first()
    )

    if not twin:
        raise DigitalTwinNotFoundException(
            "Digital Twin not found."
        )

    db.delete(twin)
    db.commit()

    return {
        "message": "Digital Twin deleted successfully."
    }