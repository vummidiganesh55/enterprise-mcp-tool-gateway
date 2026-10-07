from app.mcp_gateway.registry import ToolMetadata, tool_registry


class ToolVersionManager:
    def get_current_version(self, name: str) -> str:
        tool = tool_registry.get(name)
        return tool.version

    def resolve(
        self,
        name: str,
        version: str | None = None,
    ) -> ToolMetadata:
        tool = tool_registry.get(name)

        if version is None:
            return tool

        if tool.version != version:
            raise ValueError(
                f"Tool '{name}' version '{version}' is not available. "
                f"Available version: '{tool.version}'"
            )

        return tool

    def is_compatible(
        self,
        name: str,
        version: str,
    ) -> bool:
        try:
            self.resolve(name, version)
            return True
        except (KeyError, ValueError):
            return False


tool_version_manager = ToolVersionManager()


# Backward-compatible functions
def get_tool_version(name: str) -> str:
    return tool_version_manager.get_current_version(name)


def resolve_tool(
    name: str,
    version: str | None = None,
) -> ToolMetadata:
    return tool_version_manager.resolve(name, version)