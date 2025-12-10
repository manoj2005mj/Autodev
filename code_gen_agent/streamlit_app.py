import streamlit as st
import json
import os
from dotenv import load_dotenv
from src.core.graph import create_graph
from src.core.state import GraphState
from langchain_core.messages import HumanMessage
from typing import Any, Dict, cast
from langchain_core.runnables import RunnableConfig

# Load Env
load_dotenv()

st.set_page_config(page_title="AutoDev Agent", layout="wide")
st.title("🤖 AutoDev: AI Software Architect")

# --- Session State Management ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "demo_thread_1"
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Project Controls ---
with st.sidebar:
    st.header("Project Configuration")
    user_story = st.text_area("User Story", "Build a simple To-Do List app with a dark mode UI.")
    start_btn = st.button("🚀 Start New Project")
    
    if start_btn:
        st.session_state.messages = []
        # Initial Run
        config: RunnableConfig = {"configurable": {"thread_id": st.session_state.thread_id}}
        initial_state: GraphState = {
            "user_story": user_story,
            "iteration_count": 0,
            "messages": [],
            "api_spec": "",
            "architecture_plan": "",
            "frontend_files": {},
            "backend_files": {},
            "infra_files": {},
            "human_feedback": "",
            "structured_errors": []
        }
        
        with st.spinner("Architecting & Coding..."):
            # Run until the interrupt (Human Node)
            for event in st.session_state.graph.stream(initial_state, config=config):
                pass 
            st.rerun()

# --- Main Logic: Retrieve Current State ---
config: RunnableConfig = {"configurable": {"thread_id": st.session_state.thread_id}}
# Get the current snapshot of the graph (paused state)
snapshot = st.session_state.graph.get_state(config)

if snapshot.values:
    state = snapshot.values
    
    # 1. Display Architecture Plan
    if "api_spec" in state:
        with st.expander("📄 Architecture Plan & API Spec", expanded=False):
            st.json(json.loads(state["api_spec"]))
            st.markdown(state.get("architecture_plan", ""))

    # 2. Code Review Tabs
    st.subheader("💻 Generated Codebase")
    tab1, tab2 = st.tabs(["Frontend (React)", "Backend (FastAPI)"])
    
    with tab1:
        files = state.get("frontend_files", {})
        if files:
            for fname, code in files.items():
                st.markdown(f"**`{fname}`**")
                st.code(code, language="javascript")
        else:
            st.info("Frontend code not generated yet.")

    with tab2:
        files = state.get("backend_files", {})
        if files:
            for fname, code in files.items():
                st.markdown(f"**`{fname}`**")
                st.code(code, language="python")
        else:
            st.info("Backend code not generated yet.")

    # 3. Human Feedback Loop (The "Sandbox")
    st.divider()
    st.subheader("🛠️ Sandbox / Human Review")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        feedback = st.text_input("Paste Error Log (or type 'success')", placeholder="TypeError: cannot read property 'map'...")
    with col2:
        submit_feedback = st.button("Submit Feedback")

    if submit_feedback and feedback:
        # Resume the graph!
        # We update the state with the human feedback and resume
        with st.spinner("Analyzing Feedback & Fixing Code..."):
            
            # Update the state 'human_feedback' key
            st.session_state.graph.update_state(
                config, 
                {"human_feedback": feedback}, 
                as_node="human" # We pretend to be the human node
            )
            
            # Continue execution (will go to Reflector -> Router -> Agents)
            for event in st.session_state.graph.stream(None, config=config):
                pass
            
            st.rerun()

else:
    st.info("👈 Enter a User Story in the sidebar and click Start to begin.")