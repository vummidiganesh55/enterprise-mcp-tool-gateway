from pydantic import BaseModel

from app.validation.gateway_validator import gateway_validator
from app.validation.schemas import CustomerRequest


def test_valid_customer_request():
    gateway_validator.register_request_schema(
        "customer_get",
        CustomerRequest,
    )

    try:
        result = gateway_validator.validate_request(
            tool_name="customer_get",
            data={
                "customer_id": "CUST-001",
            },
        )

        assert result["valid"] is True
        assert result["data"]["customer_id"] == "CUST-001"
        assert result["error"] is None

    finally:
        gateway_validator.request_schemas.pop(
            "customer_get",
            None,
        )


def test_invalid_customer_request():
    gateway_validator.register_request_schema(
        "customer_get",
        CustomerRequest,
    )

    try:
        result = gateway_validator.validate_request(
            tool_name="customer_get",
            data={
                "customer_id": "",
            },
        )

        assert result["valid"] is False
        assert result["data"] is None
        assert result["error"] is not None

    finally:
        gateway_validator.request_schemas.pop(
            "customer_get",
            None,
        )


def test_unknown_tool_schema_passes_through():
    data = {
        "ticket_id": "TICKET-001",
    }

    result = gateway_validator.validate_request(
        tool_name="ticket_get",
        data=data,
    )

    assert result["valid"] is True
    assert result["data"] == data


def test_response_without_schema_passes_through():
    data = {
        "success": True,
        "customer_id": "CUST-001",
    }

    result = gateway_validator.validate_response(
        data=data,
    )

    assert result["valid"] is True
    assert result["data"] == data


class CustomerResponse(BaseModel):
    success: bool
    customer_id: str


def test_valid_response():
    result = gateway_validator.validate_response(
        data={
            "success": True,
            "customer_id": "CUST-001",
        },
        response_model=CustomerResponse,
    )

    assert result["valid"] is True
    assert result["data"]["customer_id"] == "CUST-001"


def test_invalid_response():
    result = gateway_validator.validate_response(
        data={
            "success": "invalid",
            "customer_id": "CUST-001",
        },
        response_model=CustomerResponse,
    )

    assert result["valid"] is False
    assert result["data"] is None
    assert result["error"] is not None