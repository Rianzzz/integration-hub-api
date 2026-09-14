from integration_hub.integrations.source_c import SourceCAdapter


def test_normalize_maps_minimal_fields_and_defaults_optionals_to_none():
    adapter = SourceCAdapter()
    raw = {
        "user_ref": "C-55",
        "full_name": "Maria Silva",
        "primary_email": "maria.silva@example.com",
    }

    customer = adapter.normalize(raw)

    assert customer.source == "source_c"
    assert customer.external_id == "C-55"
    assert customer.email == "maria.silva@example.com"
    assert customer.phone is None
    assert customer.document is None
    assert customer.raw_payload == raw


def test_fetch_customers_normalizes_every_record():
    adapter = SourceCAdapter()

    customers = adapter.fetch_customers()

    assert len(customers) == 2
    assert all(c.source == "source_c" for c in customers)
