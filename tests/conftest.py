import pytest

from integration_hub.core.database import SessionLocal
from integration_hub.domain.models import Customer


@pytest.fixture
def db_session():
    """Sessão contra o Postgres real, limpa depois de cada teste."""
    session = SessionLocal()

    yield session

    session.rollback()
    session.query(Customer).delete()
    session.commit()
    session.close()
