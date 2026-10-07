from typing import Any

from app.security.audit.audit_logger import AUDIT_EVENTS


def search_audit_events(
    tool_name: str | None = None,
    user_id: str | None = None,
    success: bool | None = None,
) -> dict[str, Any]:

    results = []

    for event in AUDIT_EVENTS:

        if tool_name is not None:
            if event["tool_name"] != tool_name:
                continue

        if user_id is not None:
            if event["user_id"] != user_id:
                continue

        if success is not None:
            if event["success"] != success:
                continue

        results.append(event)

    return {
        "success": True,
        "count": len(results),
        "results": results,
    }