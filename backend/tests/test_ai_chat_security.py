from unittest.mock import patch
from uuid import uuid4


def get_headers(
    client,
):
    """
    Create a unique user, authenticate,
    and return JWT headers.
    """

    unique_id = uuid4().hex[:10]

    username = (
        f"security_user_{unique_id}"
    )

    email = (
        f"security_{unique_id}"
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

    token = (
        login_response
        .json()["access_token"]
    )

    return {
        "Authorization": (
            f"Bearer {token}"
        )
    }


def create_digital_twin(
    client,
    headers,
):
    """
    Create a Digital Twin for a test user.
    """

    response = client.post(
        "/digital-twin",
        headers=headers,
        json={
            "twin_name": (
                "Security Test Twin"
            ),
            "personality": (
                "Helpful, secure, reliable, "
                "and practical"
            ),
            "communication_style": (
                "Clear and concise"
            ),
            "goals": (
                "Provide secure personalized "
                "AI assistance"
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
    Create a conversation owned by
    the authenticated user.
    """

    response = client.post(
        "/conversations",
        headers=headers,
        json={
            "title": (
                "Security Validation Test"
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


def test_chat_rejects_empty_message(
    client,
):
    """
    Verify that an empty AI chat
    message is rejected.
    """

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

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/chat"
        ),
        headers=headers,
        json={
            "message": "",
        },
    )

    assert (
        response.status_code
        == 422
    ), (
        "EMPTY MESSAGE VALIDATION FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_chat_rejects_oversized_message(
    client,
):
    """
    Verify that a message exceeding the
    maximum length is rejected.
    """

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

    oversized_message = (
        "A" * 5001
    )

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/chat"
        ),
        headers=headers,
        json={
            "message": oversized_message,
        },
    )

    assert (
        response.status_code
        == 422
    ), (
        "MESSAGE LENGTH VALIDATION FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_chat_requires_jwt_token(
    client,
):
    """
    Verify that AI chat cannot be used
    without authentication.
    """

    response = client.post(
        (
            "/conversations/"
            "invalid-conversation-id/"
            "chat"
        ),
        json={
            "message": (
                "This request has no token."
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
        "JWT PROTECTION FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )


@patch(
    "app.services.ai_provider."
    "ai_provider_service."
    "generate_response"
)
def test_user_cannot_access_another_users_conversation(
    mock_generate_response,
    client,
):
    """
    Verify conversation ownership
    isolation between users.
    """

    mock_generate_response.return_value = (
        "This response should not "
        "be generated."
    )

    owner_headers = get_headers(
        client
    )

    create_digital_twin(
        client=client,
        headers=owner_headers,
    )

    conversation = (
        create_conversation(
            client=client,
            headers=owner_headers,
        )
    )

    other_user_headers = get_headers(
        client
    )

    create_digital_twin(
        client=client,
        headers=other_user_headers,
    )

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/chat"
        ),
        headers=other_user_headers,
        json={
            "message": (
                "Access another user's "
                "conversation."
            ),
        },
    )

    assert (
        response.status_code
        in {
            403,
            404,
        }
    ), (
        "CONVERSATION OWNERSHIP "
        "PROTECTION FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )

    mock_generate_response\
        .assert_not_called()