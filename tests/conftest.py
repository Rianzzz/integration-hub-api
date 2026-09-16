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

    yield TestClient(app)

    app.dependency_overrides.clear()
