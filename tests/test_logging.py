import logging

from app.observability.logging import (
    setup_logging,
    log_tool_execution,
)


def test_logging_setup():
    setup_logging()

    logger = logging.getLogger(
        "enterprise-mcp-gateway"
    )

    assert logger.level == logging.INFO


def test_successful_tool_logging(caplog):

    setup_logging()

    with caplog.at_level(
        logging.INFO,
        logger="enterprise-mcp-gateway",
    ):
        log_tool_execution(
            tool_name="customer_get",
            success=True,
            request_id="req-001",
            details={
                "customer_id": "C001"
            },
        )

    assert "customer_get" in caplog.text
    assert "req-001" in caplog.text


def test_failed_tool_logging(caplog):

    setup_logging()

    with caplog.at_level(
        logging.ERROR,
        logger="enterprise-mcp-gateway",
    ):
        log_tool_execution(
            tool_name="customer_get",
            success=False,
            request_id="req-002",
            details={
                "error": "CUSTOMER_NOT_FOUND"
            },
        )

    assert "customer_get" in caplog.text
    assert "req-002" in caplog.text
    assert "CUSTOMER_NOT_FOUND" in caplog.text