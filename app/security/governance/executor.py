from typing import Any, Callable
import time

from app.observability.health import record_tool_call
from app.observability.metrics import metrics_collector
from app.idempotency.manager import idempotency_manager
from app.security.audit.audit_logger import audit_event
from app.security.approval.manager import approval_manager
from app.security.authorization.rbac import check_permission
from app.security.rate_limit.limiter import RateLimiter
from app.reliability.executor import ReliabilityExecutor
from app.reliability.errors import ReliabilityError
from app.validation.gateway_validator import gateway_validator
from app.security.scanner.scanner import security_scanner


class GovernanceExecutor:
    def __init__(
        self,
        *,
        reliability_executor: ReliabilityExecutor | None = None,
    ) -> None:
        self.reliability_executor = (
            reliability_executor or ReliabilityExecutor()
        )

        self.rate_limiter = RateLimiter(
            max_requests=10,
            window_seconds=60,
        )

    def execute(
        self,
        *,
        user_id: str,
        role: str,
        tool_name: str,
        function: Callable[..., Any],
        risk_level: str,
        request_id: str,
        idempotency_key: str,
        args: tuple | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        args = args or ()
        kwargs = kwargs or {}

        # ==========================================================
        # 1. RBAC AUTHORIZATION
        # ==========================================================

        authorized = check_permission(
            role,
            tool_name,
        )

        if not authorized:
            audit_event(
                user_id=user_id,
                role=role,
                tool_name=tool_name,
                action="AUTHORIZATION_DENIED",
                success=False,
                request_id=request_id,
                details={
                    "reason": "ROLE_NOT_AUTHORIZED",
                },
            )

            return {
                "success": False,
                "error": "AUTHORIZATION_DENIED",
            }

        # ==========================================================
        # 2. SECURITY SCANNER
        # ==========================================================

        security_result = security_scanner.scan(
            {
                "query": kwargs.get("query", ""),
                "role": role,
                "tool_name": tool_name,
                "authorized": authorized,
                "data": kwargs,
            }
        )

        if not security_result["safe"]:
            audit_event(
                user_id=user_id,
                role=role,
                tool_name=tool_name,
                action="SECURITY_THREAT_BLOCKED",
                success=False,
                request_id=request_id,
                details={
                    "detected_threats": security_result[
                        "detected_threats"
                    ],
                    "security_result": security_result,
                },
            )

            return {
                "success": False,
                "error": "SECURITY_THREAT_DETECTED",
                "detected_threats": security_result[
                    "detected_threats"
                ],
            }

        # ==========================================================
        # 3. REQUEST VALIDATION
        # ==========================================================

        validation_result = gateway_validator.validate_request(
            tool_name=tool_name,
            data=kwargs,
        )

        if not validation_result["valid"]:
            audit_event(
                user_id=user_id,
                role=role,
                tool_name=tool_name,
                action="REQUEST_VALIDATION_FAILED",
                success=False,
                request_id=request_id,
                details={
                    "error": validation_result["error"],
                },
            )

            return {
                "success": False,
                "error": "REQUEST_VALIDATION_FAILED",
                "details": validation_result["error"],
            }

        # ==========================================================
        # 4. RATE LIMITING
        # ==========================================================

        if not self.rate_limiter.allow(user_id):
            audit_event(
                user_id=user_id,
                role=role,
                tool_name=tool_name,
                action="RATE_LIMIT_DENIED",
                success=False,
                request_id=request_id,
                details={
                    "reason": "RATE_LIMIT_EXCEEDED",
                },
            )

            return {
                "success": False,
                "error": "RATE_LIMIT_EXCEEDED",
            }

        # ==========================================================
        # 5. HIGH-RISK APPROVAL
        # ==========================================================

        if risk_level == "HIGH":
            approval = approval_manager.create_request(
                request_id=request_id,
                user_id=user_id,
                tool_name=tool_name,
                reason="HIGH_RISK_TOOL_EXECUTION",
            )

            if approval.status != "APPROVED":
                audit_event(
                    user_id=user_id,
                    role=role,
                    tool_name=tool_name,
                    action="APPROVAL_REQUIRED",
                    success=False,
                    request_id=request_id,
                    details={
                        "approval_id": approval.request_id,
                        "status": approval.status,
                    },
                )

                return {
                    "success": False,
                    "error": "APPROVAL_REQUIRED",
                    "approval_id": approval.request_id,
                    "status": approval.status,
                }

        # ==========================================================
        # 6. IDEMPOTENCY
        # ==========================================================

        def execute_idempotent_tool():
            return idempotency_manager.execute(
                idempotency_key,
                function,
                *args,
                **kwargs,
            )

        # ==========================================================
        # 7. RELIABILITY + TOOL EXECUTION
        # ==========================================================

        start_time = time.perf_counter()

        try:
            result = self.reliability_executor.execute(
                execute_idempotent_tool
            )

            # ======================================================
            # 8. RESPONSE VALIDATION
            # ======================================================

            response_validation = (
                gateway_validator.validate_response(
                    tool_name=tool_name,
                    data=result,
                )
            )

            if not response_validation["valid"]:
                latency_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                record_tool_call(
                    tool_name=tool_name,
                    success=False,
                    latency_ms=latency_ms,
                )

                metrics_collector.record_failure(
                    tool_name=tool_name,
                    latency_seconds=latency_ms / 1000,
                )

                audit_event(
                    user_id=user_id,
                    role=role,
                    tool_name=tool_name,
                    action="RESPONSE_VALIDATION_FAILED",
                    success=False,
                    request_id=request_id,
                    details={
                        "error": response_validation["error"],
                    },
                )

                return {
                    "success": False,
                    "error": "RESPONSE_VALIDATION_FAILED",
                    "details": response_validation["error"],
                }

            result = response_validation["data"]

            # ======================================================
            # 9. SUCCESS OBSERVABILITY
            # ======================================================

            latency_ms = (
                time.perf_counter() - start_time
            ) * 1000

            record_tool_call(
                tool_name=tool_name,
                success=True,
                latency_ms=latency_ms,
            )

            metrics_collector.record_success(
                tool_name=tool_name,
                latency_seconds=latency_ms / 1000,
            )

            audit_event(
                user_id=user_id,
                role=role,
                tool_name=tool_name,
                action="TOOL_EXECUTION",
                success=True,
                request_id=request_id,
                details={
                    "latency_ms": round(
                        latency_ms,
                        2,
                    ),
                },
            )

            return {
                "success": True,
                "data": result,
            }

        # ==========================================================
        # 10. RELIABILITY ERROR
        # ==========================================================

        except ReliabilityError as exc:
            latency_ms = (
                time.perf_counter() - start_time
            ) * 1000

            record_tool_call(
                tool_name=tool_name,
                success=False,
                latency_ms=latency_ms,
            )

            metrics_collector.record_failure(
                tool_name=tool_name,
                latency_seconds=latency_ms / 1000,
            )

            audit_event(
                user_id=user_id,
                role=role,
                tool_name=tool_name,
                action="TOOL_EXECUTION_FAILED",
                success=False,
                request_id=request_id,
                details={
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                    "latency_ms": round(
                        latency_ms,
                        2,
                    ),
                },
            )

            return {
                "success": False,
                "error": str(exc),
            }

        # ==========================================================
        # 11. UNEXPECTED ERROR
        # ==========================================================

        except Exception as exc:
            latency_ms = (
                time.perf_counter() - start_time
            ) * 1000

            record_tool_call(
                tool_name=tool_name,
                success=False,
                latency_ms=latency_ms,
            )

            metrics_collector.record_failure(
                tool_name=tool_name,
                latency_seconds=latency_ms / 1000,
            )

            audit_event(
                user_id=user_id,
                role=role,
                tool_name=tool_name,
                action="TOOL_EXECUTION_FAILED",
                success=False,
                request_id=request_id,
                details={
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                    "latency_ms": round(
                        latency_ms,
                        2,
                    ),
                },
            )

            return {
                "success": False,
                "error": str(exc),
            }


governance_executor = GovernanceExecutor()