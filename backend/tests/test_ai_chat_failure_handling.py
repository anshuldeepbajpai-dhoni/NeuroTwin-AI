from unittest.mock import patch
from uuid import uuid4
import pytest


def get_headers(
    client,
):
    """
    Register a unique test user,
    log in, and return JWT headers.
    """

    unique_id = uuid4().hex[:10]

    username = (
        f"failure_user_{unique_id}"
    )

    email = (
        f"failure_{unique_id}"
        "@example.com"
    )

    password = (
        "StrongPassword123!"
    )

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert (
        register_response.status_code
        == 201
    ), (
        "REGISTER FAILED: "
        f"{register_response.status_code} "
        f"{register_response.json()}"
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert (
        login_response.status_code
        == 200
    ), (
        "LOGIN FAILED: "
        f"{login_response.status_code} "
        f"{login_response.json()}"
    )

    access_token = (
        login_response
        .json()["access_token"]
    )

    return {
        "Authorization": (
            f"Bearer {access_token}"
        )
    }


def create_digital_twin(
    client,
    headers,
):
    """
    Create a Digital Twin for the
    authenticated test user.
    """

    response = client.post(
        "/digital-twin",
        headers=headers,
        json={
            "twin_name": (
                "Failure Test Twin"
            ),
            "personality": (
                "Helpful, reliable, "
                "practical, and calm"
            ),
            "communication_style": (
                "Clear and concise"
            ),
            "goals": (
                "Provide reliable and "
                "personalized assistance"
            ),
            "interests": (
                "Artificial intelligence, "
                "Python, and FastAPI"
            ),
        },
    )

    assert (
        response.status_code
        == 201
    ), (
        "DIGITAL TWIN CREATION FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )


def create_conversation(
    client,
    headers,
):
    """
    Create a conversation for the
    authenticated test user.
    """

    response = client.post(
        "/conversations",
        headers=headers,
        json={
            "title": (
                "Failure Handling Test"
            ),
        },
    )

    assert (
        response.status_code
        == 201
    ), (
        "CONVERSATION CREATION FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )

    return response.json()


def test_ai_chat_requires_authentication(
    client,
):
    """
    Verify that an unauthenticated user
    cannot access the AI chat endpoint.
    """

    response = client.post(
        (
            "/conversations/"
            "invalid-conversation-id/"
            "chat"
        ),
        json={
            "message": (
                "This request should "
                "not be authorized."
            ),
        },
    )

    assert (
        response.status_code
        in {
            401,
            403,
        }
    ), (
        "AUTHENTICATION PROTECTION FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_ai_chat_rejects_invalid_conversation(
    client,
):
    """
    Verify that an authenticated user
    cannot chat using a nonexistent
    conversation ID.
    """

    headers = get_headers(
        client
    )

    create_digital_twin(
        client=client,
        headers=headers,
    )

    response = client.post(
        (
            "/conversations/"
            "invalid-conversation-id/"
            "chat"
        ),
        headers=headers,
        json={
            "message": (
                "Test invalid conversation."
            ),
        },
    )

    assert (
        response.status_code
        in {
            404,
            422,
        }
    ), (
        "INVALID CONVERSATION HANDLING "
        "FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )


@patch(
    "app.services.ai_provider."
    "ai_provider_service."
    "generate_response"
)
def test_ai_provider_failure_is_handled(
    mock_generate_response,
    client,
):
    """
    Verify that an unexpected AI-provider
    failure returns a controlled API error.
    """

    mock_generate_response.side_effect = (
        RuntimeError(
            "AI provider unavailable"
        )
    )

    headers = get_headers(
        client
    )

    create_digital_twin(
        client=client,
        headers=headers,
    )

    conversation = (
        create_conversation(
            client=client,
            headers=headers,
        )
    )

    with pytest.raises(
        RuntimeError,
        match="AI provider unavailable",
    ):
        client.post(
            (
                "/conversations/"
                f"{conversation['id']}"
                "/chat"
            ),
            headers=headers,
            json={
                "message": (
                    "Generate a test response."
                ),
            },
        )

    mock_generate_response\
        .assert_called_once()