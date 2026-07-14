from unittest.mock import patch
from uuid import uuid4


def get_headers(
    client,
):
    """
    Register a unique user,
    log in, and return JWT headers.
    """

    unique_id = uuid4().hex[:10]

    username = (
        f"memory_user_{unique_id}"
    )

    email = (
        f"memory_{unique_id}"
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
    Create the user's Digital Twin.
    """

    response = client.post(
        "/digital-twin",
        headers=headers,
        json={
            "twin_name": (
                "Memory Intelligence Twin"
            ),
            "personality": (
                "Helpful, intelligent, "
                "practical, and supportive"
            ),
            "communication_style": (
                "Clear and concise"
            ),
            "goals": (
                "Understand the user and "
                "provide personalized help"
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

    return response.json()


def create_conversation(
    client,
    headers,
):
    """
    Create a conversation.
    """

    response = client.post(
        "/conversations",
        headers=headers,
        json={
            "title": (
                "Automatic Memory Test"
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
    "app.services.automatic_memory."
    "memory_extractor.extract"
)
def test_chat_creates_automatic_memory(
    mock_extract,
    mock_generate_response,
    client,
):
    """
    Verify that meaningful information
    sent through AI chat creates a
    long-term memory.
    """

    user_message = (
        "I want to become an AI engineer "
        "and I am learning FastAPI."
    )

    ai_response = (
        "Your AI engineering goal and "
        "FastAPI learning journey can help "
        "me provide personalized guidance."
    )

    mock_generate_response.return_value = (
        ai_response
    )

    mock_extract.return_value = {
        "should_save": True,
        "title": (
            "AI Engineering Goal"
        ),
        "content": (
            "The user wants to become "
            "an AI engineer and is "
            "learning FastAPI."
        ),
        "category": "goal",
        "importance": 5,
    }

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

    chat_response = client.post(
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
        chat_response.status_code
        == 201
    ), (
        "AI CHAT FAILED: "
        f"{chat_response.status_code} "
        f"{chat_response.json()}"
    )

    mock_generate_response.assert_called_once()

    mock_extract.assert_called_once_with(
        user_message
    )

    memory_response = client.get(
        "/memories",
        headers=headers,
    )

    assert (
        memory_response.status_code
        == 200
    ), (
        "MEMORY RETRIEVAL FAILED: "
        f"{memory_response.status_code} "
        f"{memory_response.json()}"
    )

    memory_data = (
        memory_response.json()
    )

    if isinstance(
        memory_data,
        dict,
    ):
        memories = (
            memory_data.get(
                "items",
                memory_data.get(
                    "memories",
                    [],
                ),
            )
        )
    else:
        memories = memory_data

    assert len(memories) >= 1

    created_memory = next(
        (
            memory
            for memory in memories
            if memory["title"]
            == "AI Engineering Goal"
        ),
        None,
    )

    assert (
        created_memory
        is not None
    ), (
        "AUTOMATIC MEMORY NOT FOUND: "
        f"{memory_data}"
    )

    assert (
        created_memory["content"]
        == (
            "The user wants to become "
            "an AI engineer and is "
            "learning FastAPI."
        )
    )

    assert (
        created_memory["category"]
        == "goal"
    )

    assert (
        created_memory["importance"]
        == 5
    )