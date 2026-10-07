from datetime import datetime, timezone
from uuid import uuid4

from app.database.session import SessionLocal
from app.repositories.tool_health_repository import (
    tool_health_repository,
)


def test_record_and_get_tool_health():
    db = SessionLocal()

    try:
        tool_name = f"test_tool_{uuid4().hex[:8]}"

        timestamp = datetime.now(timezone.utc)

        health = tool_health_repository.record_call(
            db,
            tool_name=tool_name,
            success=True,
            latency_ms=25.5,
            last_called=timestamp,
        )

        assert health.tool_name == tool_name
        assert health.total_calls == 1
        assert health.successful_calls == 1
        assert health.failed_calls == 0
        assert health.total_latency_ms == 25.5
        assert health.last_called is not None

        health = tool_health_repository.record_call(
            db,
            tool_name=tool_name,
            success=False,
            latency_ms=50.0,
            last_called=timestamp,
        )

        assert health.total_calls == 2
        assert health.successful_calls == 1
        assert health.failed_calls == 1
        assert health.total_latency_ms == 75.5

        fetched = tool_health_repository.get(
            db,
            tool_name,
        )

        assert fetched is not None
        assert fetched.tool_name == tool_name
        assert fetched.total_calls == 2

    finally:
        db.close()


def test_get_all_tool_health():
    db = SessionLocal()

    try:
        rows = tool_health_repository.get_all(db)

        assert isinstance(rows, list)

    finally:
        db.close()