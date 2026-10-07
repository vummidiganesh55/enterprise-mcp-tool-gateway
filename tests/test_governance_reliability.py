from app.reliability.executor import ReliabilityExecutor
from app.security.governance.executor import GovernanceExecutor


def test_governance_retries_failed_tool():

    calls = {
        "count": 0,
    }

    def flaky_tool():

        calls["count"] += 1

        if calls["count"] < 3:
            raise RuntimeError(
                "TEMPORARY_FAILURE"
            )

        return {
            "message": "success",
        }

    reliability = ReliabilityExecutor(
        max_attempts=3,
        timeout_seconds=1.0,
    )

    executor = GovernanceExecutor(
        reliability_executor=reliability,
    )

    result = executor.execute(
        user_id="U-REL-001",
        role="support",
        tool_name="customer_get",
        risk_level="LOW",
        request_id="REQ-REL-001",
        idempotency_key="IDEMP-REL-001",
        function=flaky_tool,
    )

    assert result["success"] is True
    assert result["data"]["message"] == "success"
    assert calls["count"] == 3


def test_governance_timeout():

    def slow_tool():

        import time

        time.sleep(0.2)

        return {
            "message": "too slow",
        }

    reliability = ReliabilityExecutor(
        max_attempts=1,
        timeout_seconds=0.05,
    )

    executor = GovernanceExecutor(
        reliability_executor=reliability,
    )

    result = executor.execute(
        user_id="U-REL-002",
        role="support",
        tool_name="customer_get",
        risk_level="LOW",
        request_id="REQ-REL-002",
        idempotency_key="IDEMP-REL-002",
        function=slow_tool,
    )

    assert result["success"] is False


def test_governance_fallback():

    def primary():

        raise RuntimeError(
            "PRIMARY_FAILED"
        )

    def fallback():

        return {
            "message": "fallback_success",
        }

    reliability = ReliabilityExecutor(
        max_attempts=1,
        timeout_seconds=1.0,
    )

    executor = GovernanceExecutor(
        reliability_executor=reliability,
    )

    result = executor.reliability_executor.execute(
        primary,
        fallback=fallback,
    )

    assert result["message"] == "fallback_success"