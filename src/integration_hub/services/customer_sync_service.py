import logging

from integration_hub.domain.schemas import SyncResult
from integration_hub.integrations.base import SourceAdapter
from integration_hub.repositories.customer_repository import CustomerRepository

logger = logging.getLogger(__name__)


class CustomerSyncService:
    """Decide se cada cliente vindo do adapter deve ser criado ou atualizado."""

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def sync(self, adapter: SourceAdapter) -> SyncResult:
        logger.info("Iniciando sincronizacao da fonte %s", adapter.source_name)
        created = 0
        updated = 0

        for customer_data in adapter.fetch_customers():
            existing = self._repository.get_by_source_and_external_id(
                customer_data.source, customer_data.external_id
            )
            if existing:
                self._repository.update(existing, customer_data)
                updated += 1
            else:
                self._repository.create(customer_data)
                created += 1

        logger.info(
            "Sincronizacao da fonte %s concluida: %d criados, %d atualizados",
            adapter.source_name,
            created,
            updated,
        )
        return SyncResult(source=adapter.source_name, created=created, updated=updated)
