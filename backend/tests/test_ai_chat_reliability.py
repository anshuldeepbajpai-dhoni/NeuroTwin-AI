from unittest.mock import patch
from uuid import uuid4


def get_headers(
    client,
):
    """
    Register and authenticate a unique
    reliability-test user.
    """

    unique_id = uuid4().hex[:10]

    username = (
        f"reliability_{unique_id}"
    )

    email = (
        f"reliability_{unique_id}"
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
    reliability-test user.
    """

    response = client.post(
        "/digital-twin",
        headers=headers,
        json={
            "twin_name": (
                "Reliability Test Twin"
            ),
            "personality": (
                "Helpful, reliable, "
                "practical, and supportive"
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
    reliability-test user.
    """

    response = client.post(
        "/conversations",
        headers=headers,
        json={
            "title": (
                "Reliability Test"
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
    "ai_provider_service."
    "generate_response"
)
def test_ai_failure_removes_incomplete_message(
    mock_generate_response,
    client,
):
    """
    Verify that an AI-provider failure
    returns 503 and does not leave an
    incomplete user message.
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

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/chat"
        ),
        headers=headers,
        json={
            "message": (
                "This message should be "
                "removed after AI failure."
            ),
        },
    )

    assert (
        response.status_code
        == 503
    ), (
        "AI FAILURE STATUS FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )

    messages_response = client.get(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages"
        ),
        headers=headers,
    )

    assert (
        messages_response.status_code
        == 200
    ), (
        "MESSAGE RETRIEVAL FAILED: "
        f"{messages_response.status_code} "
        f"{messages_response.json()}"
    )

    response_data = (
        messages_response.json()
    )

    if isinstance(
        response_data,
        dict,
    ):
        messages = (
            response_data.get(
                "items",
                response_data.get(
                    "messages",
                    [],
                ),
            )
        )
    else:
        messages = response_data

    failed_content = (
        "This message should be "
        "removed after AI failure."
    )

    assert not any(
        message["content"]
        == failed_content
        for message in messages
    ), (
        "ORPHAN USER MESSAGE FOUND: "
        f"{messages}"
    )


@patch(
    "app.api.ai_chat."
    "automatic_memory_service."
    "process_message"
)
@patch(
    "app.services.ai_provider."
    "ai_provider_service."
    "generate_response"
)
def test_memory_failure_does_not_break_chat(
    mock_generate_response,
    mock_process_message,
    client,
):
    """
    Verify that automatic-memory failure
    does not destroy a successful chat.
    """

    mock_generate_response.return_value = (
        "Your AI learning progress "
        "is moving forward."
    )

    mock_process_message.side_effect = (
        RuntimeError(
            "Memory processing failed"
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

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/chat"
        ),
        headers=headers,
        json={
            "message": (
                "I am improving my "
                "FastAPI skills."
            ),
        },
    )

    assert (
        response.status_code
        == 201
    ), (
        "MEMORY FAILURE BROKE CHAT: "
        f"{response.status_code} "
        f"{response.json()}"
    )

    response_data = (
        response.json()
    )

    assert (
        response_data[
            "assistant_message"
        ]["content"]
        == (
            "Your AI learning progress "
            "is moving forward."
        )
    )

    mock_process_message\
        .assert_called_once()


@patch(
    "app.services.conversation_summary."
    "conversation_summary_service."
    "update_summary"
)

@patch(
    "app.services.ai_provider."
    "ai_provider_service."
    "generate_response"
)
def test_summary_failure_does_not_break_chat(
    mock_generate_response,
    mock_update_summary,
    client,
):
    """
    Verify that conversation-summary
    failure does not destroy a
    successfully generated chat.
    """

    mock_generate_response.return_value = (
        "Your FastAPI progress is "
        "continuing successfully."
    )

    mock_update_summary.side_effect = (
        RuntimeError(
            "Summary processing failed"
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

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/chat"
        ),
        headers=headers,
        json={
            "message": (
                "I completed another "
                "FastAPI backend phase."
            ),
        },
    )

    assert (
        response.status_code
        == 201
    ), (
        "SUMMARY FAILURE BROKE CHAT: "
        f"{response.status_code} "
        f"{response.json()}"
    )

    response_data = (
        response.json()
    )

    assert (
        response_data[
            "assistant_message"
        ]["content"]
        == (
            "Your FastAPI progress is "
            "continuing successfully."
        )
    )

    mock_update_summary\
        .assert_called_once()