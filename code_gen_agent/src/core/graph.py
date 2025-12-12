from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.core.state import GraphState

# Nodes
from src.agents.architect import architect_node
from src.agents.frontend import frontend_node
from src.agents.backend import backend_node
from src.agents.infra import infra_node  # <--- NEW
from src.agents.sandbox import sandbox_node # <--- NEW (Replaces Human)
from src.agents.reflector import reflector_node
from src.agents.router import route_after_reflection

def create_graph():
    workflow = StateGraph(GraphState)

    # 1. Add Nodes
    workflow.add_node("architect", architect_node)
    workflow.add_node("frontend", frontend_node)
    workflow.add_node("backend", backend_node)
    workflow.add_node("infra", infra_node) # <--- NEW
    workflow.add_node("sandbox", sandbox_node) # <--- NEW
    workflow.add_node("reflector", reflector_node)
    
    # 2. Edges
    workflow.set_entry_point("architect")
    
    # Fan-Out to THREE builders
    workflow.add_edge("architect", "frontend")
    workflow.add_edge("architect", "backend")
    workflow.add_edge("architect", "infra") # <--- NEW
    
    # Fan-In to Sandbox
    workflow.add_edge("frontend", "sandbox")
    workflow.add_edge("backend", "sandbox")
    workflow.add_edge("infra", "sandbox")
    
    # Sandbox -> Reflector
    workflow.add_edge("sandbox", "reflector")
    
    # Conditional Routing
    workflow.add_conditional_edges(
        "reflector",
        route_after_reflection,
        {
            "frontend": "frontend",
            "backend": "backend",
            "infra": "infra",  # Ensure infra can be fixed too
            "end_node": END
        }
    )
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory, interrupt_before=["reflector"])# No interrupt needed now!