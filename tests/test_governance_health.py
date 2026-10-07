import app.mcp_gateway.server  # noqa: F401

from app.observability.health import (
    _TOOL_STATS,
    get_tool_health_status,
)
from app.security.governance.executor import (
    governance_executor,
)


def setup_function():
    _TOOL_STATS.clear()


def test_successful_tool_updates_health():

    def test_tool():
        return {
            "success": True,
            "message": "OK",
        }

    result = governance_executor.execute(
        user_id="U-HEALTH-001",
        role="support",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-HEALTH-001",
        idempotency_key="IDEMP-HEALTH-001",
        function=test_tool,
    )

    assert result["success"] is True

    health = get_tool_health_status(
        "ticket_create"
    )

    assert health["total_calls"] == 1
    assert health["successful_calls"] == 1
    assert health["failed_calls"] == 0
    assert health["success_rate"] == 100.0
    assert health["average_latency_ms"] >= 0
    assert health["last_called"] is not None


def test_failed_tool_updates_health():

    def failing_tool():
        raise RuntimeError(
            "TEST_TOOL_FAILURE"
        )

    result = governance_executor.execute(
        user_id="U-HEALTH-002",
        role="support",
        tool_name="ticket_create",
        risk_level="MEDIUM",
        request_id="REQ-HEALTH-002",
        idempotency_key="IDEMP-HEALTH-002",
        function=failing_tool,
    )

    assert result["success"] is False
    assert result["error"] == "TEST_TOOL_FAILURE"

    health = get_tool_health_status(
        "ticket_create"
    )

    assert health["total_calls"] == 1
    assert health["successful_calls"] == 0
    assert health["failed_calls"] == 1
    assert health["success_rate"] == 0.0
    assert health["average_latency_ms"] >= 0
    assert health["last_called"] is not None