from integration_hub.integrations.source_a import SourceAAdapter
from integration_hub.repositories.customer_repository import CustomerRepository
from integration_hub.services.customer_sync_service import CustomerSyncService


def test_sync_creates_new_customers(db_session):
    repository = CustomerRepository(db_session)
    service = CustomerSyncService(repository)

    result = service.sync(SourceAAdapter())

    assert result.created == 2
    assert result.updated == 0
    assert result.total == 2
    assert len(repository.list_all()) == 2


def test_sync_is_idempotent_and_updates_on_second_run(db_session):
    repository = CustomerRepository(db_session)
    service = CustomerSyncService(repository)
    service.sync(SourceAAdapter())

    result = service.sync(SourceAAdapter())

    assert result.created == 0
    assert result.updated == 2
    assert len(repository.list_all()) == 2
