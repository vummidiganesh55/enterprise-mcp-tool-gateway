from app.mcp_gateway import server

from app.observability.health import (
    get_tool_health,
    get_tool_health_status,
)


def test_get_tool_health():

    health = get_tool_health()

    assert isinstance(health, list)
    assert len(health) >= 1

    for tool in health:
        assert "tool_name" in tool
        assert "version" in tool
        assert "enabled" in tool
        assert "status" in tool
        assert "risk_level" in tool


def test_health_check_tool():

    result = get_tool_health_status(
        "health_check"
    )

    assert result["tool_name"] == "health_check"
    assert result["enabled"] is True
    assert result["status"] == "HEALTHY"


def test_unknown_tool():

    try:
        get_tool_health_status(
            "unknown_tool"
        )
        assert False
    except KeyError:
        assert True