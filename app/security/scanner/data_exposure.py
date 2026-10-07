from typing import Any


SENSITIVE_FIELDS = {
    "password",
    "passwd",
    "secret",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "authorization",
    "credit_card",
    "card_number",
    "cvv",
    "ssn",
}


def detect_data_exposure(
    data: dict[str, Any],
) -> dict[str, Any]:

    exposed_fields = []

    for key in data:
        normalized_key = key.lower()

        if normalized_key in SENSITIVE_FIELDS:
            exposed_fields.append(key)

    detected = len(exposed_fields) > 0

    return {
        "detected": detected,
        "risk": "HIGH" if detected else "LOW",
        "exposed_fields": exposed_fields,
    }