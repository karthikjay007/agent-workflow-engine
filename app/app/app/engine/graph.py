from typing import Callable, Dict, Any, Optional

class Node:
    def __init__(self, name: str, func: Callable[[Dict[str, Any]], Any]):
        self.name = name
        self.func = func

class Graph:
    def __init__(
        self,
        nodes: Dict[str, Node],
        edges: Dict[str, Optional[str]],
        start: str,
        branches: Dict[str, Callable[[Dict], str]] = None,
        loops: Dict[str, Callable[[Dict], bool]] = None
    ):
        self.nodes = nodes
        self.edges = edges
        self.start = start
        self.branches = branches or {}
        self.loops = loops or {}
