from integration_hub.domain.schemas import CustomerCreate
from integration_hub.integrations.base import SourceAdapter

# Simula uma plataforma de e-commerce: contato aninhado em um sub-objeto,
# documento fiscal sem máscara.
_FAKE_SOURCE_B_RESPONSE = [
    {
        "id": "B-1001",
        "name": "Maria Silva",
        "contact": {"email": "maria.silva@example.com", "phone": "11999990001"},
        "tax_id": "12345678900",
    },
    {
        "id": "B-1002",
        "name": "Ana Costa",
        "contact": {"email": "ana.costa@example.com", "phone": None},
        "tax_id": None,
    },
]


class SourceBAdapter(SourceAdapter):
    source_name = "source_b"

    def fetch_raw_customers(self) -> list[dict]:
        return _FAKE_SOURCE_B_RESPONSE

    def normalize(self, raw: dict) -> CustomerCreate:
        return CustomerCreate(
            source=self.source_name,
            external_id=raw["id"],
            full_name=raw["name"],
            email=raw["contact"]["email"],
            phone=raw["contact"]["phone"],
            document=raw["tax_id"],
            raw_payload=raw,
        )
