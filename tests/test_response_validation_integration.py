from pydantic import BaseModel

from app.security.governance.executor import GovernanceExecutor
from app.validation.gateway_validator import gateway_validator


class CustomerResponse(BaseModel):
    customer_id: str
    updated: bool


def test_governance_accepts_valid_response():

    gateway_validator.register_response_schema(
        "customer_update",
        CustomerResponse,
    )

    try:
        executor = GovernanceExecutor()

        result = executor.execute(
            user_id="user-001",
            role="admin",
            tool_name="customer_update",
            risk_level="MEDIUM",
            request_id="REQ-RESPONSE-001",
            idempotency_key="IDEMP-RESPONSE-001",
            function=lambda customer_id: {
                "customer_id": customer_id,
                "updated": True,
            },
            kwargs={
                "customer_id": "CUST-001",
            },
        )

        assert result["success"] is True
        assert result["data"]["customer_id"] == "CUST-001"

    finally:
        gateway_validator.response_schemas.pop(
            "customer_update",
            None,
        )


def test_governance_rejects_invalid_response():

    gateway_validator.register_response_schema(
        "customer_update",
        CustomerResponse,
    )

    try:
        executor = GovernanceExecutor()

        result = executor.execute(
            user_id="user-001",
            role="admin",
            tool_name="customer_update",
            risk_level="MEDIUM",
            request_id="REQ-RESPONSE-002",
            idempotency_key="IDEMP-RESPONSE-002",
            function=lambda customer_id: {
                "customer_id": customer_id,
                "updated": "INVALID",
            },
            kwargs={
                "customer_id": "CUST-001",
            },
        )

        assert result["success"] is False
        assert result["error"] == "RESPONSE_VALIDATION_FAILED"

    finally:
        gateway_validator.response_schemas.pop(
            "customer_update",
            None,
        )


def test_governance_allows_tool_without_response_schema():

    executor = GovernanceExecutor()

    result = executor.execute(
        user_id="user-001",
        role="support",
        tool_name="ticket_get",
        risk_level="LOW",
        request_id="REQ-RESPONSE-003",
        idempotency_key="IDEMP-RESPONSE-003",
        function=lambda ticket_id: {
            "ticket_id": ticket_id,
        },
        kwargs={
            "ticket_id": "TICKET-001",
        },
    )

    assert result["success"] is True
    assert result["data"]["ticket_id"] == "TICKET-001"