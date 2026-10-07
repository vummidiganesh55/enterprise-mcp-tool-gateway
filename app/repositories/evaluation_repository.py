from typing import Any

from sqlalchemy.orm import Session

from app.database.models.evaluation import EvaluationRun


class EvaluationRepository:

    def save(
        self,
        db: Session,
        *,
        run_id: str,
        timestamp: str,
        total_cases: int,
        passed: int,
        failed: int,
        accuracy: float,
        results: list[dict[str, Any]],
        metrics: dict[str, Any],
    ) -> EvaluationRun:

        run = EvaluationRun(
            run_id=run_id,
            timestamp=timestamp,
            total_cases=total_cases,
            passed=passed,
            failed=failed,
            accuracy=accuracy,
            results=results,
            metrics=metrics,
        )

        db.add(run)
        db.commit()
        db.refresh(run)

        return run

    def get(
        self,
        db: Session,
        run_id: str,
    ) -> EvaluationRun | None:

        return db.get(EvaluationRun, run_id)

    def get_all(
        self,
        db: Session,
    ) -> list[EvaluationRun]:

        return (
            db.query(EvaluationRun)
            .order_by(EvaluationRun.timestamp.asc())
            .all()
        )


evaluation_repository = EvaluationRepository()