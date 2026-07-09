from app.core.security import create_access_token


def get_headers():

    token = create_access_token(
        {
            "sub": "admin@gmail.com",
            "id": "dc416fd0-c31b-451d-8da4-4da980dfdd7b",
            "role": "admin"
        }
    )

    return {
        "Authorization": f"Bearer {token}"
    }


def delete_existing(client):

    client.delete(
        "/digital-twin/",
        headers=get_headers()
    )


def create_sample(client):

    delete_existing(client)

    response = client.post(
        "/digital-twin/",
        headers=get_headers(),
        json={
            "twin_name": "Anshul AI",
            "personality": "Friendly AI assistant",
            "communication_style": "Professional",
            "goals": "Help users",
            "interests": "AI, Python"
        }
    )

    return response

def test_create_digital_twin(client):

    response = create_sample(client)

    assert response.status_code == 201

def test_duplicate_digital_twin(client):

    create_sample(client)

    response = client.post(
        "/digital-twin/",
        headers=get_headers(),
    json={
        "twin_name": "Duplicate AI",
        "personality": "Duplicate personality for testing.",
        "communication_style": "Professional",
        "goals": "Duplicate goals for testing.",
        "interests": "Artificial Intelligence"
    }
    )

    assert response.status_code == 409

def test_get_digital_twin(client):

    create_sample(client)

    response = client.get(
        "/digital-twin/",
        headers=get_headers()
    )

    assert response.status_code == 200

def test_update_digital_twin(client):

    create_sample(client)

    response = client.put(
        "/digital-twin/",
        headers=get_headers(),
        json={
            "communication_style": "Casual"
        }
    )

    assert response.status_code == 200

def test_empty_update(client):

    create_sample(client)

    response = client.put(
        "/digital-twin/",
        headers=get_headers(),
        json={}
    )

    assert response.status_code == 400

def test_delete_digital_twin(client):

    create_sample(client)

    response = client.delete(
        "/digital-twin/",
        headers=get_headers()
    )

    assert response.status_code == 200

def test_get_after_delete(client):

    create_sample(client)

    client.delete(
        "/digital-twin/",
        headers=get_headers()
    )

    response = client.get(
        "/digital-twin/",
        headers=get_headers()
    )

    assert response.status_code == 404