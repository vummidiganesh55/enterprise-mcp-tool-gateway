import pytest

from app.reliability.circuit_breaker import (
    CircuitBreaker,
)
from app.reliability.errors import (
    CircuitOpenError,
    ReliabilityExecutionError,
)
from app.reliability.executor import (
    ReliabilityExecutor,
)


def test_reliability_executor_success():

    executor = ReliabilityExecutor(
        max_attempts=3,
        timeout_seconds=1.0,
    )

    def primary():
        return "SUCCESS"

    result = executor.execute(
        primary
    )

    assert result == "SUCCESS"


def test_reliability_executor_retry_then_success():

    calls = {
        "count": 0
    }

    executor = ReliabilityExecutor(
        max_attempts=3,
        timeout_seconds=1.0,
    )

    def primary():

        calls["count"] += 1

        if calls["count"] < 3:
            raise RuntimeError("TEMPORARY")

        return "SUCCESS"

    result = executor.execute(
        primary
    )

    assert result == "SUCCESS"
    assert calls["count"] == 3


def test_reliability_executor_fallback():

    executor = ReliabilityExecutor(
        max_attempts=2,
        timeout_seconds=1.0,
    )

    def primary():
        raise RuntimeError("PRIMARY_FAILED")

    def fallback():
        return "FALLBACK_SUCCESS"

    result = executor.execute(
        primary,
        fallback=fallback,
    )

    assert result == "FALLBACK_SUCCESS"


def test_reliability_executor_both_fail():

    executor = ReliabilityExecutor(
        max_attempts=2,
        timeout_seconds=1.0,
    )

    def primary():
        raise RuntimeError("PRIMARY_FAILED")

    def fallback():
        raise RuntimeError("FALLBACK_FAILED")

    with pytest.raises(
        ReliabilityExecutionError
    ):
        executor.execute(
            primary,
            fallback=fallback,
        )


def test_reliability_executor_open_circuit():

    breaker = CircuitBreaker(
        failure_threshold=1,
    )

    breaker.record_failure()

    executor = ReliabilityExecutor(
        max_attempts=1,
        timeout_seconds=1.0,
        circuit_breaker=breaker,
    )

    def primary():
        return "SHOULD_NOT_RUN"

    with pytest.raises(
        CircuitOpenError
    ):
        executor.execute(
            primary
        )