from app.security.scanner.data_exposure import (
    detect_data_exposure,
)


def test_sensitive_data_exposure_detected():

    data = {
        "customer_id": "C001",
        "name": "John Doe",
        "api_key": "secret-key",
        "password": "secret-password",
    }

    result = detect_data_exposure(data)

    assert result["detected"] is True
    assert result["risk"] == "HIGH"
    assert "api_key" in result["exposed_fields"]
    assert "password" in result["exposed_fields"]


def test_safe_data():

    data = {
        "customer_id": "C001",
        "name": "John Doe",
        "status": "active",
    }

    result = detect_data_exposure(data)

    assert result["detected"] is False
    assert result["risk"] == "LOW"
    assert result["exposed_fields"] == []