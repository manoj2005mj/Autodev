import json
import os
from datetime import datetime
from src.core.state import GraphState
from src.utils.python_sandbox import PythonSandbox


def sandbox_node(state: GraphState):
    """
    Run generated code in a Python-based sandbox environment.
    Tests syntax and structure without requiring Node.js.
    """
    print("\n" + "="*60)
    print("🏃 SANDBOX: Testing Generated Code")
    print("="*60)
    
    # Initialize sandbox
    sandbox = PythonSandbox(output_dir="sandbox_env")
    
    # Save generated files
    frontend_files = state.get("frontend_files", {})
    backend_files = state.get("backend_files", {})
    infra_files = state.get("infra_files", {})
    
    if not frontend_files and not backend_files:
        logs = {"error": "No code generated yet"}
        return {"sandbox_logs": json.dumps(logs)}
    
    try:
        # Save files to sandbox
        sandbox.save_generated_files(frontend_files, backend_files, infra_files)
        
        # Run validation tests
        print("\n📋 Running validation tests...")
        test_results = sandbox.run_tests()
        
        # Save logs
        sandbox.save_logs(test_results)
        
        # Format logs for display
        logs_summary = {
            "timestamp": test_results.get("timestamp"),
            "backend_syntax_errors": test_results.get("backend_syntax_errors", {}),
            "frontend_ok": test_results.get("frontend_structure_check", {}).get("total_files", 0) > 0,
            "docker_valid": test_results.get("docker_compose_valid", False),
        }
        
        # Check for errors
        if test_results.get("backend_syntax_errors"):
            print("❌ Syntax errors found in backend code")
            logs_summary["status"] = "FAILED"
        else:
            print("✅ All tests passed")
            logs_summary["status"] = "SUCCESS"
        
        return {"sandbox_logs": json.dumps(logs_summary, indent=2)}
        
    except Exception as e:
        error_log = {
            "error": str(e),
            "type": type(e).__name__,
            "timestamp": datetime.now().isoformat()
        }
        return {"sandbox_logs": json.dumps(error_log, indent=2)}
    finally:
        # Optional: Clean up sandbox (comment out to keep for debugging)
        pass