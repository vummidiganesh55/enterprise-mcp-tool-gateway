from typing import Any


DANGEROUS_TOOL_PATTERNS = [
    "execute arbitrary code",
    "run shell command",
    "execute shell",
    "disable authentication",
    "disable authorization",
    "bypass security",
    "delete all data",
    "drop database",
    "exfiltrate",
    "send credentials",
]


def detect_malicious_tool_definition(
    tool_metadata: dict[str, Any],
) -> dict[str, Any]:

    searchable_text = " ".join(
        str(value)
        for value in tool_metadata.values()
    ).lower()

    matches = [
        pattern
        for pattern in DANGEROUS_TOOL_PATTERNS
        if pattern in searchable_text
    ]

    detected = len(matches) > 0

    return {
        "detected": detected,
        "risk": "HIGH" if detected else "LOW",
        "matches": matches,
        "tool_name": tool_metadata.get("name"),
    }