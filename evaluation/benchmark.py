from typing import Any

from evaluation.evaluator import security_evaluator
from evaluation.metrics import calculate_evaluation_metrics
from evaluation.history import evaluation_history


class BenchmarkRunner:

    def run(self) -> dict[str, Any]:
        # Run all evaluation cases
        results = security_evaluator.evaluate_all()

        # Calculate metrics
        metrics = calculate_evaluation_metrics(
            results
        )

        # Save benchmark run
        run = evaluation_history.save_run(
            results=results,
            metrics=metrics,
        )

        return run


benchmark_runner = BenchmarkRunner()