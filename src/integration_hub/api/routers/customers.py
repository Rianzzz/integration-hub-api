from fastapi import APIRouter, HTTPException

from integration_hub.api.deps import CustomerRepositoryDep, CustomerSyncServiceDep
from integration_hub.domain.schemas import CustomerRead, SyncResult
from integration_hub.integrations.base import SourceAdapter
from integration_hub.integrations.source_a import SourceAAdapter
from integration_hub.integrations.source_b import SourceBAdapter
from integration_hub.integrations.source_c import SourceCAdapter

router = APIRouter(prefix="/customers", tags=["customers"])

_ADAPTERS: dict[str, type[SourceAdapter]] = {
    "source_a": SourceAAdapter,
    "source_b": SourceBAdapter,
    "source_c": SourceCAdapter,
}


@router.post("/sync", response_model=list[SyncResult])
def sync_all_sources(service: CustomerSyncServiceDep) -> list[SyncResult]:
    """Sincroniza todas as fontes registradas. Idempotente: pode rodar quantas vezes quiser."""
    return [service.sync(adapter_cls()) for adapter_cls in _ADAPTERS.values()]


@router.get("", response_model=list[CustomerRead])
def list_customers(repository: CustomerRepositoryDep) -> list[CustomerRead]:
    return repository.list_all()


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, repository: CustomerRepositoryDep) -> CustomerRead:
    customer = repository.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer
