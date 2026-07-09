import uuid

from tests.conftest import client


def test_register(client):

    unique = str(uuid.uuid4())[:8]

    response = client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@gmail.com",
            "password": "Pass@123",
            "role": "user"
        }
    )

    assert response.status_code in [200, 201]

def test_login(client):

    unique = str(uuid.uuid4())[:8]

    client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@gmail.com",
            "password": "Pass@123",
            "role": "user"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": f"{unique}@gmail.com",
            "password": "Pass@123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()