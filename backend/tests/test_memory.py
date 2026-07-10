from tests.test_profile import get_headers

def test_get_memories_pagination_metadata(
    client
):
    headers = get_headers(client)

    response = client.get(
        "/memories/",
        headers=headers,
        params={
            "page": 1,
            "page_size": 2,
            "sort_by": "created_at",
            "sort_order": "desc",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data

    assert isinstance(
        data["items"],
        list,
    )

    assert isinstance(
        data["total"],
        int,
    )

    assert data["page"] == 1

    assert data["page_size"] == 2

    assert len(
        data["items"]
    ) <= 2

def test_invalid_memory_page(
    client
):
    headers = get_headers(client)

    response = client.get(
        "/memories/",
        headers=headers,
        params={
            "page": 0,
        },
    )

    assert response.status_code == 422

def test_sort_memories_by_importance(
    client
):
    headers = get_headers(client)

    response = client.get(
        "/memories/",
        headers=headers,
        params={
            "sort_by": "importance",
            "sort_order": "desc",
            "page": 1,
            "page_size": 100,
        },
    )

    assert response.status_code == 200

    data = response.json()

    items = data["items"]

    importance_values = [
        item["importance"]
        for item in items
    ]

    assert importance_values == sorted(
        importance_values,
        reverse=True,
    )

def test_invalid_memory_sort_field(
    client
):
    headers = get_headers(client)

    response = client.get(
        "/memories/",
        headers=headers,
        params={
            "sort_by": "password",
        },
    )

    assert response.status_code == 422

def ensure_digital_twin(
    client,
    headers,
):
    response = client.get(
        "/digital-twin/",
        headers=headers,
    )

    if response.status_code == 200:
        return response.json()

    create_response = client.post(
        "/digital-twin/",
        headers=headers,
        json={
            "twin_name": "Anshul Test AI",
            "personality": (
                "Friendly, analytical, helpful, "
                "and focused on technical problem solving."
            ),
            "communication_style": (
                "Professional and clear"
            ),
            "goals": (
                "Help users solve artificial intelligence "
                "and software engineering problems."
            ),
            "interests": (
                "Artificial Intelligence, Python, "
                "FastAPI, and Data Science"
            ),
        },
    )

    assert (
        create_response.status_code
        in (201, 409)
    ), create_response.text

    if create_response.status_code == 201:
        return create_response.json()

    get_response = client.get(
        "/digital-twin/",
        headers=headers,
    )

    assert (
        get_response.status_code == 200
    ), get_response.text

    return get_response.json()

def create_test_memory(
    client,
    headers,
    title="Python Development",
    content="The user enjoys building backend APIs with Python and FastAPI.",
    category="Programming",
    importance=5,
    is_favorite=True,
):
    response = client.post(
        "/memories/",
        headers=headers,
        json={
            "title": title,
            "content": content,
            "category": category,
            "importance": importance,
            "is_favorite": is_favorite,
        },
    )

    assert response.status_code == 201, response.text

    return response

def test_complete_memory_lifecycle(
    client
):
    headers = get_headers(client)

    # Memory creation requires a Digital Twin.
    ensure_digital_twin(
        client=client,
        headers=headers,
    )

    # -------------------------
    # 1. Create Memory
    # -------------------------
    
    create_response = create_test_memory(
        client=client,
        headers=headers,
        title="FastAPI Backend Development",
        content=(
            "The user is developing a professional "
            "backend application using FastAPI."
        ),
        category="Programming",
        importance=5,
        is_favorite=True,
    )

    created_memory = create_response.json()

    memory_id = created_memory["id"]

    assert created_memory["title"] == (
        "FastAPI Backend Development"
    )

    assert created_memory["category"] == (
        "Programming"
    )

    assert created_memory["importance"] == 5

    assert created_memory["is_favorite"] is True

    # -------------------------
    # 2. Get Memory by ID
    # -------------------------

    get_response = client.get(
        f"/memories/{memory_id}",
        headers=headers,
    )

    assert (
        get_response.status_code
        == 200
    ), get_response.text

    fetched_memory = get_response.json()

    assert (
        fetched_memory["id"]
        == memory_id
    )

    assert (
        fetched_memory["title"]
        == "FastAPI Backend Development"
    )

    # -------------------------
    # 3. Search Memory
    # -------------------------

    search_response = client.get(
        "/memories/",
        headers=headers,
        params={
            "search": "FastAPI",
            "page": 1,
            "page_size": 10,
        },
    )

    assert (
        search_response.status_code
        == 200
    ), search_response.text

    search_data = search_response.json()

    assert "items" in search_data

    assert any(
        memory["id"] == memory_id
        for memory in search_data["items"]
    )

    # -------------------------
    # 4. Filter by Category
    # -------------------------

    category_response = client.get(
        "/memories/",
        headers=headers,
        params={
            "category": "Programming",
            "page": 1,
            "page_size": 100,
        },
    )

    assert (
        category_response.status_code
        == 200
    ), category_response.text

    category_data = (
        category_response.json()
    )

    assert any(
        memory["id"] == memory_id
        for memory in category_data["items"]
    )

    assert all(
        memory["category"].lower()
        == "programming"
        for memory in category_data["items"]
    )

    # -------------------------
    # 5. Filter by Importance
    # -------------------------

    importance_response = client.get(
        "/memories/",
        headers=headers,
        params={
            "importance": 5,
            "page": 1,
            "page_size": 100,
        },
    )

    assert (
        importance_response.status_code
        == 200
    ), importance_response.text

    importance_data = (
        importance_response.json()
    )

    assert any(
        memory["id"] == memory_id
        for memory in importance_data["items"]
    )

    assert all(
        memory["importance"] == 5
        for memory in importance_data["items"]
    )

    # -------------------------
    # 6. Filter Favorites
    # -------------------------

    favorite_response = client.get(
        "/memories/",
        headers=headers,
        params={
            "is_favorite": True,
            "page": 1,
            "page_size": 100,
        },
    )

    assert (
        favorite_response.status_code
        == 200
    ), favorite_response.text

    favorite_data = (
        favorite_response.json()
    )

    assert any(
        memory["id"] == memory_id
        for memory in favorite_data["items"]
    )

    assert all(
        memory["is_favorite"] is True
        for memory in favorite_data["items"]
    )

    # -------------------------
    # 7. Update Memory
    # -------------------------

    update_response = client.put(
        f"/memories/{memory_id}",
        headers=headers,
        json={
            "title": (
                "Advanced FastAPI Development"
            ),
            "importance": 4,
            "is_favorite": False,
        },
    )

    assert (
        update_response.status_code
        == 200
    ), update_response.text

    updated_memory = (
        update_response.json()
    )

    assert (
        updated_memory["title"]
        == "Advanced FastAPI Development"
    )

    assert (
        updated_memory["importance"]
        == 4
    )

    assert (
        updated_memory["is_favorite"]
        is False
    )

    # -------------------------
    # 8. Empty Update
    # -------------------------

    empty_update_response = client.put(
        f"/memories/{memory_id}",
        headers=headers,
        json={},
    )

    assert (
        empty_update_response.status_code
        == 400
    ), empty_update_response.text

    empty_update_data = (
        empty_update_response.json()
    )

    assert (
        empty_update_data["detail"]
        == "No fields provided for update."
    )

    # -------------------------
    # 9. Delete Memory
    # -------------------------

    delete_response = client.delete(
        f"/memories/{memory_id}",
        headers=headers,
    )

    assert (
        delete_response.status_code
        == 200
    ), delete_response.text

    delete_data = (
        delete_response.json()
    )

    assert (
        delete_data["message"]
        == "Memory deleted successfully."
    )

    # -------------------------
    # 10. Get After Delete
    # -------------------------

    get_after_delete = client.get(
        f"/memories/{memory_id}",
        headers=headers,
    )

    assert (
        get_after_delete.status_code
        == 404
    ), get_after_delete.text

    deleted_memory_data = (
        get_after_delete.json()
    )

    assert (
        deleted_memory_data["detail"]
        == "Memory not found."
    )

def test_combined_memory_filters(
    client
):
    headers = get_headers(client)

    response = client.get(
        "/memories/",
        headers=headers,
        params={
            "search": "Python",
            "category": "Programming",
            "importance": 5,
            "is_favorite": True,
            "page": 1,
            "page_size": 10,
            "sort_by": "created_at",
            "sort_order": "desc",
        },
    )

    assert (
        response.status_code
        == 200
    ), response.text

    data = response.json()

    assert "items" in data

    assert "total" in data

    assert "page" in data

    assert "page_size" in data

    assert "total_pages" in data

    assert data["page"] == 1

    assert data["page_size"] == 10

    for memory in data["items"]:

        searchable_text = (
            memory["title"]
            + " "
            + memory["content"]
        ).lower()

        assert "python" in searchable_text

        assert (
            memory["category"].lower()
            == "programming"
        )

        assert (
            memory["importance"]
            == 5
        )

        assert (
            memory["is_favorite"]
            is True
        )

def test_memory_not_found(
    client
):
    headers = get_headers(client)

    memory_id = (
        "00000000-0000-0000-"
        "0000-000000000000"
    )

    response = client.get(
        f"/memories/{memory_id}",
        headers=headers,
    )

    assert (
        response.status_code
        == 404
    ), response.text

    data = response.json()

    assert (
        data["detail"]
        == "Memory not found."
    )