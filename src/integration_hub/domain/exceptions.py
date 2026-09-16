class DomainError(Exception):
    """Erro base de regra de negócio, independente de HTTP."""


class CustomerNotFoundError(DomainError):
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        super().__init__(f"Cliente {customer_id} não encontrado")
