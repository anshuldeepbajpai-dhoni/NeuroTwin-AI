# ======================================================
# Standard Library
# ======================================================

import os


# ======================================================
# Third-Party Libraries
# ======================================================

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy import text
from sqlalchemy.orm import Session


# ======================================================
# Local Application Imports
# ======================================================

from app.api.auth import router as auth_router
from app.api.digital_twin import router as digital_twin_router
from app.api.profile import router as profile_router
from app.api.memory import router as memory_router

from app.core.config import settings
from app.core.logger import logger
from app.core.security import create_access_token

from app.crud.auth import authenticate_user

from app.database.base import Base
from app.database.database import engine
from app.database.session import get_db

from app.exceptions import register_exception_handlers

from app.models import User

from app.schemas import UserCreate
from app.schemas.auth import LoginRequest
from app.api.conversation import (
    router as conversation_router,
)
from app.api.message import (
    router as message_router,
)

# Log application startup
logger.info("Starting NeuroTwin AI Backend...")

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Authentication APIs (Register, Login, JWT, RBAC)"
    },
    {
        "name": "Users",
        "description": "User management APIs"
    }
]

app = FastAPI(
    title="NeuroTwin AI Backend API",
    version="1.0.0",
    summary="Enterprise-grade backend for NeuroTwin AI.",
    description="""
# NeuroTwin AI Backend

A production-ready backend built using **FastAPI**.

## Features

- JWT Authentication
- Role-Based Access Control (RBAC)
- User Profile Management
- Avatar Upload
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Migrations
- Swagger Documentation
- Pytest Testing

## Authentication

Use **Authorize** to log in using your email and password.

All protected endpoints require a valid JWT token.

## Developer

**Anshul Deep Bajpai**
""",
    contact={
        "name": "Anshul Deep Bajpai",
        "email": "anshul@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=tags_metadata,
)


Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
register_exception_handlers(app)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(digital_twin_router)
app.include_router(memory_router)
app.include_router(
    conversation_router
)
app.include_router(
    message_router
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads/avatars", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

@app.get(
    "/",
    tags=["Home"],
    summary="API Home",
    description="Returns basic information about the NeuroTwin AI Backend."
)
def root():
    logger.info("Root endpoint accessed")

    return {
        "project": settings.app_name,
        "version": settings.app_version,
        "status": "Running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Checks whether the backend service is running correctly."
)
def health():
    logger.info("Health endpoint accessed")

    return {
        "status": "Healthy",
        "message": "Backend is running successfully"
    }


@app.get(
    "/version",
    tags=["Version"],
    summary="Application Version",
    description="Returns the current backend version."
)
def version():
    logger.info("Version endpoint accessed")

    return {
        "project": settings.app_name,
        "version": settings.app_version
    }

@app.get(
    "/db-check",
    include_in_schema=False
)
def database_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("Database connection successful")

        return {
            "database": "Connected",
            "status": "Success"
        }

    except Exception as e:
        logger.exception("Database connection failed")

        return {
            "database": "Disconnected",
            "error": str(e)
        }

@app.get(
    "/error",
    include_in_schema=False
)
def error():
    try:
        x = 10 / 0
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return {
            "error": str(e)
        }
    
@app.get(
    "/tables",
    include_in_schema=False
)
def tables():

    return {
        "tables": [
            "users"
        ]
    }

