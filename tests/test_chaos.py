from chaos.scenarios import (
    always_fail,
    always_timeout,
    fail_then_recover,
    run_failure_scenario,
)

from app.reliability.executor import ReliabilityExecutor


def test_always_fail_scenario():
    result = run_failure_scenario(always_fail)

    assert result["success"] is False
    assert result["error"] == "Simulated tool failure"
    assert result["error_type"] == "RuntimeError"


def test_timeout_scenario():
    result = run_failure_scenario(always_timeout)

    assert result["success"] is False
    assert result["error"] == "Simulated tool timeout"
    assert result["error_type"] == "TimeoutError"


def test_fail_then_recover_scenario():
    operation = fail_then_recover(attempts=2)

    result = run_failure_scenario(operation)
    assert result["success"] is False

    result = run_failure_scenario(operation)
    assert result["success"] is False

    result = run_failure_scenario(operation)
    assert result["success"] is True
    assert result["result"] == "recovered"


def test_reliability_executor_recovers_from_transient_failure():
    operation = fail_then_recover(attempts=2)

    executor = ReliabilityExecutor()

    result = executor.execute(operation)

    assert result == "recovered"