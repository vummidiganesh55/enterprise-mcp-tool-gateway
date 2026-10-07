import pytest

from app.reliability.errors import FallbackError
from app.reliability.fallback import (
    execute_with_fallback,
)


def test_primary_success():

    calls = {
        "primary": 0,
        "fallback": 0,
    }

    def primary():
        calls["primary"] += 1
        return "PRIMARY_SUCCESS"

    def fallback():
        calls["fallback"] += 1
        return "FALLBACK_SUCCESS"

    result = execute_with_fallback(
        primary,
        fallback,
    )

    assert result == "PRIMARY_SUCCESS"
    assert calls["primary"] == 1
    assert calls["fallback"] == 0


def test_fallback_after_primary_failure():

    calls = {
        "primary": 0,
        "fallback": 0,
    }

    def primary():
        calls["primary"] += 1
        raise RuntimeError("PRIMARY_FAILED")

    def fallback():
        calls["fallback"] += 1
        return "FALLBACK_SUCCESS"

    result = execute_with_fallback(
        primary,
        fallback,
    )

    assert result == "FALLBACK_SUCCESS"
    assert calls["primary"] == 1
    assert calls["fallback"] == 1


def test_both_primary_and_fallback_fail():

    def primary():
        raise RuntimeError("PRIMARY_FAILED")

    def fallback():
        raise RuntimeError("FALLBACK_FAILED")

    with pytest.raises(
        FallbackError
    ):
        execute_with_fallback(
            primary,
            fallback,
        )


def test_fallback_receives_arguments():

    def primary(value):
        raise RuntimeError("FAIL")

    def fallback(value):
        return value * 2

    result = execute_with_fallback(
        primary,
        fallback,
        kwargs={
            "value": 10,
        },
    )

    assert result == 20