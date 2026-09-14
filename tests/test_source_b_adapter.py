from integration_hub.integrations.source_b import SourceBAdapter


def test_normalize_extracts_nested_contact_fields():
    adapter = SourceBAdapter()
    raw = {
        "id": "B-1001",
        "name": "Maria Silva",
        "contact": {"email": "maria.silva@example.com", "phone": "11999990001"},
        "tax_id": "12345678900",
    }

    customer = adapter.normalize(raw)

    assert customer.source == "source_b"
    assert customer.external_id == "B-1001"
    assert customer.email == "maria.silva@example.com"
    assert customer.phone == "11999990001"
    assert customer.raw_payload == raw


def test_normalize_handles_missing_optional_fields():
    adapter = SourceBAdapter()
    raw = {
        "id": "B-1002",
        "name": "Ana Costa",
        "contact": {"email": "ana.costa@example.com", "phone": None},
        "tax_id": None,
    }

    customer = adapter.normalize(raw)

    assert customer.phone is None
    assert customer.document is None


def test_fetch_customers_normalizes_every_record():
    adapter = SourceBAdapter()

    customers = adapter.fetch_customers()

    assert len(customers) == 2
    assert all(c.source == "source_b" for c in customers)
