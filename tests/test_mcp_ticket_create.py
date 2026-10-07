from app.security.governance.executor import governance_executor


def test_ticket_create_support_allowed():
    def create_ticket():
        return {
            "success": True,
            "ticket_id": "T-TEST-001",
            "customer_id": "C001",
            "subject": "Payment issue",
            "priority": "HIGH",
            "status": "OPEN",
        }

    result = governance_executor.execute(
        user_id="U001",
        role="support",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-TICKET-001",
        idempotency_key="IDEMP-TICKET-001",
        function=create_ticket,
    )

    assert result["success"] is True
    assert result["data"]["success"] is True
    assert result["data"]["ticket_id"] == "T-TEST-001"


def test_ticket_create_admin_allowed():
    def create_ticket():
        return {
            "success": True,
            "ticket_id": "T-TEST-002",
            "customer_id": "C002",
            "subject": "Refund request",
            "priority": "MEDIUM",
            "status": "OPEN",
        }

    result = governance_executor.execute(
        user_id="U002",
        role="admin",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-TICKET-002",
        idempotency_key="IDEMP-TICKET-002",
        function=create_ticket,
    )

    assert result["success"] is True
    assert result["data"]["ticket_id"] == "T-TEST-002"


def test_ticket_create_viewer_denied():
    def create_ticket():
        return {
            "success": True,
            "ticket_id": "T-TEST-003",
        }

    result = governance_executor.execute(
        user_id="U003",
        role="viewer",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-TICKET-003",
        idempotency_key="IDEMP-TICKET-003",
        function=create_ticket,
    )

    assert result["success"] is False
    assert result["error"] == "AUTHORIZATION_DENIED"


def test_ticket_create_idempotency():
    call_count = {"value": 0}

    def create_ticket():
        call_count["value"] += 1

        return {
            "success": True,
            "ticket_id": "T-IDEMP-001",
        }

    first_result = governance_executor.execute(
        user_id="U001",
        role="support",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-TICKET-004",
        idempotency_key="IDEMP-TICKET-SAME",
        function=create_ticket,
    )

    second_result = governance_executor.execute(
        user_id="U001",
        role="support",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-TICKET-005",
        idempotency_key="IDEMP-TICKET-SAME",
        function=create_ticket,
    )

    assert first_result["success"] is True
    assert second_result["success"] is True

    assert first_result["data"] == second_result["data"]
    assert call_count["value"] == 1