from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.tool_health import ToolHealth


class ToolHealthRepository:

    def record_call(
        self,
        db: Session,
        *,
        tool_name: str,
        success: bool,
        latency_ms: float,
        last_called: datetime | None = None,
    ) -> ToolHealth:

        health = db.get(ToolHealth, tool_name)

        if health is None:
            health = ToolHealth(
                tool_name=tool_name,
                total_calls=0,
                successful_calls=0,
                failed_calls=0,
                total_latency_ms=0.0,
            )
            db.add(health)

        health.total_calls += 1

        if success:
            health.successful_calls += 1
        else:
            health.failed_calls += 1

        health.total_latency_ms += latency_ms

        health.last_called = (
            last_called
            or datetime.now(timezone.utc)
        )

        db.commit()
        db.refresh(health)

        return health

    def get(
        self,
        db: Session,
        tool_name: str,
    ) -> ToolHealth | None:

        return db.get(ToolHealth, tool_name)

    def get_all(
        self,
        db: Session,
    ) -> list[ToolHealth]:

        return (
            db.query(ToolHealth)
            .order_by(ToolHealth.tool_name.asc())
            .all()
        )


tool_health_repository = ToolHealthRepository()