from app.reliability.errors import (
    ErrorCode,
    ReliabilityError,
    TimeoutError,
    CircuitOpenError,
)


def test_reliability_error_structure():

    error = ReliabilityError(
        code=ErrorCode.INTERNAL_ERROR,
        message="Something went wrong",
        details={
            "service": "customer-service",
        },
    )

    result = error.to_dict()

    assert result["success"] is False
    assert result["error"]["code"] == "INTERNAL_ERROR"
    assert result["error"]["message"] == "Something went wrong"
    assert result["error"]["details"]["service"] == "customer-service"


def test_timeout_error():

    error = TimeoutError(
        "Customer service timed out"
    )

    result = error.to_dict()

    assert result["error"]["code"] == "TIMEOUT"
    assert result["error"]["message"] == "Customer service timed out"


def test_circuit_open_error():

    error = CircuitOpenError()

    result = error.to_dict()

    assert result["error"]["code"] == "CIRCUIT_OPEN"
    assert result["success"] is False