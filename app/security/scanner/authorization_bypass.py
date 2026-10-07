from typing import Any


PROTECTED_ROLES = {
    "admin",
    "support",
    "viewer",
}


def detect_authorization_bypass(
    *,
    role: str,
    tool_name: str,
    authorized: bool,
    requested_role: str | None = None,
) -> dict[str, Any]:

    reasons = []

    if role not in PROTECTED_ROLES:
        reasons.append("UNKNOWN_ROLE")

    if requested_role is not None:
        if requested_role != role:
            reasons.append("ROLE_MISMATCH")

    if not authorized:
        reasons.append("UNAUTHORIZED_TOOL_ACCESS")

    detected = len(reasons) > 0

    return {
        "detected": detected,
        "risk": "HIGH" if detected else "LOW",
        "reasons": reasons,
        "role": role,
        "tool_name": tool_name,
    }