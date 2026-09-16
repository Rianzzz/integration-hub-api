def test_sync_all_sources_creates_customers(client):
    response = client.post("/customers/sync")

    assert response.status_code == 200
    results = response.json()
    assert {r["source"] for r in results} == {"source_a", "source_b", "source_c"}
    assert all(r["created"] == 2 for r in results)
    assert all(r["total"] == 2 for r in results)


def test_sync_twice_is_idempotent(client):
    client.post("/customers/sync")

    second_response = client.post("/customers/sync")

    results = second_response.json()
    assert all(r["created"] == 0 and r["updated"] == 2 for r in results)
    assert len(client.get("/customers").json()) == 6


def test_list_customers_returns_all_synced_customers(client):
    client.post("/customers/sync")

    response = client.get("/customers")

    assert response.status_code == 200
    assert len(response.json()) == 6


def test_get_customer_by_id_returns_customer(client):
    client.post("/customers/sync")
    first_id = client.get("/customers").json()[0]["id"]

    response = client.get(f"/customers/{first_id}")

    assert response.status_code == 200
    assert response.json()["id"] == first_id
    assert "raw_payload" not in response.json()


def test_get_customer_by_id_returns_404_when_missing(client):
    response = client.get("/customers/999999")

    assert response.status_code == 404
