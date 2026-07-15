from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.responses import (
    JSONResponse,
)
from sqlalchemy.orm import Session

from app.database.session import (
    get_db,
)
from app.services.health import (
    health_service,
)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    summary="Application Health",
    description=(
        "Verify that the NeuroTwin "
        "backend application is running."
    ),
)
def application_health():
    """
    Return the general application
    health status.
    """

    return {
        "status": "healthy",
        "application": "running",
    }


@router.get(
    "/liveness",
    summary="Application Liveness",
    description=(
        "Verify that the backend process "
        "is alive and accepting requests."
    ),
)
def application_liveness():
    """
    Return the application process
    liveness status.
    """

    return {
        "status": "alive",
    }


@router.get(
    "/readiness",
    summary="Application Readiness",
    description=(
        "Verify that the application and "
        "database are ready to serve "
        "requests."
    ),
)
def application_readiness(
    db: Session = Depends(
        get_db
    ),
):
    """
    Return application and database
    readiness information.
    """

    database_ready = (
        health_service.check_database(
            db=db
        )
    )

    if not database_ready:

        return JSONResponse(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            content={
                "status": "not_ready",
                "application": "healthy",
                "database": "disconnected",
            },
        )

    return {
        "status": "ready",
        "application": "healthy",
        "database": "connected",
    }