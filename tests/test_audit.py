import json
import logging

from app.security.audit.audit_logger import audit_event


def test_customer_update_audit(caplog):
    with caplog.at_level(logging.INFO, logger="mcp.audit"):
        audit_event(
            user_id="U001",
            role="support",
            tool_name="customer_update",
            action="UPDATE",
            success=True,
            request_id="REQ001",
            details={
                "customer_id": "C001",
            },
        )

    assert len(caplog.records) >= 1

    event = json.loads(caplog.records[-1].message)

    assert event["user_id"] == "U001"
    assert event["role"] == "support"
    assert event["tool_name"] == "customer_update"
    assert event["action"] == "UPDATE"
    assert event["success"] is True
    assert event["request_id"] == "REQ001"
    assert event["details"]["customer_id"] == "C001"


def test_customer_delete_failed_audit(caplog):
    with caplog.at_level(logging.INFO, logger="mcp.audit"):
        audit_event(
            user_id="U002",
            role="support",
            tool_name="customer_delete",
            action="DELETE",
            success=False,
            request_id="REQ002",
            details={
                "reason": "AUTHORIZATION_DENIED",
            },
        )

    event = json.loads(caplog.records[-1].message)

    assert event["user_id"] == "U002"
    assert event["role"] == "support"
    assert event["tool_name"] == "customer_delete"
    assert event["action"] == "DELETE"
    assert event["success"] is False
    assert event["details"]["reason"] == "AUTHORIZATION_DENIED"


def test_ticket_create_audit(caplog):
    with caplog.at_level(logging.INFO, logger="mcp.audit"):
        audit_event(
            user_id="U003",
            role="support",
            tool_name="ticket_create",
            action="CREATE",
            success=True,
            request_id="REQ003",
            details={
                "customer_id": "C001",
                "priority": "HIGH",
            },
        )

    event = json.loads(caplog.records[-1].message)

    assert event["tool_name"] == "ticket_create"
    assert event["action"] == "CREATE"
    assert event["success"] is True
    assert event["details"]["priority"] == "HIGH"