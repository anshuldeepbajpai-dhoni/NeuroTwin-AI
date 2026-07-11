from uuid import uuid4

from tests.test_profile import get_headers


def create_digital_twin(
    client,
    headers,
):
    response = client.post(
        "/digital-twin",
        headers=headers,
        json={
            "twin_name": "Conversation Test AI",
            "personality": (
                "Friendly, analytical, helpful, "
                "and focused on technical learning."
            ),
            "communication_style": "Professional",
            "goals": (
                "Help users understand Python, "
                "FastAPI, and software engineering."
            ),
            "interests": (
                "Python, FastAPI, artificial "
                "intelligence, and data science"
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
    title="Python Development",
):
    response = client.post(
        "/conversations",
        headers=headers,
        json={
            "title": title,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_conversation(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    response = client.post(
        "/conversations",
        headers=headers,
        json={
            "title": "FastAPI Development",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert (
        data["title"]
        == "FastAPI Development"
    )

    assert data["is_archived"] is False

    assert "id" in data

    assert "user_id" in data

    assert "digital_twin_id" in data

    assert "created_at" in data

    assert "updated_at" in data


def test_get_conversations(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    create_conversation(
        client,
        headers,
        "Machine Learning",
    )

    response = client.get(
        "/conversations",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data

    assert "total" in data

    assert "page" in data

    assert "page_size" in data

    assert "total_pages" in data


def test_get_conversation_by_id(
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
        "Data Science",
    )

    conversation_id = (
        conversation["id"]
    )

    response = client.get(
        (
            "/conversations/"
            f"{conversation_id}"
        ),
        headers=headers,
    )

    assert response.status_code == 200

    assert (
        response.json()["id"]
        == conversation_id
    )


def test_search_conversations(
    client,
):
    headers = get_headers(
        client
    )

    create_digital_twin(
        client,
        headers,
    )

    unique_text = (
        f"Python {uuid4().hex[:8]}"
    )

    create_conversation(
        client,
        headers,
        unique_text,
    )

    response = client.get(
        "/conversations",
        headers=headers,
        params={
            "search": unique_text,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    assert any(
        item["title"]
        == unique_text
        for item in data["items"]
    )


def test_filter_archived_conversations(
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
        "Archived Conversation",
    )

    conversation_id = (
        conversation["id"]
    )

    update_response = client.patch(
        (
            "/conversations/"
            f"{conversation_id}"
        ),
        headers=headers,
        json={
            "is_archived": True,
        },
    )

    assert (
        update_response.status_code
        == 200
    )

    response = client.get(
        "/conversations",
        headers=headers,
        params={
            "is_archived": True,
        },
    )

    assert response.status_code == 200

    assert any(
        item["id"]
        == conversation_id
        for item in response.json()["items"]
    )


def test_update_conversation(
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
        "Old Conversation Title",
    )

    conversation_id = (
        conversation["id"]
    )

    response = client.patch(
        (
            "/conversations/"
            f"{conversation_id}"
        ),
        headers=headers,
        json={
            "title": (
                "Updated Conversation Title"
            ),
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["title"]
        == "Updated Conversation Title"
    )


def test_empty_conversation_update(
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

    response = client.patch(
        (
            "/conversations/"
            f"{conversation['id']}"
        ),
        headers=headers,
        json={},
    )

    assert response.status_code == 400


def test_invalid_conversation_page(
    client,
):
    headers = get_headers(
        client
    )

    response = client.get(
        "/conversations",
        headers=headers,
        params={
            "page": 0,
        },
    )

    assert response.status_code == 422


def test_conversation_not_found(
    client,
):
    headers = get_headers(
        client
    )

    response = client.get(
        (
            "/conversations/"
            "invalid-conversation-id"
        ),
        headers=headers,
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Conversation not found."
    )


def test_delete_conversation(
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
        "Delete Conversation",
    )

    conversation_id = (
        conversation["id"]
    )

    response = client.delete(
        (
            "/conversations/"
            f"{conversation_id}"
        ),
        headers=headers,
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == (
            "Conversation deleted "
            "successfully."
        )
    )

    get_response = client.get(
        (
            "/conversations/"
            f"{conversation_id}"
        ),
        headers=headers,
    )

    assert (
        get_response.status_code
        == 404
    )