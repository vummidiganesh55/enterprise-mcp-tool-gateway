from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class BenchmarkRun:
    run_id: str
    timestamp: str
    total_cases: int
    passed: int
    failed: int
    accuracy: float

    # Original evaluation results for this benchmark run.
    results: list[dict[str, Any]] = field(default_factory=list)

    # Calculated benchmark metrics.
    metrics: dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Any:
        """
        Allow BenchmarkRun to behave like a dictionary.

        Examples:
            run["run_id"]
            run["accuracy"]
            run["detection_accuracy"]
            run["results"]
        """

        if hasattr(self, key):
            return getattr(self, key)

        if key in self.metrics:
            return self.metrics[key]

        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        """
        Support dictionary-style membership checks.

        Examples:
            "run_id" in run
            "detection_accuracy" in run
            "results" in run
        """

        return (
            hasattr(self, key)
            or key in self.metrics
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the complete benchmark run into a dictionary.
        """

        result = {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "total_cases": self.total_cases,
            "passed": self.passed,
            "failed": self.failed,
            "accuracy": self.accuracy,
            "results": self.results,
        }

        # Expose calculated metrics at the top level.
        result.update(self.metrics)

        # Also preserve the complete metrics object.
        result["metrics"] = self.metrics

        return result


class EvaluationHistory:

    def __init__(self) -> None:
        self._runs: list[BenchmarkRun] = []

    def save_run(
        self,
        *,
        results: list[dict[str, Any]] | None = None,
        metrics: dict[str, Any] | None = None,
        total_cases: int | None = None,
        passed: int | None = None,
        failed: int | None = None,
        accuracy: float | None = None,
    ) -> BenchmarkRun:

        results = results or []
        metrics = metrics or {}

        if total_cases is None:
            total_cases = len(results)

        if passed is None:
            passed = sum(
                1
                for result in results
                if result.get("passed", False)
            )

        if failed is None:
            failed = total_cases - passed

        if accuracy is None:
            accuracy = (
                passed / total_cases
                if total_cases > 0
                else 0.0
            )

        run = BenchmarkRun(
            run_id=f"RUN-{uuid4().hex[:8].upper()}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            total_cases=total_cases,
            passed=passed,
            failed=failed,
            accuracy=accuracy,
            results=results,
            metrics=metrics,
        )

        # Preserve existing in-memory behavior.
        self._runs.append(run)

        # Persist benchmark run to PostgreSQL.
        from app.database.session import SessionLocal
        from app.repositories.evaluation_repository import (
            evaluation_repository,
        )

        db = SessionLocal()

        try:
            evaluation_repository.save(
                db,
                run_id=run.run_id,
                timestamp=run.timestamp,
                total_cases=run.total_cases,
                passed=run.passed,
                failed=run.failed,
                accuracy=run.accuracy,
                results=run.results,
                metrics=run.metrics,
            )
        finally:
            db.close()

        return run

    def get_run(
        self,
        run_id: str,
    ) -> BenchmarkRun | None:

        for run in self._runs:
            if run.run_id == run_id:
                return run

        # Fall back to PostgreSQL.
        from app.database.session import SessionLocal
        from app.repositories.evaluation_repository import (
            evaluation_repository,
        )

        db = SessionLocal()

        try:
            stored_run = evaluation_repository.get(
                db,
                run_id,
            )

            if stored_run is None:
                return None

            run = BenchmarkRun(
                run_id=stored_run.run_id,
                timestamp=stored_run.timestamp.isoformat(),
                total_cases=stored_run.total_cases,
                passed=stored_run.passed,
                failed=stored_run.failed,
                accuracy=stored_run.accuracy,
                results=stored_run.results or [],
                metrics=stored_run.metrics or {},
            )

            self._runs.append(run)

            return run

        finally:
            db.close()

    def get_runs(self) -> list[BenchmarkRun]:
        """
        Return all benchmark runs.
        """

        if self._runs:
            return list(self._runs)

        from app.database.session import SessionLocal
        from app.repositories.evaluation_repository import (
            evaluation_repository,
        )

        db = SessionLocal()

        try:
            stored_runs = evaluation_repository.get_all(db)

            self._runs = [
                BenchmarkRun(
                    run_id=stored_run.run_id,
                    timestamp=stored_run.timestamp.isoformat(),
                    total_cases=stored_run.total_cases,
                    passed=stored_run.passed,
                    failed=stored_run.failed,
                    accuracy=stored_run.accuracy,
                    results=stored_run.results or [],
                    metrics=stored_run.metrics or {},
                )
                for stored_run in stored_runs
            ]

            return list(self._runs)

        finally:
            db.close()

    def list_runs(self) -> list[BenchmarkRun]:
        """
        Alias for get_runs().
        """

        return self.get_runs()

    def latest_run(self) -> BenchmarkRun | None:

        runs = self.get_runs()

        if not runs:
            return None

        return runs[-1]

    def compare_runs(
        self,
        first_run_id: str,
        second_run_id: str,
    ) -> dict[str, Any]:

        first = self.get_run(first_run_id)
        second = self.get_run(second_run_id)

        if first is None:
            raise ValueError(
                f"Run not found: {first_run_id}"
            )

        if second is None:
            raise ValueError(
                f"Run not found: {second_run_id}"
            )

        accuracy_delta = round(
            second.accuracy - first.accuracy,
            4,
        )

        return {
            "first_run": first.run_id,
            "second_run": second.run_id,
            "accuracy_delta": accuracy_delta,
            "regression": accuracy_delta < 0,
            "first_accuracy": first.accuracy,
            "second_accuracy": second.accuracy,
        }

    def detect_regression(
        self,
        current_run_id: str,
        previous_run_id: str | None = None,
    ) -> dict[str, Any]:

        current = self.get_run(current_run_id)

        if current is None:
            raise ValueError(
                f"Run not found: {current_run_id}"
            )

        if previous_run_id is None:
            runs = self.get_runs()

            current_index = next(
                (
                    index
                    for index, run in enumerate(runs)
                    if run.run_id == current_run_id
                ),
                None,
            )

            if current_index is None:
                raise ValueError(
                    f"Run not found: {current_run_id}"
                )

            if current_index == 0:
                return {
                    "regression": False,
                    "reason": "NO_PREVIOUS_RUN",
                    "current_run": current_run_id,
                }

            previous = runs[current_index - 1]

        else:
            previous = self.get_run(previous_run_id)

            if previous is None:
                raise ValueError(
                    f"Run not found: {previous_run_id}"
                )

        accuracy_delta = round(
            current.accuracy - previous.accuracy,
            4,
        )

        return {
            "regression": accuracy_delta < 0,
            "current_run": current.run_id,
            "previous_run": previous.run_id,
            "current_accuracy": current.accuracy,
            "previous_accuracy": previous.accuracy,
            "accuracy_delta": accuracy_delta,
        }
evaluation_history = EvaluationHistory()