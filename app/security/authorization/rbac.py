from app.security.authorization.permissions import (
    ROLE_PERMISSIONS,
)
ROLE_PERMISSIONS = {
    "admin": {
        "health_check",
        "customer_get",
        "customer_update",
        "customer_delete",
        "ticket_get",
        "ticket_create",
        "order_get",
        "order_status",
        "knowledge_search",
        "knowledge_retrieve",
        "audit_search",
    },

    "support": {
        "health_check",
        "customer_get",
        "customer_update",
        "ticket_get",
        "ticket_create",
        "order_get",
        "order_status",
        "knowledge_search",
        "knowledge_retrieve",
    },

    "viewer": {
        "health_check",
        "customer_get",
        "ticket_get",
        "order_get",
        "order_status",
        "knowledge_search",
        "knowledge_retrieve",
    },
}

def check_permission(
    role: str,
    tool_name: str,
) -> bool:

    permissions = ROLE_PERMISSIONS.get(role)

    if permissions is None:
        return False

    return tool_name in permissions