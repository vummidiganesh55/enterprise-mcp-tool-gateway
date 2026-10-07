from evaluation.benchmark import BenchmarkRunner
from evaluation.history import evaluation_history


def test_benchmark_run():

    runner = BenchmarkRunner()

    run = runner.run()

    assert "run_id" in run
    assert "timestamp" in run

    assert run["total_cases"] == 100

    assert "accuracy" in run
    assert "detection_accuracy" in run
    assert "risk_accuracy" in run

    assert "results" in run
    assert len(run["results"]) == 100


def test_multiple_benchmark_runs():

    runner = BenchmarkRunner()

    first = runner.run()
    second = runner.run()

    assert first["run_id"] != second["run_id"]

    runs = evaluation_history.get_runs()

    assert len(runs) >= 2