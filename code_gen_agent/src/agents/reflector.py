from src.core.state import GraphState
from src.utils.llm_helper import invoke_llm_json, print_message_event
from src.prompts.system_prompts import REFLECTOR_PROMPT

def reflector_node(state: GraphState):
    print("\n" + "="*60)
    print("🔍 REFLECTOR: Analyzing Feedback")
    print("="*60)
    
    feedback = state.get("human_feedback", "")
    iteration = state.get("iteration_count", 0)
    
    print(f"📊 Iteration: {iteration + 1}")
    
    if feedback.lower().strip() in ["success", "done", "looks good"]:
        print("✅ SUCCESS! Code passed all tests. No errors to fix.")
        return {"structured_errors": []}
        
    # Call LLM to parse the error
    print("\n🤖 Parsing error feedback with AI...")
    structured_errors = invoke_llm_json(REFLECTOR_PROMPT, f"Log: {feedback}")
    
    # Ensure it's a list
    if not isinstance(structured_errors, list):
        structured_errors = []
    
    if structured_errors:
        print(f"\n📋 Found {len(structured_errors)} error(s) to fix:")
        for i, err in enumerate(structured_errors, 1):
            agent = err.get('agent', 'unknown')
            instruction = err.get('instruction', 'No instruction')[:100]
            print(f"   {i}. [{agent}] {instruction}...")
    
    return {
        "structured_errors": structured_errors,
        "iteration_count": iteration + 1
    }