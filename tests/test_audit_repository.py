from app.database.session import SessionLocal
from app.repositories.audit_repository import audit_repository


def test_save_audit_event():
    db = SessionLocal()

    try:
        event = audit_repository.save(
            db,
            user_id="test-user",
            role="admin",
            tool_name="customer_get",
            action="TEST",
            success=True,
            request_id="TEST-001",
            details={"source": "pytest"},
        )

        assert event.id is not None
        assert event.user_id == "test-user"
        assert event.tool_name == "customer_get"
        assert event.success is True

    finally:
        db.close()