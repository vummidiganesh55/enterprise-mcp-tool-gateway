from app.security.governance.executor import (
    GovernanceExecutor,
)


def test_authorized_low_risk_tool_executes():

    executor = GovernanceExecutor()

    calls = {"count": 0}

    def tool():
        calls["count"] += 1
        return {
            "message": "success",
        }

    result = executor.execute(
        user_id="U001",
        role="support",
        tool_name="customer_get",
        risk_level="LOW",
        request_id="REQ-GOV-001",
        idempotency_key="IDEMP-GOV-001",
        function=tool,
    )

    assert result["success"] is True
    assert result["data"]["message"] == "success"
    assert calls["count"] == 1


def test_unauthorized_tool_is_denied():

    executor = GovernanceExecutor()

    calls = {"count": 0}

    def tool():
        calls["count"] += 1
        return {
            "message": "should_not_execute",
        }

    result = executor.execute(
        user_id="U002",
        role="viewer",
        tool_name="customer_update",
        risk_level="MEDIUM",
        request_id="REQ-GOV-002",
        idempotency_key="IDEMP-GOV-002",
        function=tool,
    )

    assert result["success"] is False
    assert result["error"] == "AUTHORIZATION_DENIED"
    assert calls["count"] == 0


def test_high_risk_requires_approval():

    executor = GovernanceExecutor()

    calls = {"count": 0}

    def tool():
        calls["count"] += 1
        return {
            "message": "deleted",
        }

    result = executor.execute(
        user_id="U003",
        role="admin",
        tool_name="customer_delete",
        risk_level="HIGH",
        request_id="REQ-GOV-003",
        idempotency_key="IDEMP-GOV-003",
        function=tool,
    )

    assert result["success"] is False
    assert result["error"] == "APPROVAL_REQUIRED"
    assert result["status"] == "PENDING"
    assert calls["count"] == 0


def test_approved_high_risk_tool_executes():

    executor = GovernanceExecutor()

    calls = {"count": 0}

    def tool():
        calls["count"] += 1
        return {
            "message": "deleted",
        }

    request_id = "REQ-GOV-004"

    # Create approval request
    from app.security.approval.manager import approval_manager

    approval_manager.create_request(
        request_id=request_id,
        user_id="U004",
        tool_name="customer_delete",
        reason="HIGH_RISK_OPERATION",
    )

    # Approve request
    approval_manager.approve(request_id)

    result = executor.execute(
        user_id="U004",
        role="admin",
        tool_name="customer_delete",
        risk_level="HIGH",
        request_id=request_id,
        idempotency_key="IDEMP-GOV-004",
        function=tool,
    )

    assert result["success"] is True
    assert result["data"]["message"] == "deleted"
    assert calls["count"] == 1


def test_idempotent_execution_runs_once():

    executor = GovernanceExecutor()

    calls = {"count": 0}

    def tool():
        calls["count"] += 1
        return {
            "message": "executed",
        }

    first = executor.execute(
        user_id="U005",
        role="support",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-GOV-005",
        idempotency_key="IDEMP-GOV-005",
        function=tool,
    )

    second = executor.execute(
        user_id="U005",
        role="support",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-GOV-006",
        idempotency_key="IDEMP-GOV-005",
        function=tool,
    )

    assert first["success"] is True
    assert second["success"] is True
    assert first["data"] == second["data"]

    # The actual tool must execute only once.
    assert calls["count"] == 1