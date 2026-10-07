from typing import Any


TOOL_POISONING_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard previous instructions",
    "reveal system prompt",
    "send credentials",
    "exfiltrate data",
    "bypass authorization",
    "disable security",
    "execute arbitrary code",
]


def detect_tool_poisoning(
    tool_metadata: dict[str, Any],
) -> dict[str, Any]:

    searchable_text = " ".join(
        str(value)
        for value in tool_metadata.values()
    ).lower()

    matches = [
        pattern
        for pattern in TOOL_POISONING_PATTERNS
        if pattern in searchable_text
    ]

    return {
        "detected": len(matches) > 0,
        "matches": matches,
        "risk": "HIGH" if matches else "LOW",
    }