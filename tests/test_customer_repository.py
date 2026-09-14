from integration_hub.domain.schemas import CustomerCreate
from integration_hub.repositories.customer_repository import CustomerRepository


def make_customer_data(**overrides) -> CustomerCreate:
    defaults = {
        "source": "source_a",
        "external_id": "ext-1",
        "full_name": "Maria Silva",
        "email": "maria@example.com",
        "phone": None,
        "document": None,
        "raw_payload": {"raw": True},
    }
    defaults.update(overrides)
    return CustomerCreate(**defaults)


def test_create_persists_customer(db_session):
    repository = CustomerRepository(db_session)

    customer = repository.create(make_customer_data())

    assert customer.id is not None
    assert customer.full_name == "Maria Silva"


def test_get_by_source_and_external_id_finds_existing_customer(db_session):
    repository = CustomerRepository(db_session)
    repository.create(make_customer_data(external_id="ext-2"))

    found = repository.get_by_source_and_external_id("source_a", "ext-2")

    assert found is not None
    assert found.external_id == "ext-2"


def test_get_by_source_and_external_id_returns_none_when_missing(db_session):
    repository = CustomerRepository(db_session)

    found = repository.get_by_source_and_external_id("source_a", "does-not-exist")

    assert found is None


def test_list_all_returns_created_customers(db_session):
    repository = CustomerRepository(db_session)
    repository.create(make_customer_data(external_id="ext-3"))

    customers = repository.list_all()

    assert len(customers) == 1


def test_update_changes_existing_customer_fields(db_session):
    repository = CustomerRepository(db_session)
    customer = repository.create(make_customer_data(external_id="ext-4"))

    updated = repository.update(
        customer, make_customer_data(external_id="ext-4", full_name="Maria Souza")
    )

    assert updated.full_name == "Maria Souza"
