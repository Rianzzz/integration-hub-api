from integration_hub.api.deps import get_customer_repository
from integration_hub.main import app


def test_unexpected_error_returns_500_without_leaking_details(client):
    def broken_repository():
        raise RuntimeError("falha interna que nao deveria vazar")

    app.dependency_overrides[get_customer_repository] = broken_repository

    response = client.get("/customers/1")

    app.dependency_overrides.pop(get_customer_repository, None)

    assert response.status_code == 500
    assert response.json() == {"detail": "Erro interno inesperado"}


def test_customer_not_found_returns_404_with_message(client):
    response = client.get("/customers/999999")

    assert response.status_code == 404
    assert "999999" in response.json()["detail"]
