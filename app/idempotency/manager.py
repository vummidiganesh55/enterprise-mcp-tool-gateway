from typing import Any

from app.idempotency.store import IdempotencyStore


class IdempotencyManager:
    def __init__(self):
        self.store = IdempotencyStore()

    def execute(
        self,
        key: str,
        function,
        *args,
        **kwargs,
    ) -> Any:

        if self.store.exists(key):
            return self.store.get(key)

        result = function(
            *args,
            **kwargs,
        )

        self.store.save(
            key,
            result,
        )

        return result


idempotency_manager = IdempotencyManager()