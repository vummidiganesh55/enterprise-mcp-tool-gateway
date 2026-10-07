from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    """
    Standard error codes used by the reliability layer.
    """

    INTERNAL_ERROR = "INTERNAL_ERROR"
    TIMEOUT = "TIMEOUT"
    RETRY_EXHAUSTED = "RETRY_EXHAUSTED"
    FALLBACK_FAILED = "FALLBACK_FAILED"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class ReliabilityError(Exception):
    """
    Base exception for reliability failures.
    """

    def __init__(
        self,
        code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        message: str = "Reliability execution failed",
        details: dict[str, Any] | None = None,
    ) -> None:

        self.code = code
        self.message = message
        self.details = details or {}

        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the reliability error into
        the standard API error response.
        """

        return {
            "success": False,
            "error": {
                "code": self.code.value,
                "message": self.message,
                "details": self.details,
            },
        }


class TimeoutError(ReliabilityError):
    """
    Raised when a tool exceeds its execution timeout.
    """

    def __init__(
        self,
        message: str = "Tool execution timed out",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            code=ErrorCode.TIMEOUT,
            message=message,
            details=details,
        )


class ToolTimeoutError(TimeoutError):
    """
    Backward-compatible alias for tool timeout handling.
    """

    pass


class RetryExhaustedError(ReliabilityError):
    """
    Raised when all retry attempts are exhausted.
    """

    def __init__(
        self,
        message: str = "All retry attempts exhausted",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            code=ErrorCode.RETRY_EXHAUSTED,
            message=message,
            details=details,
        )


class FallbackError(ReliabilityError):
    """
    Raised when both primary and fallback execution fail.
    """

    def __init__(
        self,
        message: str = "Both primary and fallback execution failed",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            code=ErrorCode.FALLBACK_FAILED,
            message=message,
            details=details,
        )


class CircuitOpenError(ReliabilityError):
    """
    Raised when the circuit breaker is open.
    """

    def __init__(
        self,
        message: str = "Circuit breaker is OPEN",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            code=ErrorCode.CIRCUIT_OPEN,
            message=message,
            details=details,
        )


class ReliabilityExecutionError(ReliabilityError):
    """
    Raised when the complete reliability pipeline fails.
    """

    def __init__(
        self,
        message: str = "Reliability execution failed",
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            code=ErrorCode.INTERNAL_ERROR,
            message=message,
            details=details,
        )