import logging
from typing import Any


LOGGER_NAME = "enterprise-mcp-gateway"


def setup_logging() -> None:
    logger = logging.getLogger(LOGGER_NAME)

    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)


logger = logging.getLogger(LOGGER_NAME)


def log_tool_execution(
    tool_name: str,
    success: bool,
    request_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:

    event = {
        "event": "tool_execution",
        "tool_name": tool_name,
        "success": success,
        "request_id": request_id,
        "details": details or {},
    }

    if success:
        logger.info(event)
    else:
        logger.error(event)