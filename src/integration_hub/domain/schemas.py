from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, computed_field


class CustomerCreate(BaseModel):
    """Dado já normalizado, pronto para ser persistido pelo repository."""

    source: str
    external_id: str
    full_name: str
    email: EmailStr
    phone: str | None = None
    document: str | None = None
    raw_payload: dict


class CustomerRead(BaseModel):
    """Formato de saída da API. Não expõe o raw_payload por padrão."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    external_id: str
    full_name: str
    email: EmailStr
    phone: str | None
    document: str | None
    created_at: datetime
    updated_at: datetime


class SyncResult(BaseModel):
    """Resumo de uma sincronização: quantos clientes foram criados vs. atualizados."""

    source: str
    created: int
    updated: int

    @computed_field
    @property
    def total(self) -> int:
        return self.created + self.updated
