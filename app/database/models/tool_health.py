from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.models_base import Base


class ToolHealth(Base):
    __tablename__ = "tool_health"

    tool_name: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    total_calls: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    successful_calls: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    failed_calls: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    total_latency_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    last_called: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )