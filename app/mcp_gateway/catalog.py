from app.mcp_gateway.registry import tool_registry


def get_tool_catalog() -> list[dict]:
    tools = tool_registry.list_tools()

    return [
        {
            "name": tool.name,
            "version": tool.version,
            "description": tool.description,
            "risk_level": tool.risk_level,
            "enabled": tool.enabled,
        }
        for tool in tools
    ]


def get_tool_details(tool_name: str) -> dict:
    tool = tool_registry.get(tool_name)

    return {
        "name": tool.name,
        "version": tool.version,
        "description": tool.description,
        "risk_level": tool.risk_level,
        "enabled": tool.enabled,
    }