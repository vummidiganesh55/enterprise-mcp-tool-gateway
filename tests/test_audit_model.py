from datetime import datetime, timezone

from app.database.models.audit import AuditEvent


def test_audit_event_model():
    event = AuditEvent(
        timestamp=datetime.now(timezone.utc),
        user_id="user-001",
        role="admin",
        tool_name="customer_get",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-001",
        details={
            "latency_ms": 12.5,
        },
    )

    assert event.user_id == "user-001"
    assert event.role == "admin"
    assert event.tool_name == "customer_get"
    assert event.action == "TOOL_EXECUTION"
    assert event.success is True
    assert event.request_id == "REQ-001"
    assert event.details["latency_ms"] == 12.5


def test_audit_event_optional_fields():
    event = AuditEvent(
        user_id="user-002",
        role="support",
        tool_name="ticket_get",
        action="TOOL_EXECUTION",
        success=False,
    )

    assert event.user_id == "user-002"
    assert event.success is False
    assert event.request_id is None
    assert event.error_message is None
    assert event.details == {}