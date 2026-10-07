from typing import Any

from app.database.session import SessionLocal
from app.repositories.idempotency_repository import (
    idempotency_repository,
)


class IdempotencyStore:
    def __init__(self):
        self._store: dict[str, Any] = {}

    def exists(self, key: str) -> bool:
        return key in self._store

    def get(self, key: str) -> Any:
        return self._store.get(key)

    def save(self, key: str, result: Any) -> None:
        self._store[key] = result

        db = SessionLocal()
        try:
            existing = idempotency_repository.get(db, key)

            if existing is None:
                idempotency_repository.save(
                    db,
                    key=key,
                    result=result,
                )
        finally:
            db.close()

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

        db = SessionLocal()
        try:
            idempotency_repository.delete(db, key)
        finally:
            db.close()