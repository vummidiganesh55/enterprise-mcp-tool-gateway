from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


TOOL_RISK_LEVELS = {
    "health_check": "LOW",

    "customer_get": "LOW",
    "customer_update": "MEDIUM",
    "customer_delete": "HIGH",

    "knowledge_search": "LOW",
    "knowledge_retrieve": "LOW",

    "ticket_get": "LOW",
    "ticket_create": "MEDIUM",

    "order_get": "LOW",
    "order_status": "LOW",

    "audit_search": "MEDIUM",
}


def classify_tool(tool_name: str) -> RiskLevel:
    return TOOL_RISK_LEVELS.get(
        tool_name,
        RiskLevel.HIGH,
    )


def is_allowed(
    tool_name: str,
    risk_level: RiskLevel | None = None,
) -> bool:

    level = risk_level or classify_tool(tool_name)

    # LOW and MEDIUM tools are allowed
    # after authentication and authorization.
    if level in {
        RiskLevel.LOW,
        RiskLevel.MEDIUM,
    }:
        return True

    # HIGH-risk tools require additional
    # security controls.
    return False

def get_risk_level(tool_name: str) -> str:
    return TOOL_RISK_LEVELS.get(tool_name, "HIGH")