from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.approval import ApprovalRequest


class ApprovalRepository:
    def create(
        self,
        db: Session,
        *,
        request_id: str,
        user_id: str,
        tool_name: str,
        reason: str,
    ) -> ApprovalRequest:
        approval = ApprovalRequest(
            request_id=request_id,
            user_id=user_id,
            tool_name=tool_name,
            reason=reason,
            status="PENDING",
        )

        db.add(approval)
        db.commit()
        db.refresh(approval)

        return approval

    def get(
        self,
        db: Session,
        request_id: str,
    ) -> ApprovalRequest | None:
        return db.get(ApprovalRequest, request_id)

    def update_status(
        self,
        db: Session,
        request_id: str,
        status: str,
    ) -> ApprovalRequest | None:
        approval = db.get(ApprovalRequest, request_id)

        if approval is None:
            return None

        approval.status = status
        approval.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(approval)

        return approval


approval_repository = ApprovalRepository()