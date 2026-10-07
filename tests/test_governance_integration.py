from app.security.approval.manager import approval_manager
from app.security.governance.executor import governance_executor


def test_customer_delete_requires_approval():

    request_id = "REQ-DELETE-001"
    idempotency_key = "IDEMP-DELETE-001"

    calls = {"count": 0}

    def delete_customer():
        calls["count"] += 1
        return {
            "success": True,
            "customer_id": "C001",
            "message": "CUSTOMER_DELETED",
        }

    result = governance_executor.execute(
        user_id="U001",
        role="admin",
        tool_name="customer_delete",
        risk_level="HIGH",
        request_id=request_id,
        idempotency_key=idempotency_key,
        function=delete_customer,
    )

    assert result["success"] is False
    assert result["error"] == "APPROVAL_REQUIRED"
    assert result["status"] == "PENDING"

    # Tool must NOT execute before approval.
    assert calls["count"] == 0


def test_customer_delete_executes_after_approval():

    request_id = "REQ-DELETE-002"
    idempotency_key = "IDEMP-DELETE-002"

    calls = {"count": 0}

    def delete_customer():
        calls["count"] += 1
        return {
            "success": True,
            "customer_id": "C001",
            "message": "CUSTOMER_DELETED",
        }

    # Create approval request.
    approval_manager.create_request(
        request_id=request_id,
        user_id="U002",
        tool_name="customer_delete",
        reason="HIGH_RISK_OPERATION",
    )

    # Approve it.
    approval_manager.approve(request_id)

    result = governance_executor.execute(
        user_id="U002",
        role="admin",
        tool_name="customer_delete",
        risk_level="HIGH",
        request_id=request_id,
        idempotency_key=idempotency_key,
        function=delete_customer,
    )

    assert result["success"] is True
    assert result["data"]["success"] is True
    assert result["data"]["customer_id"] == "C001"
    assert calls["count"] == 1