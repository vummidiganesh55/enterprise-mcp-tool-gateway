import time
from collections import defaultdict
from typing import Any


class MetricsCollector:
    def __init__(self):
        self._total_requests = defaultdict(int)
        self._successful_requests = defaultdict(int)
        self._failed_requests = defaultdict(int)
        self._latencies = defaultdict(list)

    def record_success(
        self,
        tool_name: str,
        latency_seconds: float,
    ) -> None:
        self._total_requests[tool_name] += 1
        self._successful_requests[tool_name] += 1
        self._latencies[tool_name].append(
            latency_seconds
        )

    def record_failure(
        self,
        tool_name: str,
        latency_seconds: float,
    ) -> None:
        self._total_requests[tool_name] += 1
        self._failed_requests[tool_name] += 1
        self._latencies[tool_name].append(
            latency_seconds
        )

    def get_metrics(
        self,
        tool_name: str,
    ) -> dict[str, Any]:

        total = self._total_requests[tool_name]
        success = self._successful_requests[tool_name]
        failure = self._failed_requests[tool_name]
        latencies = self._latencies[tool_name]

        success_rate = (
            success / total
            if total > 0
            else 0.0
        )

        average_latency = (
            round(sum(latencies) / len(latencies), 6)
            if latencies
            else 0.0
        )

        return {
            "tool_name": tool_name,
            "total_requests": total,
            "successful_requests": success,
            "failed_requests": failure,
            "success_rate": success_rate,
            "average_latency_seconds": average_latency,
        }


metrics_collector = MetricsCollector()


def measure_tool_execution(
    tool_name: str,
    function,
    *args,
    **kwargs,
):
    start = time.perf_counter()

    try:
        result = function(
            *args,
            **kwargs,
        )

        latency = time.perf_counter() - start

        metrics_collector.record_success(
            tool_name,
            latency,
        )

        return result

    except Exception:
        latency = time.perf_counter() - start

        metrics_collector.record_failure(
            tool_name,
            latency,
        )

        raise