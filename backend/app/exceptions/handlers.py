from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    ForbiddenException,
    NotFoundException,
)

from app.exceptions.conversation import (
    ConversationNotFoundException,
    EmptyConversationUpdateException,
)

from app.exceptions.message import (
    InvalidMessageRoleException,
    MessageNotFoundException,
)

from app.exceptions.ai import (
    AIAuthenticationException,
    AIConfigurationException,
    AIConnectionException,
    AIQuotaExceededException,
    AIRateLimitException,
    AIResponseException,
    AITimeoutException,
)


async def conversation_not_found_handler(
    request,
    exc: ConversationNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message
        },
    )


async def empty_conversation_update_handler(
    request,
    exc: EmptyConversationUpdateException,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.message
        },
    )

async def message_not_found_handler(
    request,
    exc: MessageNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message
        },
    )


async def invalid_message_role_handler(
    request,
    exc: InvalidMessageRoleException,
):
    return JSONResponse(
        status_code=403,
        content={
            "detail": exc.message
        },
    )

async def ai_configuration_handler(
    request,
    exc: AIConfigurationException,
):
    return JSONResponse(
        status_code=503,
        content={
            "detail": exc.message
        },
    )


async def ai_authentication_handler(
    request,
    exc: AIAuthenticationException,
):
    return JSONResponse(
        status_code=502,
        content={
            "detail": exc.message
        },
    )


async def ai_quota_exceeded_handler(
    request,
    exc: AIQuotaExceededException,
):
    return JSONResponse(
        status_code=503,
        content={
            "detail": exc.message
        },
    )


async def ai_rate_limit_handler(
    request,
    exc: AIRateLimitException,
):
    return JSONResponse(
        status_code=429,
        content={
            "detail": exc.message
        },
    )


async def ai_timeout_handler(
    request,
    exc: AITimeoutException,
):
    return JSONResponse(
        status_code=504,
        content={
            "detail": exc.message
        },
    )


async def ai_connection_handler(
    request,
    exc: AIConnectionException,
):
    return JSONResponse(
        status_code=503,
        content={
            "detail": exc.message
        },
    )


async def ai_response_handler(
    request,
    exc: AIResponseException,
):
    return JSONResponse(
        status_code=502,
        content={
            "detail": exc.message
        },
    )

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UserAlreadyExistsException)
    async def user_exists_handler(
        request: Request,
        exc: UserAlreadyExistsException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message
            },
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.message
            },
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(
        request: Request,
        exc: ForbiddenException
    ):
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "message": exc.message
            },
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(
        request: Request,
        exc: NotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation Error",
                "errors": exc.errors()
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error"
            },
        )
    
    app.add_exception_handler(
        ConversationNotFoundException,
        conversation_not_found_handler,
    )

    app.add_exception_handler(
        EmptyConversationUpdateException,
        empty_conversation_update_handler,
    )
    
    app.add_exception_handler(
        MessageNotFoundException,
        message_not_found_handler,
    )

    app.add_exception_handler(
        InvalidMessageRoleException,
        invalid_message_role_handler,
    )

    app.add_exception_handler(
        AIConfigurationException,
        ai_configuration_handler,
    )

    app.add_exception_handler(
        AIAuthenticationException,
        ai_authentication_handler,
    )

    app.add_exception_handler(
        AIQuotaExceededException,
        ai_quota_exceeded_handler,
    )

    app.add_exception_handler(
        AIRateLimitException,
        ai_rate_limit_handler,
    )

    app.add_exception_handler(
        AITimeoutException,
        ai_timeout_handler,
    )

    app.add_exception_handler(
        AIConnectionException,
        ai_connection_handler,
    )

    app.add_exception_handler(
        AIResponseException,
        ai_response_handler,
    )