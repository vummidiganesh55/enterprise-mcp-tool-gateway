import time

import pytest

from app.reliability.timeout import (
    ToolTimeoutError,
    execute_with_timeout,
)


def test_timeout_success():

    def fast_function():
        return "SUCCESS"

    result = execute_with_timeout(
        fast_function,
        timeout_seconds=1.0,
    )

    assert result == "SUCCESS"


def test_timeout_failure():

    def slow_function():
        time.sleep(0.2)
        return "TOO_SLOW"

    with pytest.raises(
        ToolTimeoutError,
        match="Tool execution timed out",
    ):
        execute_with_timeout(
            slow_function,
            timeout_seconds=0.05,
        )


def test_timeout_custom_arguments():

    def add_numbers(a, b):
        return a + b

    result = execute_with_timeout(
        add_numbers,
        timeout_seconds=1.0,
        a=10,
        b=20,
    )

    assert result == 30


def test_timeout_invalid_value():

    def function():
        return "SUCCESS"

    with pytest.raises(
        ValueError,
        match="timeout_seconds must be greater than 0",
    ):
        execute_with_timeout(
            function,
            timeout_seconds=0,
        )


def test_function_exception_propagates():

    def failing_function():
        raise RuntimeError(
            "TOOL_FAILURE"
        )

    with pytest.raises(
        RuntimeError,
        match="TOOL_FAILURE",
    ):
        execute_with_timeout(
            failing_function,
            timeout_seconds=1.0,
        )