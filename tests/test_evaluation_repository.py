from uuid import uuid4

from app.database.session import SessionLocal
from app.repositories.evaluation_repository import evaluation_repository


def test_save_and_get_evaluation_run():
    db = SessionLocal()

    try:
        run_id = f"TEST-RUN-{uuid4().hex[:8].upper()}"

        run = evaluation_repository.save(
            db,
            run_id=run_id,
            timestamp="2026-10-07T10:00:00+00:00",
            total_cases=100,
            passed=84,
            failed=16,
            accuracy=0.84,
            results=[
                {
                    "case_id": "CASE-001",
                    "passed": True,
                }
            ],
            metrics={
                "detection_accuracy": 0.84,
                "risk_accuracy": 0.84,
            },
        )

        assert run.run_id == run_id
        assert run.total_cases == 100
        assert run.passed == 84
        assert run.failed == 16
        assert run.accuracy == 0.84

        fetched = evaluation_repository.get(
            db,
            run_id,
        )

        assert fetched is not None
        assert fetched.run_id == run_id
        assert fetched.total_cases == 100
        assert fetched.passed == 84
        assert fetched.failed == 16
        assert fetched.metrics["detection_accuracy"] == 0.84

    finally:
        db.close()


def test_get_all_evaluation_runs():
    db = SessionLocal()

    try:
        runs = evaluation_repository.get_all(db)

        assert isinstance(runs, list)

    finally:
        db.close()