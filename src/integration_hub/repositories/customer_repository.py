from sqlalchemy import select
from sqlalchemy.orm import Session

from integration_hub.domain.models import Customer
from integration_hub.domain.schemas import CustomerCreate


class CustomerRepository:
    """Única camada que fala com a tabela customers."""

    def __init__(self, db: Session):
        self._db = db

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self._db.get(Customer, customer_id)

    def get_by_source_and_external_id(self, source: str, external_id: str) -> Customer | None:
        stmt = select(Customer).where(
            Customer.source == source, Customer.external_id == external_id
        )
        return self._db.scalars(stmt).first()

    def list_all(self) -> list[Customer]:
        return list(self._db.scalars(select(Customer)).all())

    def create(self, data: CustomerCreate) -> Customer:
        customer = Customer(**data.model_dump())
        self._db.add(customer)
        self._db.commit()
        self._db.refresh(customer)
        return customer

    def update(self, customer: Customer, data: CustomerCreate) -> Customer:
        for field, value in data.model_dump().items():
            setattr(customer, field, value)
        self._db.commit()
        self._db.refresh(customer)
        return customer
