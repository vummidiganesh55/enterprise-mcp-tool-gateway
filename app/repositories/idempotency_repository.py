from typing import Any

from sqlalchemy.orm import Session

from app.database.models.idempotency import IdempotencyRecord


class IdempotencyRepository:
    def save(
        self,
        db: Session,
        *,
        key: str,
        result: Any,
    ) -> IdempotencyRecord:
        record = IdempotencyRecord(
            key=key,
            result=result,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    def get(
        self,
        db: Session,
        key: str,
    ) -> IdempotencyRecord | None:
        return db.get(IdempotencyRecord, key)

    def delete(
        self,
        db: Session,
        key: str,
    ) -> None:
        record = db.get(IdempotencyRecord, key)

        if record is not None:
            db.delete(record)
            db.commit()


idempotency_repository = IdempotencyRepository()