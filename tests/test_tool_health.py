import app.mcp_gateway.server  # noqa: F401

from app.observability.health import (
    _TOOL_STATS,
    get_tool_health,
    get_tool_health_status,
    record_tool_call,
)

def setup_function():
    """Reset health statistics before every test."""
    _TOOL_STATS.clear()


def test_initial_tool_health():
    result = get_tool_health_status("customer_get")

    assert result["tool_name"] == "customer_get"
    assert result["version"] == "1.0.0"
    assert result["enabled"] is True
    assert result["status"] == "HEALTHY"
    assert result["risk_level"] == "LOW"

    assert result["total_calls"] == 0
    assert result["successful_calls"] == 0
    assert result["failed_calls"] == 0
    assert result["success_rate"] == 0.0
    assert result["average_latency_ms"] == 0.0
    assert result["last_called"] is None


def test_record_successful_tool_call():
    record_tool_call(
        tool_name="customer_get",
        success=True,
        latency_ms=50.0,
    )

    result = get_tool_health_status("customer_get")

    assert result["total_calls"] == 1
    assert result["successful_calls"] == 1
    assert result["failed_calls"] == 0
    assert result["success_rate"] == 100.0
    assert result["average_latency_ms"] == 50.0
    assert result["last_called"] is not None


def test_record_failed_tool_call():
    record_tool_call(
        tool_name="customer_get",
        success=False,
        latency_ms=100.0,
    )

    result = get_tool_health_status("customer_get")

    assert result["total_calls"] == 1
    assert result["successful_calls"] == 0
    assert result["failed_calls"] == 1
    assert result["success_rate"] == 0.0
    assert result["average_latency_ms"] == 100.0
    assert result["last_called"] is not None


def test_success_rate():
    record_tool_call(
        tool_name="customer_get",
        success=True,
        latency_ms=20.0,
    )

    record_tool_call(
        tool_name="customer_get",
        success=True,
        latency_ms=30.0,
    )

    record_tool_call(
        tool_name="customer_get",
        success=False,
        latency_ms=40.0,
    )

    result = get_tool_health_status("customer_get")

    assert result["total_calls"] == 3
    assert result["successful_calls"] == 2
    assert result["failed_calls"] == 1
    assert result["success_rate"] == 66.67


def test_average_latency():
    record_tool_call(
        tool_name="customer_get",
        success=True,
        latency_ms=20.0,
    )

    record_tool_call(
        tool_name="customer_get",
        success=True,
        latency_ms=40.0,
    )

    result = get_tool_health_status("customer_get")

    assert result["total_calls"] == 2
    assert result["average_latency_ms"] == 30.0


def test_multiple_tool_health():
    record_tool_call(
        tool_name="customer_get",
        success=True,
        latency_ms=25.0,
    )

    record_tool_call(
        tool_name="ticket_get",
        success=False,
        latency_ms=75.0,
    )

    customer = get_tool_health_status("customer_get")
    ticket = get_tool_health_status("ticket_get")

    assert customer["total_calls"] == 1
    assert customer["successful_calls"] == 1

    assert ticket["total_calls"] == 1
    assert ticket["failed_calls"] == 1


def test_get_all_tool_health():
    record_tool_call(
        tool_name="customer_get",
        success=True,
        latency_ms=25.0,
    )

    health = get_tool_health()

    assert isinstance(health, list)
    assert len(health) >= 1

    customer_health = next(
        item
        for item in health
        if item["tool_name"] == "customer_get"
    )

    assert customer_health["total_calls"] == 1
    assert customer_health["successful_calls"] == 1
    assert customer_health["success_rate"] == 100.0