from app.security.governance.executor import GovernanceExecutor
from app.validation.gateway_validator import gateway_validator
from app.validation.schemas import CustomerRequest


def test_governance_rejects_invalid_customer_request():
    gateway_validator.register_request_schema(
        "customer_update",
        CustomerRequest,
    )

    try:
        executor = GovernanceExecutor()

        result = executor.execute(
            user_id="user-001",
            role="admin",
            tool_name="customer_update",
            risk_level="MEDIUM",
            request_id="REQ-VALIDATION-001",
            idempotency_key="IDEMP-VALIDATION-001",
            function=lambda customer_id: {
                "customer_id": customer_id,
                "updated": True,
            },
            kwargs={
                "customer_id": "",
            },
        )

        assert result["success"] is False
        assert result["error"] == "REQUEST_VALIDATION_FAILED"

    finally:
        gateway_validator.request_schemas.pop(
            "customer_update",
            None,
        )


def test_governance_accepts_valid_customer_request():
    gateway_validator.register_request_schema(
        "customer_update",
        CustomerRequest,
    )

    try:
        executor = GovernanceExecutor()

        result = executor.execute(
            user_id="user-001",
            role="admin",
            tool_name="customer_update",
            risk_level="MEDIUM",
            request_id="REQ-VALIDATION-002",
            idempotency_key="IDEMP-VALIDATION-002",
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
        gateway_validator.request_schemas.pop(
            "customer_update",
            None,
        )


def test_governance_allows_unregistered_tool_schema():
    executor = GovernanceExecutor()

    result = executor.execute(
        user_id="user-001",
        role="support",
        tool_name="ticket_get",
        risk_level="LOW",
        request_id="REQ-VALIDATION-003",
        idempotency_key="IDEMP-VALIDATION-003",
        function=lambda ticket_id: {
            "ticket_id": ticket_id,
        },
        kwargs={
            "ticket_id": "TICKET-001",
        },
    )

    assert result["success"] is True
    assert result["data"]["ticket_id"] == "TICKET-001"