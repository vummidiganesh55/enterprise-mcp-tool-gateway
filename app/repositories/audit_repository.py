from typing import Any

from sqlalchemy.orm import Session

from app.database.models.audit import AuditEvent


class AuditRepository:
    def save(
        self,
        db: Session,
        *,
        user_id: str,
        role: str,
        tool_name: str,
        action: str,
        success: bool,
        request_id: str | None = None,
        details: dict[str, Any] | None = None,
        error_message: str | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            user_id=user_id,
            role=role,
            tool_name=tool_name,
            action=action,
            success=success,
            request_id=request_id,
            details=details or {},
            error_message=error_message,
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        return event


audit_repository = AuditRepository()