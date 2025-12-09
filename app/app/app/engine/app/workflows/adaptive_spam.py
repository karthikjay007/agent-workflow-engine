import asyncio
from typing import Dict, Any
from engine.registry import registry
from engine.graph import Node, Graph

async def extract_metadata(state: Dict[str, Any]):
    txt = state.get("email", "")
    state["meta"] = {
        "length": len(txt),
        "links": txt.count("http"),
        "symbols": sum(1 for c in txt if c in "!@#$%")
    }
    await asyncio.sleep(0)
    return state

async def spam_score(state: Dict[str, Any]):
    m = state["meta"]
    score = m["length"] * 0.01 + m["links"] * 0.6 + m["symbols"] * 0.5
    detect = registry.get("pattern_detector")
    score += detect(state["email"]) * 0.7
    state["spam_score"] = score
    await asyncio.sleep(0)
    return state

async def suggest_rule(state: Dict[str, Any]):
    threshold = state.get("threshold", 5)
    state["rule"] = "BLOCK" if state["spam_score"] >= threshold else "REVIEW"
    await asyncio.sleep(0)
    return state

nodes = {
    "extract": Node("extract", extract_metadata),
    "score": Node("score", spam_score),
    "suggest": Node("suggest", suggest_rule),
}

edges = {
    "extract": "score",
    "score": "suggest",
    "suggest": None,
}

loops = {
    "suggest": lambda s: s.get("spam_score", 0) >= s.get("threshold", 5)
}

def build_graph():
    return Graph(nodes=nodes, edges=edges, start="extract", loops=loops)

registry.register("pattern_detector", lambda txt: txt.count("!!!"))
