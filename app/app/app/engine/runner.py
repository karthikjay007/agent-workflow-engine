import asyncio
import uuid
from typing import Dict, Any, Tuple
from .graph import Graph, Node

class RunRecord:
    def __init__(self, run_id: str, graph_id: str, state: Dict[str, Any]):
        self.run_id = run_id
        self.graph_id = graph_id
        self.state = state
        self.logs = []
        self.current_node = None
        self.done = False

class GraphRunner:
    def __init__(self):
        self.graphs: Dict[str, Graph] = {}
        self.runs: Dict[str, RunRecord] = {}

    def create_graph(self, graph: Graph) -> str:
        gid = str(uuid.uuid4())
        self.graphs[gid] = graph
        return gid

    async def _execute_node(self, node: Node, state: Dict[str, Any]):
        result = node.func(state)
        if asyncio.iscoroutine(result):
            return await result
        return result

    async def run(self, graph_id: str, initial_state: Dict[str, Any]):
        graph = self.graphs[graph_id]
        run_id = str(uuid.uuid4())
        run = RunRecord(run_id, graph_id, initial_state.copy())
        self.runs[run_id] = run

        node_name = graph.start

        while node_name:
            run.current_node = node_name
            node = graph.nodes[node_name]
            run.logs.append(f"START {node_name}")

            run.state = await self._execute_node(node, run.state)
            run.logs.append(f"END {node_name}")

            if node_name in graph.loops:
                if graph.loops[node_name](run.state):
                    run.logs.append(f"LOOP {node_name} repeating")
                    continue

            node_name = graph.edges.get(node_name)

        run.done = True
        return run.state, run.logs

    def get_run(self, run_id: str):
        return self.runs.get(run_id)

runner = GraphRunner()
