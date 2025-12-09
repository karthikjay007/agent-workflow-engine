from typing import Callable, Dict, Any

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]):
        self.tools[name] = fn

    def get(self, name: str):
        return self.tools.get(name)

registry = ToolRegistry()
