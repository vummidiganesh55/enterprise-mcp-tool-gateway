from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolMetadata:
    name: str
    version: str
    description: str
    function: Callable[..., Any]
    risk_level: str = "LOW"
    enabled: bool = True


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolMetadata] = {}

    def register(self, tool: ToolMetadata) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolMetadata:
        tool = self._tools.get(name)

        if tool is None:
            raise KeyError(
                f"Tool '{name}' is not registered"
            )

        if not tool.enabled:
            raise RuntimeError(
                f"Tool '{name}' is disabled"
            )

        return tool

    def list_tools(self) -> list[ToolMetadata]:
        return list(self._tools.values())

    def exists(self, name: str) -> bool:
        return name in self._tools

    def unregister(self, name: str) -> None:
        if name not in self._tools:
            raise KeyError(
                f"Tool '{name}' is not registered"
            )

        del self._tools[name]


# Global Tool Registry
tool_registry = ToolRegistry()