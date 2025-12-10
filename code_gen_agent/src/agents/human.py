import os
from langchain_core.messages import HumanMessage
from src.core.state import GraphState
from src.utils.llm_helper import print_message_event

def save_files(base_path, files_dict):
    """Helper to write dict of files to disk"""
    if not files_dict: return
    for path, content in files_dict.items():
        full_path = os.path.join(base_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

def human_node(state: GraphState):
    print("\n" + "="*60)
    print("👨‍💼 HUMAN REVIEW (SANDBOX)")
    print("="*60)
    
    # 1. Write files to output directory
    output_dir = "output"
    save_files(output_dir, state.get("frontend_files", {}))
    save_files(output_dir, state.get("backend_files", {}))
    
    print(f"\n✅ Code has been written to ./{output_dir}")
    print("\n🔧 Action Required: Run the code manually in another terminal.")
    print("   Type 'success' if it works, or paste the error log below:\n")
    
    # 2. Capture Human Feedback
    feedback = input(">> ")
    
    human_msg = HumanMessage(content=feedback)
    print_message_event("human", human_msg.content, "new_human_feedback")
    
    return {
        "human_feedback": feedback,
        "messages": [human_msg]
    }