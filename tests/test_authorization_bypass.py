from app.security.scanner.authorization_bypass import (
    detect_authorization_bypass,
)


def test_authorization_bypass_detected():

    result = detect_authorization_bypass(
        role="viewer",
        tool_name="customer_create",
        authorized=False,
    )

    assert result["detected"] is True
    assert result["risk"] == "HIGH"
    assert "UNAUTHORIZED_TOOL_ACCESS" in result["reasons"]


def test_role_mismatch_detected():

    result = detect_authorization_bypass(
        role="viewer",
        tool_name="customer_get",
        authorized=True,
        requested_role="admin",
    )

    assert result["detected"] is True
    assert result["risk"] == "HIGH"
    assert "ROLE_MISMATCH" in result["reasons"]


def test_authorized_request_is_safe():

    result = detect_authorization_bypass(
        role="support",
        tool_name="customer_get",
        authorized=True,
    )

    assert result["detected"] is False
    assert result["risk"] == "LOW"
    assert result["reasons"] == []