import logging
from abc import ABC, abstractmethod

from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_fixed

from integration_hub.domain.schemas import CustomerCreate

logger = logging.getLogger(__name__)


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
        raw_customers = self._fetch_raw_customers_with_retry()
        return [self.normalize(raw) for raw in raw_customers]

    def _fetch_raw_customers_with_retry(self) -> list[dict]:
        """Chamadas a fontes externas podem falhar de forma transitória (timeout, instabilidade
        de rede). Tenta até 3 vezes antes de desistir, o que fica implementado uma vez só aqui
        e vale pra qualquer adapter, sem cada um precisar lidar com isso."""
        retryer = Retrying(
            stop=stop_after_attempt(3),
            wait=wait_fixed(0.2),
            retry=retry_if_exception_type(ConnectionError),
            reraise=True,
            before_sleep=lambda state: logger.warning(
                "Tentativa %d de buscar dados da fonte %s falhou, tentando de novo",
                state.attempt_number,
                self.source_name,
            ),
        )
        return retryer(self.fetch_raw_customers)
