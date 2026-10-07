from pydantic import BaseModel

from app.validation.request_validator import validate_customer_request
from app.validation.response_validator import validate_response
from app.validation.schemas import ToolRequest

def test_valid_customer_request():
    result = validate_customer_request(
        {
            "customer_id": "CUST-001",
        }
    )

    assert result["valid"] is True
    assert result["data"]["customer_id"] == "CUST-001"
    assert result["error"] is None


def test_invalid_customer_request_empty_id():
    result = validate_customer_request(
        {
            "customer_id": "",
        }
    )

    assert result["valid"] is False
    assert result["data"] is None
    assert result["error"] is not None


def test_invalid_customer_request_missing_id():
    result = validate_customer_request({})

    assert result["valid"] is False
    assert result["data"] is None
    assert result["error"] is not None


def test_customer_id_max_length():
    result = validate_customer_request(
        {
            "customer_id": "A" * 50,
        }
    )

    assert result["valid"] is True


def test_customer_id_exceeds_max_length():
    result = validate_customer_request(
        {
            "customer_id": "A" * 51,
        }
    )

    assert result["valid"] is False


class CustomerResponse(BaseModel):
    customer_id: str
    name: str


def test_valid_response():
    result = validate_response(
        {
            "customer_id": "CUST-001",
            "name": "John",
        },
        CustomerResponse,
    )

    assert result["valid"] is True
    assert result["data"]["customer_id"] == "CUST-001"
    assert result["error"] is None


def test_invalid_response():
    result = validate_response(
        {
            "customer_id": "CUST-001",
        },
        CustomerResponse,
    )

    assert result["valid"] is False
    assert result["data"] is None
    assert result["error"] is not None
def test_valid_tool_request():
    request = ToolRequest(
        tool_name="customer_get",
        arguments={
            "customer_id": "CUST-001",
        },
    )

    assert request.tool_name == "customer_get"
    assert request.arguments["customer_id"] == "CUST-001"


def test_invalid_tool_request_empty_tool_name():
    try:
        ToolRequest(
            tool_name="",
            arguments={},
        )
        assert False, "Expected validation error"
    except Exception:
        assert True