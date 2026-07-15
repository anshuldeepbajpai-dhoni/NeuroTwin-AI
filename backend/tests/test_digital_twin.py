from uuid import uuid4


def get_headers(
    client,
):
    """
    Register and authenticate a unique
    Digital Twin test user.
    """

    unique_id = uuid4().hex[:10]

    username = (
        f"twin_user_{unique_id}"
    )

    email = (
        f"twin_{unique_id}"
        "@example.com"
    )

    password = (
        "Pass@123"
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
        "DIGITAL TWIN TEST USER "
        "REGISTRATION FAILED: "
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
        "DIGITAL TWIN TEST USER "
        "LOGIN FAILED: "
        f"{login_response.status_code} "
        f"{login_response.json()}"
    )

    response_data = (
        login_response.json()
    )

    assert (
        "access_token"
        in response_data
    ), (
        "ACCESS TOKEN MISSING: "
        f"{response_data}"
    )

    access_token = (
        response_data[
            "access_token"
        ]
    )

    return {
        "Authorization": (
            f"Bearer {access_token}"
        )
    }


def delete_existing(
    client,
    headers,
):
    """
    Delete an existing Digital Twin
    belonging to the current test user.

    A 404 response is acceptable when
    the user has no Digital Twin.
    """

    response = client.delete(
        "/digital-twin/",
        headers=headers,
    )

    assert (
        response.status_code
        in {
            200,
            404,
        }
    ), (
        "DIGITAL TWIN CLEANUP FAILED: "
        f"{response.status_code} "
        f"{response.json()}"
    )


def create_sample(
    client,
    headers,
):
    """
    Create a sample Digital Twin using
    the same authenticated test user.
    """

    delete_existing(
        client=client,
        headers=headers,
    )

    response = client.post(
        "/digital-twin/",
        headers=headers,
        json={
            "twin_name": (
                "Anshul AI"
            ),
            "personality": (
                "Friendly AI assistant"
            ),
            "communication_style": (
                "Professional"
            ),
            "goals": (
                "Help users"
            ),
            "interests": (
                "AI, Python"
            ),
        },
    )

    return response


def test_create_digital_twin(
    client,
):
    """
    Verify Digital Twin creation.
    """

    headers = get_headers(
        client
    )

    response = create_sample(
        client=client,
        headers=headers,
    )

    assert (
        response.status_code
        == 201
    ), (
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_duplicate_digital_twin(
    client,
):
    """
    Verify that one user cannot create
    multiple Digital Twins.
    """

    headers = get_headers(
        client
    )

    first_response = create_sample(
        client=client,
        headers=headers,
    )

    assert (
        first_response.status_code
        == 201
    )

    response = client.post(
        "/digital-twin/",
        headers=headers,
        json={
            "twin_name": (
                "Duplicate AI"
            ),
            "personality": (
                "Duplicate personality "
                "for testing."
            ),
            "communication_style": (
                "Professional"
            ),
            "goals": (
                "Duplicate goals "
                "for testing."
            ),
            "interests": (
                "Artificial Intelligence"
            ),
        },
    )

    assert (
        response.status_code
        == 409
    ), (
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_get_digital_twin(
    client,
):
    """
    Verify Digital Twin retrieval.
    """

    headers = get_headers(
        client
    )

    create_response = create_sample(
        client=client,
        headers=headers,
    )

    assert (
        create_response.status_code
        == 201
    )

    response = client.get(
        "/digital-twin/",
        headers=headers,
    )

    assert (
        response.status_code
        == 200
    ), (
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_update_digital_twin(
    client,
):
    """
    Verify Digital Twin updates.
    """

    headers = get_headers(
        client
    )

    create_response = create_sample(
        client=client,
        headers=headers,
    )

    assert (
        create_response.status_code
        == 201
    )

    response = client.put(
        "/digital-twin/",
        headers=headers,
        json={
            "communication_style": (
                "Casual"
            ),
        },
    )

    assert (
        response.status_code
        == 200
    ), (
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_empty_update(
    client,
):
    """
    Verify that an empty update request
    is rejected.
    """

    headers = get_headers(
        client
    )

    create_response = create_sample(
        client=client,
        headers=headers,
    )

    assert (
        create_response.status_code
        == 201
    )

    response = client.put(
        "/digital-twin/",
        headers=headers,
        json={},
    )

    assert (
        response.status_code
        == 400
    ), (
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_delete_digital_twin(
    client,
):
    """
    Verify Digital Twin deletion.
    """

    headers = get_headers(
        client
    )

    create_response = create_sample(
        client=client,
        headers=headers,
    )

    assert (
        create_response.status_code
        == 201
    )

    response = client.delete(
        "/digital-twin/",
        headers=headers,
    )

    assert (
        response.status_code
        == 200
    ), (
        f"{response.status_code} "
        f"{response.json()}"
    )


def test_get_after_delete(
    client,
):
    """
    Verify that a deleted Digital Twin
    can no longer be retrieved.
    """

    headers = get_headers(
        client
    )

    create_response = create_sample(
        client=client,
        headers=headers,
    )

    assert (
        create_response.status_code
        == 201
    )

    delete_response = client.delete(
        "/digital-twin/",
        headers=headers,
    )

    assert (
        delete_response.status_code
        == 200
    )

    response = client.get(
        "/digital-twin/",
        headers=headers,
    )

    assert (
        response.status_code
        == 404
    ), (
        f"{response.status_code} "
        f"{response.json()}"
    )