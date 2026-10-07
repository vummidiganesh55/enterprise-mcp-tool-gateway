import time
from concurrent.futures import ThreadPoolExecutor

from app.tools.customer.get import get_customer


def execute_request(customer_id: str) -> dict:
    start = time.perf_counter()

    try:
        result = get_customer(customer_id)

        latency = time.perf_counter() - start

        return {
            "success": result["success"],
            "latency": latency,
        }

    except Exception as exc:
        latency = time.perf_counter() - start

        return {
            "success": False,
            "latency": latency,
            "error": str(exc),
        }


def run_load_test(
    total_requests: int = 50,
    workers: int = 10,
) -> dict:

    customer_ids = [
        "C001",
        "C002",
    ]

    start_time = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:

        futures = [
            executor.submit(
                execute_request,
                customer_ids[i % len(customer_ids)],
            )
            for i in range(total_requests)
        ]

        results = [
            future.result()
            for future in futures
        ]

    total_time = time.perf_counter() - start_time

    successful = sum(
        1
        for result in results
        if result["success"]
    )

    failed = total_requests - successful

    latencies = [
        result["latency"]
        for result in results
    ]

    average_latency = (
        sum(latencies) / len(latencies)
        if latencies
        else 0.0
    )

    throughput = (
        total_requests / total_time
        if total_time > 0
        else 0.0
    )

    return {
        "total_requests": total_requests,
        "successful_requests": successful,
        "failed_requests": failed,
        "total_time": total_time,
        "average_latency": average_latency,
        "throughput": throughput,
    }
def test_load_test():

    result = run_load_test(
        total_requests=50,
        workers=10,
    )

    assert result["total_requests"] == 50
    assert result["successful_requests"] == 50
    assert result["failed_requests"] == 0

    assert result["total_time"] >= 0
    assert result["average_latency"] >= 0
    assert result["throughput"] > 0