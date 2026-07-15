# ======================================================
# Standard Library
# ======================================================

import os


# ======================================================
# Third-Party Libraries
# ======================================================

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from fastapi.staticfiles import StaticFiles

from sqlalchemy import text


# ======================================================
# Local Application Imports
# ======================================================

from app.api.ai_chat import (
    router as ai_chat_router,
)
from app.api.auth import (
    router as auth_router,
)
from app.api.conversation import (
    router as conversation_router,
)
from app.api.digital_twin import (
    router as digital_twin_router,
)
from app.api.memory import (
    router as memory_router,
)
from app.api.message import (
    router as message_router,
)
from app.api.profile import (
    router as profile_router,
)

from app.core.config import settings
from app.core.logger import logger

from app.database.database import engine

from app.exceptions import (
    register_exception_handlers,
)
from app.api.health import (
    router as health_router,
)
from app.middleware.request_logging import (
    RequestLoggingMiddleware,
)
from starlette.middleware.httpsredirect import (
    HTTPSRedirectMiddleware,
)
from starlette.middleware.trustedhost import (
    TrustedHostMiddleware,
)

from app.middleware.security_headers import (
    SecurityHeadersMiddleware,
)

# ======================================================
# Application Startup
# ======================================================

logger.info(
    "Starting NeuroTwin AI Backend..."
)


# ======================================================
# OpenAPI Tags
# ======================================================

tags_metadata = [
    {
        "name": "Authentication",
        "description": (
            "Authentication APIs including "
            "registration, login, JWT, and RBAC."
        ),
    },
    {
        "name": "Users",
        "description": (
            "User management APIs."
        ),
    },
    {
        "name": "Profile",
        "description": (
            "User profile management APIs."
        ),
    },
    {
        "name": "Digital Twin",
        "description": (
            "Digital Twin management APIs."
        ),
    },
    {
        "name": "Memories",
        "description": (
            "Long-term memory management APIs."
        ),
    },
    {
        "name": "Conversations",
        "description": (
            "Conversation management APIs."
        ),
    },
    {
        "name": "Messages",
        "description": (
            "Conversation message APIs."
        ),
    },
    {
        "name": "AI Chat",
        "description": (
            "Personalized Digital Twin "
            "AI chat APIs."
        ),
    },
]


# ======================================================
# FastAPI Application
# ======================================================

app = FastAPI(
    title="NeuroTwin AI Backend API",
    version="1.0.0",
    summary=(
        "Enterprise-grade backend "
        "for NeuroTwin AI."
    ),
    description="""
# NeuroTwin AI Backend

A personalized AI Digital Twin backend
built using **FastAPI**.

## Features

- JWT Authentication
- Role-Based Access Control
- User Profile Management
- Avatar Upload
- Digital Twin Management
- Long-Term Memory Management
- Conversation Management
- Message Management
- Personalized AI Chat
- OpenAI Integration
- Ollama Local Fallback
- Automatic Memory Extraction
- Conversation Summarization
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Migrations
- Swagger Documentation
- Pytest Testing

## Authentication

Use **Authorize** with a valid JWT token.

Protected endpoints require:

`Authorization: Bearer <access_token>`

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



# ======================================================
# Exception Handlers
# ======================================================

register_exception_handlers(
    app
)


# ======================================================
# API Routers
# ======================================================
app.include_router(
    health_router
)

app.include_router(
    auth_router
)

app.include_router(
    profile_router
)

app.include_router(
    digital_twin_router
)

app.include_router(
    memory_router
)

app.include_router(
    conversation_router
)

app.include_router(
    message_router
)

app.include_router(
    ai_chat_router
)

# ======================================================
# Production Security Configuration
# ======================================================

allowed_hosts = [
    host.strip()
    for host in (
        settings.allowed_hosts.split(
            ","
        )
    )
    if host.strip()
]

cors_origins = [
    origin.strip()
    for origin in (
        settings.cors_origins.split(
            ","
        )
    )
    if origin.strip()
]


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Request-ID",
    ],
    expose_headers=[
        "X-Request-ID",
        "X-Process-Time-MS",
    ],
)


app.add_middleware(
    SecurityHeadersMiddleware
)


if settings.enable_https_redirect:

    app.add_middleware(
        HTTPSRedirectMiddleware
    )

# ======================================================
# CORS Configuration
# ======================================================

app.add_middleware(
    RequestLoggingMiddleware
)

# ======================================================
# Static File Configuration
# ======================================================

os.makedirs(
    "uploads/avatars",
    exist_ok=True,
)

app.mount(
    "/uploads",
    StaticFiles(
        directory="uploads"
    ),
    name="uploads",
)


# ======================================================
# Core API Endpoints
# ======================================================

@app.get(
    "/",
    tags=["Home"],
    summary="API Home",
)
def root():

    logger.info(
        "Root endpoint accessed"
    )

    return {
        "project": settings.app_name,
        "version": settings.app_version,
        "status": "Running",
        "docs": "/docs",
        "health": "/health",
    }



@app.get(
    "/version",
    tags=["Version"],
    summary="Application Version",
)
def version():

    logger.info(
        "Version endpoint accessed"
    )

    return {
        "project": settings.app_name,
        "version": settings.app_version,
    }


@app.get(
    "/db-check",
    include_in_schema=False,
)
def database_check():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        logger.info(
            "Database connection successful"
        )

        return {
            "database": "Connected",
            "status": "Success",
        }

    except Exception as error:

        logger.exception(
            "Database connection failed"
        )

        return {
            "database": "Disconnected",
            "error": str(error),
        }


@app.get(
    "/error",
    include_in_schema=False,
)
def error():

    try:

        result = 10 / 0

        return {
            "result": result
        }

    except Exception as error:

        logger.exception(
            "An unexpected error occurred"
        )

        return {
            "error": str(error)
        }


@app.get(
    "/tables",
    include_in_schema=False,
)
def tables():

    return {
        "tables": [
            "users",
            "digital_twins",
            "memories",
            "conversations",
            "messages",
        ]
    }