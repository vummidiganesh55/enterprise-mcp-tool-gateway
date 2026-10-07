def check_attribute_access(
    role: str,
    tool_name: str,
    customer_id: str | None = None,
) -> bool:

    # Admin has unrestricted access.
    if role == "admin":
        return True

    # Support can access customer data.
    if role == "support" and tool_name == "customer_get":
        return customer_id is not None

    # Viewer can only use health check.
    if role == "viewer" and tool_name == "health_check":
        return True

    return False