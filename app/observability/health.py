from datetime import datetime, timezone
from typing import Any

from app.mcp_gateway.registry import tool_registry
from app.database.session import SessionLocal
from app.repositories.tool_health_repository import (
    tool_health_repository,
)


# Runtime health statistics for each tool.
# This remains isolated per application process.
_TOOL_STATS: dict[str, dict[str, Any]] = {}


def _get_stats(
    tool_name: str,
) -> dict[str, Any]:
    """Get runtime statistics for a tool."""

    if tool_name not in _TOOL_STATS:
        _TOOL_STATS[tool_name] = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "total_latency_ms": 0.0,
            "last_called": None,
        }

    return _TOOL_STATS[tool_name]


def record_tool_call(
    tool_name: str,
    success: bool,
    latency_ms: float,
) -> None:
    """Record one tool execution."""

    stats = _get_stats(tool_name)

    # Update runtime statistics.
    stats["total_calls"] += 1

    if success:
        stats["successful_calls"] += 1
    else:
        stats["failed_calls"] += 1

    stats["total_latency_ms"] += latency_ms

    now = datetime.now(timezone.utc)

    stats["last_called"] = now.isoformat()

    # Persist tool-health statistics to PostgreSQL.
    db = SessionLocal()

    try:
        tool_health_repository.record_call(
            db,
            tool_name=tool_name,
            success=success,
            latency_ms=latency_ms,
            last_called=now,
        )

    finally:
        db.close()


def _build_health(
    tool_name: str,
    version: str,
    enabled: bool,
    risk_level: str,
) -> dict[str, Any]:

    stats = _get_stats(tool_name)

    total_calls = stats["total_calls"]

    success_rate = (
        (
            stats["successful_calls"]
            / total_calls
        )
        * 100
        if total_calls > 0
        else 0.0
    )

    average_latency_ms = (
        stats["total_latency_ms"]
        / total_calls
        if total_calls > 0
        else 0.0
    )

    return {
        "tool_name": tool_name,
        "version": version,
        "enabled": enabled,
        "status": (
            "HEALTHY"
            if enabled
            else "DISABLED"
        ),
        "risk_level": risk_level,
        "total_calls": total_calls,
        "successful_calls": stats["successful_calls"],
        "failed_calls": stats["failed_calls"],
        "success_rate": round(
            success_rate,
            2,
        ),
        "average_latency_ms": round(
            average_latency_ms,
            2,
        ),
        "last_called": stats["last_called"],
    }


def get_tool_health() -> list[dict[str, Any]]:
    """Return health information for all registered tools."""

    health = []

    for tool in tool_registry.list_tools():
        health.append(
            _build_health(
                tool_name=tool.name,
                version=tool.version,
                enabled=tool.enabled,
                risk_level=tool.risk_level,
            )
        )

    return health


def get_tool_health_status(
    tool_name: str,
) -> dict[str, Any]:
    """Return health information for one tool."""

    tool = tool_registry.get(tool_name)

    return _build_health(
        tool_name=tool.name,
        version=tool.version,
        enabled=tool.enabled,
        risk_level=tool.risk_level,
    )