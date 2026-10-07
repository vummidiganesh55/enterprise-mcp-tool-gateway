import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(
        self,
        max_requests: int = 10,
        window_seconds: int = 60,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self._requests = defaultdict(deque)

    def allow(self, client_id: str) -> bool:
        now = time.time()

        requests = self._requests[client_id]

        # Remove expired requests.
        while requests:
            if now - requests[0] >= self.window_seconds:
                requests.popleft()
            else:
                break

        if len(requests) >= self.max_requests:
            return False

        requests.append(now)

        return True

    def remaining(self, client_id: str) -> int:
        now = time.time()

        requests = self._requests[client_id]

        while requests:
            if now - requests[0] >= self.window_seconds:
                requests.popleft()
            else:
                break

        return max(
            0,
            self.max_requests - len(requests),
        )