from app.mcp_gateway.registry import tool_registry


def discover_tools():
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


def discover_tool(name: str):
    tool = tool_registry.get(name)

    return {
        "name": tool.name,
        "version": tool.version,
        "description": tool.description,
        "risk_level": tool.risk_level,
        "enabled": tool.enabled,
    }