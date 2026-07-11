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
