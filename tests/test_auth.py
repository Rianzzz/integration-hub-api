def test_login_with_correct_credentials_returns_token(client):
    response = client.post(
        "/auth/token", data={"username": "admin", "password": "admin"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_with_wrong_credentials_returns_401(client):
    response = client.post(
        "/auth/token", data={"username": "admin", "password": "senha-errada"}
    )

    assert response.status_code == 401


def test_sync_without_token_is_rejected(client):
    response = client.post("/customers/sync")

    assert response.status_code == 401


def test_sync_with_valid_token_succeeds(client):
    token = client.post(
        "/auth/token", data={"username": "admin", "password": "admin"}
    ).json()["access_token"]

    response = client.post(
        "/customers/sync", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_list_customers_does_not_require_auth(client):
    response = client.get("/customers")

    assert response.status_code == 200
