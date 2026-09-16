import pytest

from integration_hub.domain.schemas import CustomerCreate
from integration_hub.integrations.base import SourceAdapter


class FlakyAdapter(SourceAdapter):
    """Adapter de teste que simula uma fonte externa instável."""

    source_name = "flaky"

    def __init__(self, fail_times: int):
        self._fail_times = fail_times
        self.attempts = 0

    def fetch_raw_customers(self) -> list[dict]:
        self.attempts += 1
        if self.attempts <= self._fail_times:
            raise ConnectionError("fonte externa instavel")
        return [{"id": "1", "name": "Teste", "email": "teste@example.com"}]

    def normalize(self, raw: dict) -> CustomerCreate:
        return CustomerCreate(
            source=self.source_name,
            external_id=raw["id"],
            full_name=raw["name"],
            email=raw["email"],
            raw_payload=raw,
        )


def test_fetch_customers_retries_and_succeeds_after_transient_failures():
    adapter = FlakyAdapter(fail_times=2)

    customers = adapter.fetch_customers()

    assert len(customers) == 1
    assert adapter.attempts == 3


def test_fetch_customers_raises_after_exhausting_retries():
    adapter = FlakyAdapter(fail_times=10)

    with pytest.raises(ConnectionError):
        adapter.fetch_customers()

    assert adapter.attempts == 3


def test_fetch_customers_does_not_retry_on_unexpected_errors():
    class BrokenAdapter(FlakyAdapter):
        def fetch_raw_customers(self) -> list[dict]:
            self.attempts += 1
            raise ValueError("erro de programacao, nao deveria ser retentado")

    adapter = BrokenAdapter(fail_times=0)

    with pytest.raises(ValueError):
        adapter.fetch_customers()

    assert adapter.attempts == 1
