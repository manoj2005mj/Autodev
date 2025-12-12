#!/usr/bin/env python3
"""
Docker Environment Validation Script
Verifies all fixes are working correctly without Docker
"""

import sys
import json
from pathlib import Path

def validate_no_emojis():
    """Check all Python files for emoji characters"""
    print("[CHECK] Scanning for emoji characters...")
    
    py_files = list(Path('src').glob('**/*.py'))
    emoji_patterns = {
        '❌': 'CROSS_MARK',
        '✅': 'CHECK_MARK',
        '📋': 'CLIPBOARD',
        '📊': 'CHART',
        '🤖': 'ROBOT',
        '🏃': 'RUNNER',
        '✨': 'SPARKLES',
        '👋': 'WAVING_HAND'
    }
    
    issues = []
    for py_file in py_files:
        content = py_file.read_text(encoding='utf-8', errors='ignore')
        for emoji, name in emoji_patterns.items():
            if emoji in content:
                issues.append(f"  {py_file}: contains emoji ({name})")
    
    if issues:
        print(f"[FAIL] Found {len(issues)} emoji issues:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("[OK] No emoji characters found")
        return True

def validate_imports():
    """Check all required imports are available"""
    print("\n[CHECK] Validating imports...")
    
    try:
        from src.agents.sandbox import sandbox_node
        from src.utils.python_sandbox import PythonSandbox
        from src.core.state import GraphState
        print("[OK] All imports successful")
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False

def validate_sandbox_integration():
    """Test sandbox node with sample code"""
    print("\n[CHECK] Testing sandbox integration...")
    
    try:
        from src.agents.sandbox import sandbox_node
        from src.core.state import GraphState
        from langchain_core.messages import BaseMessage
        
        test_state: GraphState = {  # type: ignore
            "messages": [],
            "user_story": "Test",
            "api_spec": "",
            "architecture_plan": "",
            "frontend_files": {"App.tsx": "export default () => null"},
            "backend_files": {"main.py": "print('test')"},
            "infra_files": {},
            "human_feedback": "",
            "structured_errors": [],
            "iteration_count": 0,
        }
        
        result = sandbox_node(test_state)
        
        if "sandbox_logs" not in result:
            print("[FAIL] sandbox_logs not in result")
            return False
        
        logs = json.loads(result["sandbox_logs"])
        if "status" not in logs:
            print("[FAIL] No status in sandbox logs")
            return False
            
        print(f"[OK] Sandbox test passed with status: {logs.get('status')}")
        return True
        
    except Exception as e:
        print(f"[FAIL] Sandbox test failed: {e}")
        return False

def validate_state_schema():
    """Check GraphState doesn't have undefined fields"""
    print("\n[CHECK] Validating GraphState schema...")
    
    try:
        from src.core.state import GraphState
        import typing
        
        # Get type hints
        hints = typing.get_type_hints(GraphState)
        
        # Check for sandbox_logs (should not exist)
        if 'sandbox_logs' in hints:
            print("[FAIL] sandbox_logs field should not exist in GraphState")
            return False
        
        # Check for required fields
        required = ['messages', 'user_story', 'frontend_files', 'backend_files']
        for field in required:
            if field not in hints:
                print(f"[FAIL] Missing required field: {field}")
                return False
        
        print(f"[OK] GraphState schema valid with {len(hints)} fields")
        return True
        
    except Exception as e:
        print(f"[FAIL] State validation failed: {e}")
        return False

def main():
    """Run all validations"""
    print("="*60)
    print("Docker Environment Validation Suite")
    print("="*60)
    
    results = {
        "Emoji Check": validate_no_emojis(),
        "Imports Check": validate_imports(),
        "State Schema Check": validate_state_schema(),
        "Sandbox Integration": validate_sandbox_integration(),
    }
    
    print("\n" + "="*60)
    print("Validation Summary")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n[SUCCESS] All Docker environment fixes validated!")
        return 0
    else:
        print(f"\n[ERROR] {total - passed} checks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
