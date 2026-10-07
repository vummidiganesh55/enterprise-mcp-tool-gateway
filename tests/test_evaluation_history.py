from evaluation.history import EvaluationHistory


def test_save_run():
    history = EvaluationHistory()

    run = history.save_run(
        total_cases=100,
        passed=84,
        failed=16,
        accuracy=0.84,
        metrics={
            "security_accuracy": 0.84,
        },
    )

    assert run.run_id.startswith("RUN-")
    assert run.total_cases == 100
    assert run.passed == 84
    assert run.failed == 16
    assert run.accuracy == 0.84


def test_get_run():
    history = EvaluationHistory()

    run = history.save_run(
        total_cases=100,
        passed=84,
        failed=16,
        accuracy=0.84,
    )

    result = history.get_run(run.run_id)

    assert result is not None
    assert result.run_id == run.run_id


def test_list_runs():
    history = EvaluationHistory()

    history.save_run(
        total_cases=100,
        passed=84,
        failed=16,
        accuracy=0.84,
    )

    history.save_run(
        total_cases=100,
        passed=90,
        failed=10,
        accuracy=0.90,
    )

    runs = history.list_runs()

    assert len(runs) == 2


def test_latest_run():
    history = EvaluationHistory()

    first = history.save_run(
        total_cases=100,
        passed=84,
        failed=16,
        accuracy=0.84,
    )

    second = history.save_run(
        total_cases=100,
        passed=90,
        failed=10,
        accuracy=0.90,
    )

    latest = history.latest_run()

    assert latest is not None
    assert latest.run_id == second.run_id
    assert latest.run_id != first.run_id


def test_compare_runs():
    history = EvaluationHistory()

    first = history.save_run(
        total_cases=100,
        passed=84,
        failed=16,
        accuracy=0.84,
    )

    second = history.save_run(
        total_cases=100,
        passed=90,
        failed=10,
        accuracy=0.90,
    )

    comparison = history.compare_runs(
        first.run_id,
        second.run_id,
    )

    assert comparison["accuracy_delta"] == 0.06
    assert comparison["regression"] is False


def test_regression_detection():
    history = EvaluationHistory()

    first = history.save_run(
        total_cases=100,
        passed=90,
        failed=10,
        accuracy=0.90,
    )

    second = history.save_run(
        total_cases=100,
        passed=80,
        failed=20,
        accuracy=0.80,
    )

    comparison = history.compare_runs(
        first.run_id,
        second.run_id,
    )

    assert comparison["accuracy_delta"] == -0.10
    assert comparison["regression"] is True