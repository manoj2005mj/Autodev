import json
from langchain_core.messages import AIMessage
from src.core.state import GraphState
from src.utils.llm_helper import invoke_llm_json

INFRA_PROMPT = """You are a DevOps Engineer.
Goal: Generate a 'docker-compose.yml' to run the frontend and backend.
Context:
- Frontend: Node.js/React (Dockerfile usually in ./frontend)
- Backend: Python/FastAPI (Dockerfile usually in ./backend)
- Database: Postgres (if needed by API Spec)

Output:
Strict JSON: {"docker-compose.yml": "content...", "frontend/Dockerfile": "...", "backend/Dockerfile": "..."}
Ensure services are named 'frontend' and 'backend'.
"""

def infra_node(state: GraphState):
    print("--- INFRA: Generating Docker Config ---")
    
    api_spec = state["api_spec"]
    # We pass the plan so it knows if it needs a DB
    plan = state["architecture_plan"]
    
    user_prompt = f"Generate Docker config for this system.\nPlan: {plan}\nAPI: {api_spec}"
    
    files = invoke_llm_json(INFRA_PROMPT, user_prompt)
    
    return {
        "infra_files": files,
        "messages": [AIMessage(content="Docker configuration generated.")]
    }