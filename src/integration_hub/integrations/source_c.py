from integration_hub.domain.schemas import CustomerCreate
from integration_hub.integrations.base import SourceAdapter

# Simula um sistema de suporte/atendimento: cadastro mínimo, sem telefone
# nem documento — só o essencial pra abrir um chamado.
_FAKE_SOURCE_C_RESPONSE = [
    {
        "user_ref": "C-55",
        "full_name": "Maria Silva",
        "primary_email": "maria.silva@example.com",
    },
    {
        "user_ref": "C-56",
        "full_name": "Carlos Souza",
        "primary_email": "carlos.souza@example.com",
    },
]


class SourceCAdapter(SourceAdapter):
    source_name = "source_c"

    def fetch_raw_customers(self) -> list[dict]:
        return _FAKE_SOURCE_C_RESPONSE

    def normalize(self, raw: dict) -> CustomerCreate:
        return CustomerCreate(
            source=self.source_name,
            external_id=raw["user_ref"],
            full_name=raw["full_name"],
            email=raw["primary_email"],
            phone=None,
            document=None,
            raw_payload=raw,
        )
