import pytest
from fastapi.testclient import TestClient

from integration_hub.core.database import SessionLocal, get_db
from integration_hub.domain.models import Customer
from integration_hub.main import app


@pytest.fixture
def db_session():
    """Sessão contra o Postgres real, limpa depois de cada teste."""
    session = SessionLocal()

    yield session

    session.rollback()
    session.query(Customer).delete()
    session.commit()
    session.close()


@pytest.fixture
def client(db_session):
    """TestClient da API, usando a mesma sessão de teste (com a mesma limpeza automática)."""
    app.dependency_overrides[get_db] = lambda: db_session

    # raise_server_exceptions=False: quando testamos um 500, queremos a resposta
    # JSON de verdade, nao a excecao original relancada pelo TestClient.
    yield TestClient(app, raise_server_exceptions=False)

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Header Authorization pronto pra uso em rotas protegidas por JWT."""
    token = client.post(
        "/auth/token", data={"username": "admin", "password": "admin"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
