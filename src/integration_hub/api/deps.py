from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from integration_hub.core.database import get_db
from integration_hub.repositories.customer_repository import CustomerRepository
from integration_hub.services.customer_sync_service import CustomerSyncService

DbSession = Annotated[Session, Depends(get_db)]


def get_customer_repository(db: DbSession) -> CustomerRepository:
    return CustomerRepository(db)


CustomerRepositoryDep = Annotated[CustomerRepository, Depends(get_customer_repository)]


def get_customer_sync_service(repository: CustomerRepositoryDep) -> CustomerSyncService:
    return CustomerSyncService(repository)


CustomerSyncServiceDep = Annotated[CustomerSyncService, Depends(get_customer_sync_service)]
