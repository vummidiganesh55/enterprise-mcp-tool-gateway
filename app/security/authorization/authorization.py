from app.security.authorization.rbac import check_permission
from app.security.authorization.abac import check_attribute_access


def authorize(
    role: str,
    tool_name: str,
    customer_id: str | None = None,
) -> dict:

    if not check_permission(
        role,
        tool_name,
    ):
        return {
            "allowed": False,
            "reason": "ROLE_PERMISSION_DENIED",
        }

    if not check_attribute_access(
        role,
        tool_name,
        customer_id,
    ):
        return {
            "allowed": False,
            "reason": "ATTRIBUTE_ACCESS_DENIED",
        }

    return {
        "allowed": True,
        "reason": None,
    }