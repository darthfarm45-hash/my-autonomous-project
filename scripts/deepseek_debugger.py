#!/usr/bin/env python3
"""
QA Debugger Harness (Zero-Cost Architecture)
Captures test failure tracebacks and queries OpenRouter Free DeepSeek R1 (:free),
Groq DeepSeek Distill, or local Ollama for surgical fixes.
"""

import os
import sys
import argparse
from datetime import datetime

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, "scripts"))
from ai_bridge import query_qa_debugger

def main():
    parser = argparse.ArgumentParser(description="Zero-Cost QA Debugger Harness for tracebacks and test failures.")
    parser.add_argument("--traceback-file", "-f", type=str, help="Path to file containing pytest/terminal traceback.")
    parser.add_argument("--context", "-c", type=str, help="Path to relevant source code file being debugged.")
    parser.add_argument("--output-log", "-o", type=str, help="Path to save debug session log.")

    args = parser.parse_args()

    # Read traceback
    if args.traceback_file and os.path.exists(args.traceback_file):
        with open(args.traceback_file, "r", encoding="utf-8") as f:
            traceback_text = f.read()
    else:
        if sys.stdin.isatty():
            print("Paste terminal traceback (Ctrl+D to submit):", file=sys.stderr)
        traceback_text = sys.stdin.read().strip()

    if not traceback_text:
        print("[Error] No traceback provided.", file=sys.stderr)
        sys.exit(1)

    # Read optional context source code
    context_code = ""
    if args.context and os.path.exists(args.context):
        with open(args.context, "r", encoding="utf-8") as f:
            context_code = f"\n\n--- Source Code ({args.context}) ---\n" + f.read()

    debug_prompt = f"Analyze this test/terminal error traceback and provide a surgical fix:\n\n```\n{traceback_text}\n```{context_code}"

    print("[*] Routing failure to Zero-Cost QA Debugger (DeepSeek R1 Free / Groq / Ollama)...", file=sys.stderr)
    fix_advice = query_qa_debugger(debug_prompt)

    # Save to log
    log_dir = os.path.join(WORKSPACE_ROOT, "logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = args.output_log or os.path.join(log_dir, f"qa_debug_{timestamp}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"=== TRACEBACK ===\n{traceback_text}\n\n=== DIAGNOSIS & SURGICAL FIX ===\n{fix_advice}\n")

    print(f"[+] Diagnosis complete. Log saved to {log_path}\n", file=sys.stderr)
    print(fix_advice)

if __name__ == "__main__":
    main()
