from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.logger import logger
from sqlalchemy import text

from backend.app.database.database import engine
from backend.app.core.logger import logger

from backend.app.database.base import Base
from backend.app.database.database import engine
from backend.app.schemas import UserCreate
from backend.app.models import User
from backend.app.api.users import router as user_router

# Log application startup
logger.info("Starting NeuroTwin AI Backend...")

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)
app.include_router(user_router)
Base.metadata.create_all(bind=engine)

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


@app.post("/schema-test")
def schema_test(user: UserCreate):

    return {
        "message": "Schema validation successful",
        "data": user
    }