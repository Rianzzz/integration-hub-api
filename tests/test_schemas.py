from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from integration_hub.domain.schemas import CustomerCreate, CustomerRead


def test_customer_create_rejects_invalid_email():
    with pytest.raises(ValidationError):
        CustomerCreate(
            source="source_a",
            external_id="123",
            full_name="Maria Silva",
            email="nao-eh-um-email",
            raw_payload={},
        )


def test_customer_read_builds_from_object_attributes():
    class FakeCustomerRow:
        id = 1
        source = "source_a"
        external_id = "123"
        full_name = "Maria Silva"
        email = "maria@example.com"
        phone = None
        document = None
        created_at = datetime.now(UTC)
        updated_at = datetime.now(UTC)

    customer = CustomerRead.model_validate(FakeCustomerRow())

    assert customer.full_name == "Maria Silva"
