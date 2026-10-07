from app.security.approval.manager import approval_manager
from app.security.governance.executor import governance_executor


def test_mcp_customer_delete_after_approval():

    request_id = "REQ-MCP-DELETE-002"
    idempotency_key = "IDEMP-MCP-DELETE-002"

    # First create the approval request.
    approval_manager.create_request(
        request_id=request_id,
        user_id="U001",
        tool_name="customer_delete",
        reason="HIGH_RISK_OPERATION",
    )

    # Approve the request.
    approval = approval_manager.approve(request_id)

    assert approval.status == "APPROVED"

    # Execute the governed operation.
    def delete_customer():
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

    assert result["success"] is True
    assert result["data"]["success"] is True
    assert result["data"]["customer_id"] == "C001"