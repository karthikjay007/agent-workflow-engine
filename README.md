# Agent Workflow Engine (FastAPI)

A minimal workflow/graph execution engine built using **Python** and **FastAPI**.  
The system supports node-based execution, shared state passing, loops, branching, and a simple tool registry.  
This project demonstrates backend fundamentals such as API design, async execution, and clean code structure.

---

## 🚀 Features

### ✔ Workflow Engine  
- Nodes as Python functions (sync or async)  
- Shared dictionary state passed between nodes  
- Edge-based routing (simple directed graph)  
- Conditional looping (iterate a node until condition becomes false)  
- Optional branching  
- Execution logs for every node  

### ✔ Tool Registry  
- Register reusable helper functions  
- Nodes can call tools dynamically  

### ✔ FastAPI Endpoints  
| Endpoint | Purpose |
|---------|---------|
| `POST /graph/create` | Creates a workflow graph |
| `POST /graph/run` | Executes the workflow |
| `GET /graph/state/{run_id}` | Fetches state of an ongoing workflow |

### ✔ Example Workflow Included  
**Adaptive Spam Detection Workflow**  
Steps:  
1. Extract metadata  
2. Compute spam score  
3. Detect patterns using registry tool  
4. Suggest rule  
5. Loop until score < threshold  

This workflow is completely original and not one of the assignment's default options.

---

## 📁 Project Structure

