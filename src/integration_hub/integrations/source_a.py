from integration_hub.domain.schemas import CustomerCreate
from integration_hub.integrations.base import SourceAdapter

# Em produção isso viria de uma chamada HTTP a um CRM legado.
# Aqui simulamos o formato de resposta dele (campos em português, CPF com máscara).
_FAKE_SOURCE_A_RESPONSE = [
    {
        "customer_id": "A-001",
        "nome_completo": "Maria Silva",
        "email_contato": "maria.silva@example.com",
        "telefone": "+55 11 99999-0001",
        "cpf": "123.456.789-00",
    },
    {
        "customer_id": "A-002",
        "nome_completo": "João Pereira",
        "email_contato": "joao.pereira@example.com",
        "telefone": None,
        "cpf": "987.654.321-00",
    },
]


class SourceAAdapter(SourceAdapter):
    source_name = "source_a"

    def fetch_raw_customers(self) -> list[dict]:
        return _FAKE_SOURCE_A_RESPONSE

    def normalize(self, raw: dict) -> CustomerCreate:
        return CustomerCreate(
            source=self.source_name,
            external_id=raw["customer_id"],
            full_name=raw["nome_completo"],
            email=raw["email_contato"],
            phone=raw["telefone"],
            document=raw["cpf"],
            raw_payload=raw,
        )
