from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError as FutureTimeoutError,
)
from typing import Any, Callable

from app.reliability.errors import ToolTimeoutError


def execute_with_timeout(
    function: Callable[..., Any],
    *,
    timeout_seconds: float = 5.0,
    **kwargs: Any,
) -> Any:
    """
    Execute a function with a maximum execution time.
    """

    if timeout_seconds <= 0:
        raise ValueError(
            "timeout_seconds must be greater than 0"
        )

    executor = ThreadPoolExecutor(
        max_workers=1
    )

    future = executor.submit(
        function,
        **kwargs,
    )

    try:

        result = future.result(
            timeout=timeout_seconds
        )

        executor.shutdown(wait=True)

        return result

    except FutureTimeoutError as exc:

        future.cancel()

        executor.shutdown(
            wait=False,
            cancel_futures=True,
        )

        raise ToolTimeoutError(
            f"Tool execution timed out after "
            f"{timeout_seconds} seconds"
        ) from exc

    except Exception:

        executor.shutdown(
            wait=True
        )

        raise