from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from engine.runner import runner
from workflows.adaptive_spam import build_graph

app = FastAPI(title="Minimal Workflow Engine")

class CreateGraphRequest(BaseModel):
    example: str = None

class RunGraphRequest(BaseModel):
    graph_id: str
    state: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    g = build_graph()
    gid = runner.create_graph(g)
    app.state.sample_graph_id = gid

@app.post("/graph/create")
async def create_graph(req: CreateGraphRequest):
    if req.example == "adaptive_spam":
        g = build_graph()
        gid = runner.create_graph(g)
        return {"graph_id": gid}
    raise HTTPException(400, "unknown example")

@app.post("/graph/run")
async def run_graph(req: RunGraphRequest):
    try:
        final_state, logs = await runner.run(req.graph_id, req.state)
        return {"final_state": final_state, "logs": logs}
    except KeyError:
        raise HTTPException(404, "graph not found")

@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    run = runner.get_run(run_id)
    if not run:
        raise HTTPException(404, "run not found")
    return {
        "state": run.state,
        "logs": run.logs,
        "current_node": run.current_node,
        "done": run.done
    }
