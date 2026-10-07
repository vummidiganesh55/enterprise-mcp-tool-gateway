from typing import Any, Callable

from app.reliability.circuit_breaker import (
    CircuitBreaker,
)
from app.reliability.errors import (
    CircuitOpenError,
    ReliabilityExecutionError,
)
from app.reliability.retry import retry
from app.reliability.timeout import (
    execute_with_timeout,
)


class ReliabilityExecutor:

    def __init__(
        self,
        *,
        max_attempts: int = 3,
        timeout_seconds: float = 5.0,
        circuit_breaker: CircuitBreaker | None = None,
    ):

        self.max_attempts = max_attempts
        self.timeout_seconds = timeout_seconds

        self.circuit_breaker = (
            circuit_breaker
            or CircuitBreaker()
        )

    def execute(
        self,
        primary: Callable[..., Any],
        *,
        fallback: Callable[..., Any] | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> Any:

        kwargs = kwargs or {}

        def execute_primary():

            return execute_with_timeout(
                primary,
                timeout_seconds=self.timeout_seconds,
                **kwargs,
            )

        try:

            if not self.circuit_breaker.allow_request():

                if fallback is not None:
                    return fallback(**kwargs)

                raise CircuitOpenError(
                    "Circuit breaker is OPEN"
                )

            try:

                result = retry(
                    execute_primary,
                    max_attempts=self.max_attempts,
                )

                self.circuit_breaker.record_success()

                return result

            except Exception:

                self.circuit_breaker.record_failure()

                if fallback is not None:

                    try:
                        return fallback(**kwargs)

                    except Exception as fallback_error:

                        raise ReliabilityExecutionError(
                            "Primary and fallback "
                            "execution failed"
                        ) from fallback_error

                raise

        except CircuitOpenError:

            if fallback is not None:
                return fallback(**kwargs)

            raise