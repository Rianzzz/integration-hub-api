from integration_hub.domain.models import Customer


def test_customer_maps_to_customers_table():
    assert Customer.__tablename__ == "customers"


def test_customer_has_unique_constraint_on_source_and_external_id():
    constraint_names = {c.name for c in Customer.__table__.constraints}

    assert "uq_customer_source_external_id" in constraint_names
