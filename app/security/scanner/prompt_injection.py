from typing import Any


PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard previous instructions",
    "system prompt",
    "reveal your instructions",
    "bypass security",
    "override security",
]


def detect_prompt_injection(
    text: str,
) -> dict[str, Any]:

    normalized_text = text.lower()

    matches = [
        pattern
        for pattern in PROMPT_INJECTION_PATTERNS
        if pattern in normalized_text
    ]

    return {
        "detected": len(matches) > 0,
        "matches": matches,
        "risk": "HIGH" if matches else "LOW",
    }