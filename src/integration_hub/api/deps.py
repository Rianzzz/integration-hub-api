from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from integration_hub.core.database import get_db
from integration_hub.core.security import decode_access_token
from integration_hub.domain.exceptions import InvalidCredentialsError
from integration_hub.repositories.customer_repository import CustomerRepository
from integration_hub.services.customer_sync_service import CustomerSyncService

DbSession = Annotated[Session, Depends(get_db)]

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: Annotated[str, Depends(_oauth2_scheme)]) -> str:
    try:
        return decode_access_token(token)
    except jwt.PyJWTError as exc:
        raise InvalidCredentialsError("Token inválido ou expirado") from exc


CurrentUserDep = Annotated[str, Depends(get_current_user)]


def get_customer_repository(db: DbSession) -> CustomerRepository:
    return CustomerRepository(db)


CustomerRepositoryDep = Annotated[CustomerRepository, Depends(get_customer_repository)]


def get_customer_sync_service(repository: CustomerRepositoryDep) -> CustomerSyncService:
    return CustomerSyncService(repository)


CustomerSyncServiceDep = Annotated[CustomerSyncService, Depends(get_customer_sync_service)]
