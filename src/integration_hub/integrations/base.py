from abc import ABC, abstractmethod

from integration_hub.domain.schemas import CustomerCreate


class SourceAdapter(ABC):
    """Contrato que todo adapter de fonte externa precisa seguir."""

    source_name: str

    @abstractmethod
    def fetch_raw_customers(self) -> list[dict]:
        """Busca os dados brutos da fonte externa, no formato dela."""

    @abstractmethod
    def normalize(self, raw: dict) -> CustomerCreate:
        """Converte um registro bruto da fonte para o formato único do domínio."""

    def fetch_customers(self) -> list[CustomerCreate]:
        return [self.normalize(raw) for raw in self.fetch_raw_customers()]
