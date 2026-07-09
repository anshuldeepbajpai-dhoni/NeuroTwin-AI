def test_root(client):

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Running"