import pytest

from app.reliability.circuit_breaker import (
    CircuitBreaker,
)
from app.reliability.errors import (
    CircuitOpenError,
)


def test_circuit_starts_closed():

    breaker = CircuitBreaker(
        failure_threshold=3,
    )

    assert breaker.state.state == "CLOSED"
    assert breaker.allow_request() is True


def test_circuit_opens_after_threshold():

    breaker = CircuitBreaker(
        failure_threshold=3,
    )

    breaker.record_failure()
    breaker.record_failure()

    assert breaker.state.state == "CLOSED"

    breaker.record_failure()

    assert breaker.state.state == "OPEN"
    assert breaker.allow_request() is False


def test_open_circuit_rejects_execution():

    breaker = CircuitBreaker(
        failure_threshold=1,
    )

    breaker.record_failure()

    def function():
        return "SUCCESS"

    with pytest.raises(
        CircuitOpenError
    ):
        breaker.execute(function)


def test_success_resets_circuit():

    breaker = CircuitBreaker(
        failure_threshold=2,
    )

    breaker.record_failure()

    breaker.record_success()

    assert breaker.state.state == "CLOSED"
    assert breaker.state.failure_count == 0


def test_half_open_recovery():

    breaker = CircuitBreaker(
        failure_threshold=1,
        recovery_timeout_seconds=0.01,
    )

    breaker.record_failure()

    assert breaker.state.state == "OPEN"

    import time

    time.sleep(0.02)

    assert breaker.allow_request() is True
    assert breaker.state.state == "HALF_OPEN"