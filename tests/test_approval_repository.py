from app.database.session import SessionLocal
from app.repositories.approval_repository import approval_repository
from uuid import uuid4

def test_create_and_get_approval():
    db = SessionLocal()

    try:
        request_id = f"TEST-APPROVAL-{uuid4().hex}"

        approval = approval_repository.create(
            db,
            request_id=request_id,
            user_id="test-user",
            tool_name="customer_delete",
            reason="HIGH_RISK_TOOL_EXECUTION",
        )

        assert approval.request_id == request_id
        assert approval.user_id == "test-user"
        assert approval.tool_name == "customer_delete"
        assert approval.status == "PENDING"

        fetched = approval_repository.get(db, request_id)

        assert fetched is not None
        assert fetched.request_id == request_id
        assert fetched.status == "PENDING"

    finally:
        db.close()