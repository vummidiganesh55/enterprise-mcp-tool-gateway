from typing import Any, Callable


def run_failure_scenario(
    operation: Callable[[], Any],
) -> dict[str, Any]:

    try:
        result = operation()

        return {
            "success": True,
            "result": result,
            "error": None,
        }

    except Exception as exc:

        return {
            "success": False,
            "result": None,
            "error": str(exc),
            "error_type": type(exc).__name__,
        }


def always_fail() -> None:
    raise RuntimeError(
        "Simulated tool failure"
    )


def always_timeout() -> None:
    raise TimeoutError(
        "Simulated tool timeout"
    )


def fail_then_recover(
    attempts: int = 2,
) -> Callable[[], str]:

    state = {"count": 0}

    def operation() -> str:

        state["count"] += 1

        if state["count"] <= attempts:
            raise RuntimeError(
                "Simulated temporary failure"
            )

        return "recovered"

    return operation