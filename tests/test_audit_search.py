from app.security.audit.audit_logger import AUDIT_EVENTS, audit_event
from app.tools.governance.audit_search import search_audit_events


def setup_function():
    AUDIT_EVENTS.clear()


def test_search_by_tool_name():

    audit_event(
        user_id="U001",
        role="support",
        tool_name="customer_get",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-001",
    )

    audit_event(
        user_id="U002",
        role="support",
        tool_name="ticket_create",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-002",
    )

    result = search_audit_events(
        tool_name="customer_get"
    )

    assert result["success"] is True
    assert result["count"] == 1
    assert result["results"][0]["tool_name"] == "customer_get"


def test_search_by_user_id():

    audit_event(
        user_id="U001",
        role="support",
        tool_name="customer_get",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-003",
    )

    audit_event(
        user_id="U002",
        role="admin",
        tool_name="customer_update",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-004",
    )

    result = search_audit_events(
        user_id="U001"
    )

    assert result["success"] is True
    assert result["count"] == 1
    assert result["results"][0]["user_id"] == "U001"


def test_search_by_success():

    audit_event(
        user_id="U001",
        role="support",
        tool_name="customer_get",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-005",
    )

    audit_event(
        user_id="U002",
        role="viewer",
        tool_name="customer_update",
        action="AUTHORIZATION_DENIED",
        success=False,
        request_id="REQ-006",
    )

    result = search_audit_events(
        success=False
    )

    assert result["success"] is True
    assert result["count"] == 1
    assert result["results"][0]["success"] is False


def test_search_multiple_filters():

    audit_event(
        user_id="U001",
        role="support",
        tool_name="ticket_create",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-007",
    )

    audit_event(
        user_id="U002",
        role="support",
        tool_name="ticket_create",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-008",
    )

    result = search_audit_events(
        tool_name="ticket_create",
        user_id="U001",
        success=True,
    )

    assert result["success"] is True
    assert result["count"] == 1
    assert result["results"][0]["user_id"] == "U001"


def test_search_no_matching_events():

    audit_event(
        user_id="U001",
        role="support",
        tool_name="customer_get",
        action="TOOL_EXECUTION",
        success=True,
        request_id="REQ-009",
    )

    result = search_audit_events(
        tool_name="unknown_tool"
    )

    assert result["success"] is True
    assert result["count"] == 0
    assert result["results"] == []