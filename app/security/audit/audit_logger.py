import json
import logging
from datetime import datetime, timezone
from typing import Any

from app.database.session import SessionLocal
from app.repositories.audit_repository import audit_repository

logger = logging.getLogger("mcp.audit")

AUDIT_EVENTS: list[dict[str, Any]] = []


def audit_event(
    *,
    user_id: str,
    role: str,
    tool_name: str,
    action: str,
    success: bool,
    request_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "role": role,
        "tool_name": tool_name,
        "action": action,
        "success": success,
        "request_id": request_id,
        "details": details or {},
    }

    # Keep existing in-memory audit behavior
    AUDIT_EVENTS.append(event)

    # Keep existing application logging
    logger.info(json.dumps(event))

    # Persist audit event to PostgreSQL
    db = SessionLocal()

    try:
        audit_repository.save(
            db,
            user_id=user_id,
            role=role,
            tool_name=tool_name,
            action=action,
            success=success,
            request_id=request_id,
            details=details or {},
        )
    except Exception as exc:
        # Database persistence failure must not break tool execution.
        logger.exception(
            "Failed to persist audit event to PostgreSQL: %s",
            exc,
        )
    finally:
        db.close()