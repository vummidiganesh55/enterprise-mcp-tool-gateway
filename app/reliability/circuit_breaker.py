from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.reliability.errors import CircuitOpenError


@dataclass
class CircuitState:
    failure_count: int = 0
    state: str = "CLOSED"
    opened_at: datetime | None = None


class CircuitBreaker:

    def __init__(
        self,
        *,
        failure_threshold: int = 3,
        recovery_timeout_seconds: float = 30.0,
    ):
        if failure_threshold < 1:
            raise ValueError(
                "failure_threshold must be at least 1"
            )

        if recovery_timeout_seconds <= 0:
            raise ValueError(
                "recovery_timeout_seconds must be greater than 0"
            )

        self.failure_threshold = (
            failure_threshold
        )

        self.recovery_timeout_seconds = (
            recovery_timeout_seconds
        )

        self.state = CircuitState()

    def _should_attempt_recovery(self) -> bool:

        if self.state.opened_at is None:
            return False

        elapsed = (
            datetime.now(timezone.utc)
            - self.state.opened_at
        )

        return (
            elapsed.total_seconds()
            >= self.recovery_timeout_seconds
        )

    def allow_request(self) -> bool:

        if self.state.state == "CLOSED":
            return True

        if self.state.state == "OPEN":

            if self._should_attempt_recovery():

                self.state.state = "HALF_OPEN"

                return True

            return False

        # HALF_OPEN
        return True

    def record_success(self) -> None:

        self.state.failure_count = 0
        self.state.state = "CLOSED"
        self.state.opened_at = None

    def record_failure(self) -> None:

        self.state.failure_count += 1

        if (
            self.state.failure_count
            >= self.failure_threshold
        ):
            self.state.state = "OPEN"

            self.state.opened_at = (
                datetime.now(timezone.utc)
            )

    def execute(
        self,
        function,
        **kwargs,
    ):

        if not self.allow_request():

            raise CircuitOpenError(
                "Circuit breaker is OPEN"
            )

        try:

            result = function(**kwargs)

            self.record_success()

            return result

        except Exception:

            self.record_failure()

            raise