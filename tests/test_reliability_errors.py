from app.reliability.errors import (
    CircuitOpenError,
    FallbackError,
    ReliabilityError,
    ReliabilityExecutionError,
    RetryExhaustedError,
    ToolTimeoutError,
)


def test_reliability_error_hierarchy():

    assert issubclass(
        ToolTimeoutError,
        ReliabilityError,
    )

    assert issubclass(
        RetryExhaustedError,
        ReliabilityError,
    )

    assert issubclass(
        FallbackError,
        ReliabilityError,
    )

    assert issubclass(
        CircuitOpenError,
        ReliabilityError,
    )

    assert issubclass(
        ReliabilityExecutionError,
        ReliabilityError,
    )


def test_error_messages():

    assert str(
        ToolTimeoutError("timeout")
    ) == "timeout"

    assert str(
        CircuitOpenError("open")
    ) == "open"