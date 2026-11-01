#!/usr/bin/env python3
"""
Zero-Cost Autonomous Orchestrator
Coordinates the 100% Free Autonomous Roster:
- Phase 2: Groq (Llama 3.3 70B Free) -> QA Product Manager (Tests & Edge Cases)
- Phase 3: Ollama (Qwen 2.5 14B Local) -> Infinite Laborer (Models & Code Micro-Tasks)
- Phase 4: OpenRouter (DeepSeek R1 Free) -> QA Debugger (Self-Healing Traceback Fixes)
- Phase 5: Google Gemini (Gemini 1.5 Pro Free) -> Staff Code Reviewer (Security & Architecture Audit)
"""

import os
import sys
import re
import subprocess
import argparse

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, "scripts"))

from ai_bridge import query_product_manager, query_ollama, query_qa_debugger, query_staff_reviewer

DEFAULT_SPEC = "specs/MASTER_SPEC.md"

def run_cmd(cmd_list, capture=True):
    try:
        proc = subprocess.run(
            cmd_list,
            cwd=WORKSPACE_ROOT,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.STDOUT if capture else None,
            text=True
        )
        return proc.returncode, proc.stdout if capture else ""
    except Exception as e:
        return 1, str(e)

def main():
    parser = argparse.ArgumentParser(description="Zero-Cost Multi-Agent Autonomous Orchestrator.")
    parser.add_argument("--spec", "-s", default=DEFAULT_SPEC, help="Path to MASTER_SPEC.md")
    args = parser.parse_args()

    spec_path = os.path.join(WORKSPACE_ROOT, args.spec)
    if not os.path.exists(spec_path):
        print(f"[Error] Spec file '{spec_path}' not found.", file=sys.stderr)
        print("Please save your spec into specs/MASTER_SPEC.md first.", file=sys.stderr)
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        spec_content = f.read()

    print("=" * 70)
    print("🚀 LAUNCHING 100% ZERO-COST AUTONOMOUS PIPELINE")
    print(f"📁 Spec: {args.spec}")
    print("🤖 Roster: Groq (Tests) | Ollama Qwen (Code) | OpenRouter DeepSeek (QA) | Gemini (Audit)")
    print("=" * 70)

    # Phase 2: Groq Cloud (QA Product Manager)
    print("\n[Phase 2] Querying Groq Llama 3.3 70B (QA Product Manager) for Test Suite...")
    test_gen_prompt = (
        f"You are the QA Product Manager. Review this software specification:\n\n{spec_content}\n\n"
        "Generate a complete, production-ready PyTest test suite that tests core functionality and edge cases. "
        "Output ONLY valid python test code."
    )
    test_code = query_product_manager(test_gen_prompt)
    clean_test_code = re.sub(r"^```python\s*|\s*```$", "", test_code.strip(), flags=re.MULTILINE)
    test_file_path = os.path.join(WORKSPACE_ROOT, "tests/test_master.py")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(clean_test_code)
    print(f"[✓] Tests generated and saved to {test_file_path}")

    # Phase 3: Ollama Qwen 2.5:14b (Infinite Laborer)
    print("\n[Phase 3] Querying Local Qwen 2.5:14b (Infinite Laborer) to Build Implementation...")
    build_prompt = (
        f"Implement the complete software system specified below adhering to all interfaces required by the test suite.\n\n"
        f"--- SPEC ---\n{spec_content}\n\n--- TEST SUITE ---\n{clean_test_code}\n\n"
        "Output ONLY production-ready Python code implementing the system."
    )
    src_code = query_ollama(build_prompt, system="You are an expert autonomous software engineer. Output only clean, working Python code.")
    clean_src_code = re.sub(r"^```python\s*|\s*```$", "", src_code.strip(), flags=re.MULTILINE)
    src_file_path = os.path.join(WORKSPACE_ROOT, "src/app.py")
    with open(src_file_path, "w", encoding="utf-8") as f:
        f.write(clean_src_code)
    print(f"[✓] Application code generated and saved to {src_file_path}")

    # Phase 4: Self-Healing Test Loop (OpenRouter DeepSeek QA Debugger)
    print("\n[Phase 4] Executing Test Suite & Self-Healing Loop...")
    heal_cmd = [sys.executable, os.path.join(WORKSPACE_ROOT, "scripts/self_heal_runner.py")]
    code, heal_out = run_cmd(heal_cmd, capture=False)

    # Phase 5: Google Gemini (Staff Code Reviewer)
    print("\n[Phase 5] Querying Google Gemini (Staff Reviewer) for Final Architecture & Security Audit...")
    audit_cmd = [sys.executable, os.path.join(WORKSPACE_ROOT, "scripts/claude_reviewer.py"), "-o", "specs/AUDIT_REPORT.md"]
    run_cmd(audit_cmd, capture=False)

    print("\n" + "=" * 70)
    print("🎉 ZERO-COST AUTONOMOUS PIPELINE RUN COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
