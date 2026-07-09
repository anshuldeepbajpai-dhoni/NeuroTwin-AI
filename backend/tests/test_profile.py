def get_headers(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@gmail.com",
            "password": "Pass@123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def get_headers(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "admin@gmail.com",
            "password": "Pass@123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
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

    assert response.status_code == 200

    data = response.json()

    assert data["bio"] == "Testing Profile API"


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