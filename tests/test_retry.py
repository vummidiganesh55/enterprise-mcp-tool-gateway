import pytest

from app.reliability.retry import retry


def test_retry_success_first_attempt():

    calls = {"count": 0}

    def successful_function():
        calls["count"] += 1
        return "SUCCESS"

    result = retry(
        successful_function,
        max_attempts=3,
    )

    assert result == "SUCCESS"
    assert calls["count"] == 1


def test_retry_after_failures():

    calls = {"count": 0}

    def eventually_successful():
        calls["count"] += 1

        if calls["count"] < 3:
            raise RuntimeError("TEMPORARY_FAILURE")

        return "SUCCESS"

    result = retry(
        eventually_successful,
        max_attempts=3,
    )

    assert result == "SUCCESS"
    assert calls["count"] == 3


def test_retry_exhausted():

    calls = {"count": 0}

    def always_fails():
        calls["count"] += 1
        raise RuntimeError("PERMANENT_FAILURE")

    with pytest.raises(RuntimeError, match="PERMANENT_FAILURE"):
        retry(
            always_fails,
            max_attempts=3,
        )

    assert calls["count"] == 3


def test_retry_custom_exception():

    calls = {"count": 0}

    def function():
        calls["count"] += 1

        if calls["count"] == 1:
            raise ValueError("RETRY_ME")

        return "SUCCESS"

    result = retry(
        function,
        max_attempts=3,
        exceptions=(ValueError,),
    )

    assert result == "SUCCESS"
    assert calls["count"] == 2


def test_retry_invalid_attempts():

    def function():
        return "SUCCESS"

    with pytest.raises(
        ValueError,
        match="max_attempts must be at least 1",
    ):
        retry(
            function,
            max_attempts=0,
        )