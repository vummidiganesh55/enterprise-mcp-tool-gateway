from app.security.scanner.malicious_tool_definition import (
    detect_malicious_tool_definition,
)


def test_malicious_tool_definition_detected():

    tool = {
        "name": "dangerous_tool",
        "description": (
            "Execute arbitrary code and "
            "disable authentication."
        ),
        "version": "1.0.0",
    }

    result = detect_malicious_tool_definition(tool)

    assert result["detected"] is True
    assert result["risk"] == "HIGH"
    assert len(result["matches"]) >= 2


def test_safe_tool_definition():

    tool = {
        "name": "customer_get",
        "description": (
            "Retrieve a customer by customer ID."
        ),
        "version": "1.0.0",
    }

    result = detect_malicious_tool_definition(tool)

    assert result["detected"] is False
    assert result["risk"] == "LOW"
    assert result["matches"] == []