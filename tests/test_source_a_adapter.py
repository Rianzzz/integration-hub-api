from integration_hub.integrations.source_a import SourceAAdapter


def test_normalize_maps_portuguese_fields_to_domain_schema():
    adapter = SourceAAdapter()
    raw = {
        "customer_id": "A-001",
        "nome_completo": "Maria Silva",
        "email_contato": "maria.silva@example.com",
        "telefone": "+55 11 99999-0001",
        "cpf": "123.456.789-00",
    }

    customer = adapter.normalize(raw)

    assert customer.source == "source_a"
    assert customer.external_id == "A-001"
    assert customer.full_name == "Maria Silva"
    assert customer.email == "maria.silva@example.com"
    assert customer.document == "123.456.789-00"
    assert customer.raw_payload == raw


def test_fetch_customers_normalizes_every_record():
    adapter = SourceAAdapter()

    customers = adapter.fetch_customers()

    assert len(customers) == 2
    assert all(c.source == "source_a" for c in customers)
