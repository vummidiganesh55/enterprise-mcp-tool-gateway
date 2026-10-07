from dataclasses import dataclass


@dataclass
class PolicyContext:
    user_id: str
    role: str
    tool_name: str
    risk_level: str
    customer_id: str | None = None


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str


class PolicyEngine:

    def evaluate(
        self,
        context: PolicyContext,
    ) -> PolicyDecision:

        # Admin can access all registered tools
        # unless the tool is HIGH risk.
        if context.role == "admin":

            if context.risk_level == "HIGH":
                return PolicyDecision(
                    allowed=False,
                    reason="HIGH_RISK_REQUIRES_APPROVAL",
                )

            return PolicyDecision(
                allowed=True,
                reason="ADMIN_POLICY_ALLOWED",
            )

        # Support users can read customer data.
        if (
            context.role == "support"
            and context.tool_name == "customer_get"
            and context.risk_level == "LOW"
        ):
            return PolicyDecision(
                allowed=True,
                reason="SUPPORT_READ_POLICY_ALLOWED",
            )

        # Viewer can only use health check.
        if (
            context.role == "viewer"
            and context.tool_name == "health_check"
            and context.risk_level == "LOW"
        ):
            return PolicyDecision(
                allowed=True,
                reason="VIEWER_HEALTH_POLICY_ALLOWED",
            )

        return PolicyDecision(
            allowed=False,
            reason="POLICY_DENIED",
        )


policy_engine = PolicyEngine()