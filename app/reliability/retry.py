from typing import Any, Callable


def retry(
    function: Callable[..., Any],
    *,
    max_attempts: int = 3,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    **kwargs: Any,
) -> Any:
    """
    Execute a function with retry support.

    Args:
        function: Function to execute.
        max_attempts: Maximum number of execution attempts.
        exceptions: Exception types that should trigger a retry.
        **kwargs: Arguments passed to the function.

    Returns:
        The function result.

    Raises:
        Exception:
            The final exception after all attempts fail.
        ValueError:
            If max_attempts is less than 1.
    """

    if max_attempts < 1:
        raise ValueError(
            "max_attempts must be at least 1"
        )

    last_exception: Exception | None = None

    for attempt in range(1, max_attempts + 1):

        try:
            return function(**kwargs)

        except exceptions as exc:

            last_exception = exc

            if attempt == max_attempts:
                raise

    # Defensive fallback.
    if last_exception is not None:
        raise last_exception

    raise RuntimeError(
        "Retry execution failed unexpectedly"
    )