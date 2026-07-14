from uuid import uuid4
from unittest.mock import patch


def get_headers(
    client,
):
    """
    Register a unique test user,
    log in, and return JWT headers.
    """

    unique_id = uuid4().hex[:10]

    username = (
        f"ai_user_{unique_id}"
    )

    email = (
        f"ai_{unique_id}"
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
    authenticated integration-test user.
    """

    response = client.post(
        "/digital-twin",
        headers=headers,
        json={
            "twin_name": (
                "AI Engineer Twin"
            ),
            "personality": (
                "Helpful, practical, "
                "focused, and encouraging"
            ),
            "communication_style": (
                "Clear and concise"
            ),
            "goals": (
                "Become an AI engineer "
                "and build production-ready "
                "AI applications"
            ),
            "interests": (
                "Python, FastAPI, machine "
                "learning, and generative AI"
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

    return response.json()


def create_conversation(
    client,
    headers,
):
    """
    Create a conversation for the
    authenticated integration-test user.
    """

    response = client.post(
        "/conversations",
        headers=headers,
        json={
            "title": (
                "AI Engineering Discussion"
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


@patch(
    "app.services.ai_provider."
    "ai_provider_service.generate_response"
)
@patch(
    "app.api.ai_chat."
    "automatic_memory_service."
    "process_message"
)
def test_complete_ai_chat_flow(
    mock_process_message,
    mock_generate_response,
    client,
):
    """
    Test the authenticated AI chat flow
    without calling OpenAI or Ollama.
    """

    ai_response = (
        "You are making strong progress. "
        "Continue learning FastAPI and "
        "build practical AI projects."
    )

    user_message = (
        "I am learning FastAPI and "
        "want to become an AI engineer."
    )

    mock_generate_response.return_value = (
        ai_response
    )

    mock_process_message.return_value = (
        None
    )

    headers = get_headers(
        client
    )

    digital_twin = (
        create_digital_twin(
            client=client,
            headers=headers,
        )
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
            "message": user_message,
        },
    )

    assert (
        response.status_code
        == 201
    ), (
        "AI CHAT FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )

    response_data = (
        response.json()
    )

    assert (
    "user_message"
    in response_data
)

    assert (
        "assistant_message"
        in response_data
    )

    assert (
        response_data[
            "user_message"
        ]["role"]
        == "user"
    )

    assert (
        response_data[
            "user_message"
        ]["content"]
        == user_message
    )

    assert (
        response_data[
            "assistant_message"
        ]["role"]
        == "assistant"
    )

    assert (
        response_data[
            "assistant_message"
        ]["content"]
        == ai_response
    )

    mock_generate_response.assert_called_once()

    mock_process_message.assert_called_once()