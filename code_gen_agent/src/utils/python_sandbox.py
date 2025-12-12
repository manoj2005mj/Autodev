"""
Python-based sandbox for testing generated code.
No Node.js dependencies required.
"""

import json
import subprocess
import os
import shutil
from pathlib import Path
from datetime import datetime


class PythonSandbox:
    """Execute generated code in an isolated environment."""

    def __init__(self, output_dir: str = "sandbox_env"):
        """Initialize sandbox directory."""
        self.output_dir = output_dir
        self.log_file = os.path.join(output_dir, "sandbox_logs.json")
        self._init_sandbox()

    def _init_sandbox(self):
        """Create sandbox directories."""
        os.makedirs(self.output_dir, exist_ok=True)

    def save_generated_files(self, frontend_files: dict, backend_files: dict, infra_files: dict):
        """Save generated code files to sandbox."""
        # Frontend
        fe_dir = os.path.join(self.output_dir, "frontend")
        os.makedirs(fe_dir, exist_ok=True)
        for filename, content in frontend_files.items():
            filepath = os.path.join(fe_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

        # Backend
        be_dir = os.path.join(self.output_dir, "backend")
        os.makedirs(be_dir, exist_ok=True)
        for filename, content in backend_files.items():
            filepath = os.path.join(be_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

        # Infrastructure
        if infra_files:
            infra_dir = os.path.join(self.output_dir, "infra")
            os.makedirs(infra_dir, exist_ok=True)
            for filename, content in infra_files.items():
                filepath = os.path.join(infra_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

        print(f"✅ Saved {len(frontend_files)} frontend files")
        print(f"✅ Saved {len(backend_files)} backend files")
        if infra_files:
            print(f"✅ Saved {len(infra_files)} infra files")

    def validate_python_syntax(self, python_files: dict) -> dict:
        """Validate Python file syntax."""
        errors = {}
        for filename, content in python_files.items():
            try:
                compile(content, filename, "exec")
            except SyntaxError as e:
                errors[filename] = f"SyntaxError: {str(e)}"
        return errors

    def validate_json_format(self, json_files: dict) -> dict:
        """Validate JSON file format."""
        errors = {}
        for filename, content in json_files.items():
            try:
                json.loads(content)
            except json.JSONDecodeError as e:
                errors[filename] = f"JSONDecodeError: {str(e)}"
        return errors

    def run_tests(self) -> dict:
        """Run basic validation tests on generated code."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "backend_syntax_errors": {},
            "frontend_structure_check": {},
            "docker_compose_valid": False,
        }

        # Check backend Python files
        be_dir = os.path.join(self.output_dir, "backend")
        if os.path.exists(be_dir):
            python_files = {}
            for root, dirs, files in os.walk(be_dir):
                for file in files:
                    if file.endswith(".py"):
                        filepath = os.path.join(root, file)
                        with open(filepath, "r", encoding="utf-8") as f:
                            python_files[file] = f.read()

            if python_files:
                syntax_errors = self.validate_python_syntax(python_files)
                results["backend_syntax_errors"] = syntax_errors
                if not syntax_errors:
                    print("✅ All Python files have valid syntax")
                else:
                    print(f"⚠️ Found {len(syntax_errors)} syntax error(s)")

        # Check frontend structure
        fe_dir = os.path.join(self.output_dir, "frontend")
        if os.path.exists(fe_dir):
            files = os.listdir(fe_dir)
            results["frontend_structure_check"] = {
                "has_package_json": "package.json" in files,
                "has_index_html": "index.html" in files or "public/index.html" in str(os.listdir(fe_dir)),
                "total_files": len(files),
            }
            print(f"✅ Frontend has {len(files)} files")

        # Check docker-compose
        infra_dir = os.path.join(self.output_dir, "infra")
        if os.path.exists(infra_dir):
            docker_file = os.path.join(infra_dir, "docker-compose.yml")
            if os.path.exists(docker_file):
                try:
                    import yaml
                    with open(docker_file, "r") as f:
                        yaml.safe_load(f)
                    results["docker_compose_valid"] = True
                    print("✅ docker-compose.yml is valid")
                except ImportError:
                    # YAML not available, just check it's not empty
                    with open(docker_file, "r") as f:
                        content = f.read().strip()
                    results["docker_compose_valid"] = len(content) > 0
                    if results["docker_compose_valid"]:
                        print("✅ docker-compose.yml exists and is not empty")
                except Exception as e:
                    print(f"⚠️ docker-compose.yml validation failed: {e}")

        return results

    def save_logs(self, logs: dict):
        """Save test results to JSON."""
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
        print(f"📄 Logs saved to {self.log_file}")

    def cleanup(self):
        """Clean up sandbox environment."""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
            print(f"🧹 Cleaned up sandbox at {self.output_dir}")
