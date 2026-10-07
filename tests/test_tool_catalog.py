import pytest

import app.mcp_gateway.server
from app.mcp_gateway.catalog import (
    get_tool_catalog,
    get_tool_details,
)


def test_get_tool_catalog():
    catalog = get_tool_catalog()

    assert isinstance(catalog, list)
    assert len(catalog) >= 1

    tool_names = {
        tool["name"]
        for tool in catalog
    }

    assert "customer_get" in tool_names
    assert "customer_update" in tool_names
    assert "customer_delete" in tool_names


def test_tool_catalog_metadata():
    catalog = get_tool_catalog()

    customer_get = next(
        tool
        for tool in catalog
        if tool["name"] == "customer_get"
    )

    assert customer_get["version"] == "1.0.0"
    assert customer_get["risk_level"] == "LOW"
    assert customer_get["enabled"] is True


def test_get_tool_details():
    details = get_tool_details("customer_delete")

    assert details["name"] == "customer_delete"
    assert details["version"] == "1.0.0"
    assert details["risk_level"] == "HIGH"
    assert details["enabled"] is True


def test_unknown_tool_details():
    with pytest.raises(KeyError):
        get_tool_details("unknown_tool")