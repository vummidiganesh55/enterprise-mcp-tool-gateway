from app.observability.metrics import (
    MetricsCollector,
    measure_tool_execution,
)


def test_success_metrics():

    metrics = MetricsCollector()

    metrics.record_success(
        "customer_get",
        0.10,
    )

    metrics.record_success(
        "customer_get",
        0.20,
    )

    result = metrics.get_metrics(
        "customer_get"
    )

    assert result["total_requests"] == 2
    assert result["successful_requests"] == 2
    assert result["failed_requests"] == 0
    assert result["success_rate"] == 1.0
    assert result["average_latency_seconds"] == 0.15


def test_failure_metrics():

    metrics = MetricsCollector()

    metrics.record_success(
        "customer_get",
        0.10,
    )

    metrics.record_failure(
        "customer_get",
        0.30,
    )

    result = metrics.get_metrics(
        "customer_get"
    )

    assert result["total_requests"] == 2
    assert result["successful_requests"] == 1
    assert result["failed_requests"] == 1
    assert result["success_rate"] == 0.5


def test_measure_tool_execution():

    def tool():
        return "success"

    result = measure_tool_execution(
        "health_check",
        tool,
    )

    assert result == "success"