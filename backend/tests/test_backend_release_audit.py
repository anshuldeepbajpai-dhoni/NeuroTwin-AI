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
from app.main import app


def get_router_routes(
    router,
):
    """
    Return all HTTP methods and paths
    registered in an API router.
    """

    registered_routes = set()

    for route in router.routes:

        methods = getattr(
            route,
            "methods",
            set(),
        )

        path = getattr(
            route,
            "path",
            "",
        )

        for method in methods:

            registered_routes.add(
                (
                    method,
                    path,
                )
            )

    return registered_routes


def has_route(
    router,
    method,
    path_keyword,
):
    """
    Check whether a router contains an
    endpoint with the required method
    and path keyword.
    """

    routes = get_router_routes(
        router
    )

    return any(
        (
            route_method == method
            and path_keyword.lower()
            in route_path.lower()
        )
        for (
            route_method,
            route_path,
        )
        in routes
    )


def test_application_metadata():
    """
    Verify essential application
    metadata.
    """

    assert (
        app.title
        == "NeuroTwin AI Backend API"
    )

    assert (
        app.version
        == "1.0.0"
    )

    assert (
        "NeuroTwin"
        in app.title
    )


def test_core_public_routes_are_registered():
    """
    Verify essential public routes.
    """

    application_routes = {
        (
            method,
            route.path,
        )
        for route in app.routes
        if hasattr(
            route,
            "methods",
        )
        for method in route.methods
    }

    required_routes = {
        (
            "GET",
            "/",
        ),
        (
            "GET",
            "/version",
        ),
        (
            "GET",
            "/openapi.json",
        ),
        (
            "GET",
            "/docs",
        ),
    }

    missing_routes = (
        required_routes
        - application_routes
    )

    assert not missing_routes, (
        "MISSING PUBLIC ROUTES: "
        f"{missing_routes}"
    )


def test_health_router_is_configured():
    """
    Verify application health,
    liveness, and readiness endpoints.
    """

    from app.api.health import (
        router as health_router,
    )

    health_routes = (
        get_router_routes(
            health_router
        )
    )

    assert (
        "GET",
        "/health",
    ) in health_routes

    assert (
        "GET",
        "/health/liveness",
    ) in health_routes

    assert (
        "GET",
        "/health/readiness",
    ) in health_routes
    

def test_authentication_router_is_configured():
    """
    Verify authentication endpoints.
    """

    routes = get_router_routes(
        auth_router
    )

    assert len(routes) >= 2

    assert has_route(
        router=auth_router,
        method="POST",
        path_keyword="register",
    )

    login_exists = (
        has_route(
            router=auth_router,
            method="POST",
            path_keyword="login",
        )
        or
        has_route(
            router=auth_router,
            method="POST",
            path_keyword="token",
        )
    )

    assert login_exists


def test_digital_twin_router_is_configured():
    """
    Verify Digital Twin endpoints.
    """

    routes = get_router_routes(
        digital_twin_router
    )

    assert len(routes) == 4

    assert any(
        method == "POST"
        for method, _ in routes
    )


def test_conversation_router_is_configured():
    """
    Verify conversation endpoints.
    """

    routes = get_router_routes(
        conversation_router
    )

    assert len(routes) == 5

    assert any(
        method == "POST"
        for method, _ in routes
    )

    assert any(
        method == "GET"
        for method, _ in routes
    )


def test_memory_router_is_configured():
    """
    Verify memory endpoints.
    """

    routes = get_router_routes(
        memory_router
    )

    assert len(routes) == 5

    assert any(
        method == "GET"
        for method, _ in routes
    )


def test_message_and_profile_routers_are_configured():
    """
    Verify message and profile
    endpoints.
    """

    message_routes = (
        get_router_routes(
            message_router
        )
    )

    profile_routes = (
        get_router_routes(
            profile_router
        )
    )

    assert len(
        message_routes
    ) == 4

    assert len(
        profile_routes
    ) > 0


def test_ai_chat_router_has_response_model():
    """
    Verify the AI chat endpoint and
    its documented response model.
    """

    assert (
        len(ai_chat_router.routes)
        == 1
    )

    chat_route = (
        ai_chat_router.routes[0]
    )

    assert (
        "POST"
        in chat_route.methods
    )

    assert (
        "chat"
        in chat_route.path.lower()
    )

    assert (
        chat_route.response_model
        is not None
    )


def test_openapi_schema_is_generated():
    """
    Verify valid OpenAPI generation.
    """

    openapi_schema = (
        app.openapi()
    )

    assert (
        openapi_schema[
            "info"
        ]["title"]
        == app.title
    )

    assert (
        openapi_schema[
            "info"
        ]["version"]
        == app.version
    )

    assert (
        "paths"
        in openapi_schema
    )

    assert (
        len(
            openapi_schema["paths"]
        )
        > 0
    )