from uuid import uuid4


def get_headers(
    client,
):
    """
    Register and authenticate a unique
    test user.
    """

    unique_id = uuid4().hex[:10]

    username = (
        f"test_user_{unique_id}"
    )

    email = (
        f"test_{unique_id}"
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
        "TEST USER REGISTRATION FAILED: "
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
        "TEST USER LOGIN FAILED: "
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

    token = (
        response_data[
            "access_token"
        ]
    )

    return {
        "Authorization": (
            f"Bearer {token}"
        )
    }



def test_get_profile(client):

    headers = get_headers(client)

    response = client.get(
        "/users/profile",
        headers=headers
    )

    assert response.status_code == 200


def test_update_profile(client):

    headers = get_headers(client)

    response = client.put(
        "/users/profile",
        headers=headers,
        json={
            "phone": "+919876543210",
            "bio": "Testing Profile API",
            "timezone": "Asia/Kolkata",
            "language": "English"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200, response.text

def test_update_avatar(client):

    headers = get_headers(client)

    with open("tests/sample.png", "rb") as image:

        response = client.patch(
            "/users/profile/avatar",
            headers=headers,
            files={
                "avatar": (
                    "sample.png",
                    image,
                    "image/png"
                )
            }
        )

    assert response.status_code == 200


def test_delete_avatar(client):

    headers = get_headers(client)

    response = client.delete(
        "/users/profile/avatar",
        headers=headers
    )

    assert response.status_code == 200