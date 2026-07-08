from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import logger
from sqlalchemy import text
from app.schemas.auth import LoginRequest
from app.database.database import engine
from app.core.logger import logger
from app.core.security import create_access_token
from app.database.base import Base
from app.database.database import engine
from app.schemas import UserCreate
from app.models import User
from app.core.config import settings
from app.crud.auth import authenticate_user
from app.schemas.auth import LoginRequest
from app.database.session import get_db

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException
from app.api.auth import router as auth_router
from app.exceptions import register_exception_handlers

# Log application startup
logger.info("Starting NeuroTwin AI Backend...")

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
register_exception_handlers(app)

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


@app.get("/", tags=["Home"])
def root():
    logger.info("Root endpoint accessed")

    return {
        "project": settings.app_name,
        "version": settings.app_version,
        "status": "Running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Health"])
def health():
    logger.info("Health endpoint accessed")

    return {
        "status": "Healthy",
        "message": "Backend is running successfully"
    }


@app.get("/version", tags=["Version"])
def version():
    logger.info("Version endpoint accessed")

    return {
        "project": settings.app_name,
        "version": settings.app_version
    }

@app.get("/db-check")
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

@app.get("/error")
def error():
    try:
        x = 10 / 0
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return {
            "error": str(e)
        }
    
@app.get("/tables")
def tables():

    return {
        "tables": [
            "users"
        ]
    }
