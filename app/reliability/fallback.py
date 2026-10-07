from typing import Any, Callable

from app.reliability.errors import FallbackError


def execute_with_fallback(
    primary: Callable[..., Any],
    fallback: Callable[..., Any],
    *,
    kwargs: dict[str, Any] | None = None,
) -> Any:
    """
    Execute the primary function.

    If the primary function fails, execute
    the fallback function.
    """

    kwargs = kwargs or {}

    try:

        return primary(**kwargs)

    except Exception as primary_error:

        try:

            return fallback(**kwargs)

        except Exception as fallback_error:

            raise FallbackError(
                "Both primary and fallback "
                "execution failed"
            ) from fallback_error