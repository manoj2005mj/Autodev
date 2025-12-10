from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver # <--- NEW: For pausing
from src.core.state import GraphState

# Import Nodes
from src.agents.architect import architect_node
from src.agents.frontend import frontend_node
from src.agents.backend import backend_node
from src.agents.human import human_node
from src.agents.reflector import reflector_node
from src.agents.router import route_after_reflection

def create_graph():
    workflow = StateGraph(GraphState)

    # 1. Add Nodes
    workflow.add_node("architect", architect_node)
    workflow.add_node("frontend", frontend_node)
    workflow.add_node("backend", backend_node)
    workflow.add_node("human", human_node)
    workflow.add_node("reflector", reflector_node)
    
    # 2. Define Edges
    workflow.set_entry_point("architect")
    workflow.add_edge("architect", "frontend")
    workflow.add_edge("architect", "backend")
    workflow.add_edge("frontend", "human")
    workflow.add_edge("backend", "human")
    workflow.add_edge("human", "reflector")
    
    workflow.add_conditional_edges(
        "reflector",
        route_after_reflection,
        {
            "frontend": "frontend",
            "backend": "backend",
            "end_node": END
        }
    )
    
    # 3. Compile with Persistence and Interrupt
    # We want to PAUSE strictly before the 'human' node executes
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory, interrupt_before=["human"])