from app.security.rate_limit.limiter import RateLimiter


def test_allows_requests_within_limit():
    limiter = RateLimiter(
        max_requests=3,
        window_seconds=60,
    )

    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is True


def test_blocks_requests_after_limit():
    limiter = RateLimiter(
        max_requests=2,
        window_seconds=60,
    )

    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is False


def test_rate_limit_is_per_client():
    limiter = RateLimiter(
        max_requests=1,
        window_seconds=60,
    )

    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is False

    assert limiter.allow("user-2") is True


def test_remaining_requests():
    limiter = RateLimiter(
        max_requests=3,
        window_seconds=60,
    )

    assert limiter.remaining("user-1") == 3

    limiter.allow("user-1")

    assert limiter.remaining("user-1") == 2

    limiter.allow("user-1")

    assert limiter.remaining("user-1") == 1


def test_expired_requests_are_removed(monkeypatch):
    limiter = RateLimiter(
        max_requests=2,
        window_seconds=60,
    )

    current_time = [1000.0]

    monkeypatch.setattr(
        "app.security.rate_limit.limiter.time.time",
        lambda: current_time[0],
    )

    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is False

    current_time[0] = 1061.0

    assert limiter.allow("user-1") is True