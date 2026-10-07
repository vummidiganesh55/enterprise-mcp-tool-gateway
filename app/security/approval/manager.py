from dataclasses import dataclass
from datetime import datetime, timezone

from app.database.session import SessionLocal
from app.repositories.approval_repository import approval_repository


@dataclass
class ApprovalRequest:
    request_id: str
    user_id: str
    tool_name: str
    reason: str
    status: str = "PENDING"
    created_at: datetime | None = None


class ApprovalManager:
    def __init__(self):
        # Keep in-memory cache for backward compatibility.
        self._requests: dict[str, ApprovalRequest] = {}

    def create_request(
        self,
        request_id: str,
        user_id: str,
        tool_name: str,
        reason: str,
    ) -> ApprovalRequest:

        # Return existing request from memory.
        if request_id in self._requests:
            return self._requests[request_id]

        db = SessionLocal()

        try:
            existing = approval_repository.get(db, request_id)

            if existing is not None:
                request = ApprovalRequest(
                    request_id=existing.request_id,
                    user_id=existing.user_id,
                    tool_name=existing.tool_name,
                    reason=existing.reason,
                    status=existing.status,
                    created_at=existing.created_at,
                )

                self._requests[request_id] = request
                return request

            approval = approval_repository.create(
                db,
                request_id=request_id,
                user_id=user_id,
                tool_name=tool_name,
                reason=reason,
            )

            request = ApprovalRequest(
                request_id=approval.request_id,
                user_id=approval.user_id,
                tool_name=approval.tool_name,
                reason=approval.reason,
                status=approval.status,
                created_at=approval.created_at,
            )

            self._requests[request_id] = request

            return request

        finally:
            db.close()

    def approve(self, request_id: str) -> ApprovalRequest:
        request = self._get_request(request_id)

        db = SessionLocal()

        try:
            approval_repository.update_status(
                db,
                request_id,
                "APPROVED",
            )
        finally:
            db.close()

        request.status = "APPROVED"
        return request

    def deny(self, request_id: str) -> ApprovalRequest:
        request = self._get_request(request_id)

        db = SessionLocal()

        try:
            approval_repository.update_status(
                db,
                request_id,
                "DENIED",
            )
        finally:
            db.close()

        request.status = "DENIED"
        return request

    def get(self, request_id: str) -> ApprovalRequest | None:
        if request_id in self._requests:
            return self._requests[request_id]

        db = SessionLocal()

        try:
            approval = approval_repository.get(db, request_id)

            if approval is None:
                return None

            request = ApprovalRequest(
                request_id=approval.request_id,
                user_id=approval.user_id,
                tool_name=approval.tool_name,
                reason=approval.reason,
                status=approval.status,
                created_at=approval.created_at,
            )

            self._requests[request_id] = request

            return request

        finally:
            db.close()

    def _get_request(self, request_id: str) -> ApprovalRequest:
        request = self.get(request_id)

        if request is None:
            raise KeyError(
                f"Approval request not found: {request_id}"
            )

        return request


approval_manager = ApprovalManager()