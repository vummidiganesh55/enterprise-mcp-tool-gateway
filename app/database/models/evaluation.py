from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.models_base import Base


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    run_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    total_cases: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    passed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    failed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    accuracy: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    results: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    metrics: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )