from tests.test_profile import get_headers


def create_digital_twin(
    client,
    headers,
):
    response = client.post(
        "/digital-twin",
        headers=headers,
        json={
            "twin_name": "Message Test AI",
            "personality": (
                "Friendly, intelligent, helpful, "
                "and focused on user learning."
            ),
            "communication_style": "Professional",
            "goals": (
                "Help users solve programming "
                "and artificial intelligence "
                "problems."
            ),
            "interests": (
                "Python, FastAPI, machine "
                "learning, and data science"
            ),
        },
    )

    assert response.status_code in [
        200,
        201,
        409,
    ]


def create_conversation(
    client,
    headers,
):
    response = client.post(
        "/conversations",
        headers=headers,
        json={
            "title": (
                "Message Testing Conversation"
            ),
        },
    )

    assert response.status_code == 201

    return response.json()


def create_message(
    client,
    headers,
    conversation_id,
    content="How can I learn FastAPI?",
):
    response = client.post(
        (
            "/conversations/"
            f"{conversation_id}"
            "/messages"
        ),
        headers=headers,
        json={
            "role": "user",
            "content": content,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_message(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages"
        ),
        headers=headers,
        json={
            "role": "user",
            "content": (
                "Explain FastAPI routing."
            ),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["role"] == "user"

    assert (
        data["content"]
        == "Explain FastAPI routing."
    )

    assert "id" in data

    assert "conversation_id" in data

    assert "user_id" in data

    assert "created_at" in data


def test_get_messages(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    create_message(
        client,
        headers,
        conversation["id"],
    )

    response = client.get(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages"
        ),
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data

    assert data["total"] >= 1

    assert "total_pages" in data


def test_get_message_by_id(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    message = create_message(
        client,
        headers,
        conversation["id"],
    )

    response = client.get(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages/"
            f"{message['id']}"
        ),
        headers=headers,
    )

    assert response.status_code == 200

    assert (
        response.json()["id"]
        == message["id"]
    )


def test_filter_messages_by_role(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    create_message(
        client,
        headers,
        conversation["id"],
    )

    response = client.get(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages"
        ),
        headers=headers,
        params={
            "role": "user",
        },
    )

    assert response.status_code == 200

    assert all(
        item["role"] == "user"
        for item in (
            response.json()["items"]
        )
    )


def test_assistant_role_is_blocked(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages"
        ),
        headers=headers,
        json={
            "role": "assistant",
            "content": (
                "Fake assistant Message."
            ),
        },
    )

    assert response.status_code == 403

    assert (
        response.json()["detail"]
        == (
            "Users can create only "
            "user messages."
        )
    )


def test_system_role_is_blocked(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages"
        ),
        headers=headers,
        json={
            "role": "system",
            "content": (
                "Fake system Message."
            ),
        },
    )

    assert response.status_code == 403


def test_invalid_message_role(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    response = client.post(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages"
        ),
        headers=headers,
        json={
            "role": "admin",
            "content": "Invalid role.",
        },
    )

    assert response.status_code == 422


def test_invalid_message_page(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    response = client.get(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages"
        ),
        headers=headers,
        params={
            "page": 0,
        },
    )

    assert response.status_code == 422


def test_message_not_found(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    response = client.get(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages/"
            "invalid-message-id"
        ),
        headers=headers,
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Message not found."
    )


def test_delete_message(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    conversation = create_conversation(
        client,
        headers,
    )

    message = create_message(
        client,
        headers,
        conversation["id"],
        "Delete this Message.",
    )

    response = client.delete(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages/"
            f"{message['id']}"
        ),
        headers=headers,
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Message deleted successfully."
    )

    get_response = client.get(
        (
            "/conversations/"
            f"{conversation['id']}"
            "/messages/"
            f"{message['id']}"
        ),
        headers=headers,
    )

    assert (
        get_response.status_code
        == 404
    )