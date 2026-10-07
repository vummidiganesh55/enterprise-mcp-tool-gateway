from app.observability.tracing import (
    setup_tracing,
    trace_tool_execution,
)


def test_trace_tool_execution_success():

    setup_tracing()

    def health_check():
        return {
            "status": "healthy"
        }

    result = trace_tool_execution(
        "health_check",
        health_check,
    )

    assert result == {
        "status": "healthy"
    }


def test_trace_tool_execution_failure():

    setup_tracing()

    def failing_tool():
        raise RuntimeError(
            "Tool execution failed"
        )

    try:
        trace_tool_execution(
            "failing_tool",
            failing_tool,
        )
    except RuntimeError as exc:
        assert str(exc) == "Tool execution failed"
    else:
        raise AssertionError(
            "Expected RuntimeError"
        )