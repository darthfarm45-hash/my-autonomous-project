#!/usr/bin/env python3
"""
DeepSeek QA Debugger Harness
Captures test failure tracebacks, isolates the failing unit tests & source files,
and requests a surgical fix from DeepSeek's reasoning engine.
"""

import os
import sys
import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

def ask_deepseek(api_key: str, prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "deepseek-coder",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert surgical debugger. You receive error tracebacks and related code. "
                    "Analyze the root cause and provide only the necessary fix, explanation, and corrected code snippet."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(DEEPSEEK_API_URL, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return f"[Error from DeepSeek API]: HTTP {e.code} - {err_msg}"
    except Exception as e:
        return f"[Connection Error]: {e}"

def main():
    parser = argparse.ArgumentParser(description="DeepSeek QA Debugger Harness for tracebacks and test failures.")
    parser.add_argument("--traceback-file", "-f", type=str, help="Path to file containing pytest/terminal traceback.")
    parser.add_argument("--context", "-c", type=str, help="Path to relevant source code file being debugged.")
    parser.add_argument("--api-key", type=str, default=os.environ.get("DEEPSEEK_API_KEY"), help="DeepSeek API key (or set DEEPSEEK_API_KEY env var).")
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

    if not args.api_key:
        print("\n[Notice] DEEPSEEK_API_KEY is not set in environment or arguments.", file=sys.stderr)
        print("Generated Debug Package ready to paste into DeepSeek:\n", file=sys.stderr)
        print("="*60)
        print(debug_prompt)
        print("="*60)
        return

    print("[*] Dispatching traceback to DeepSeek Debugger API...", file=sys.stderr)
    fix_advice = ask_deepseek(args.api_key, debug_prompt)

    # Save to log
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = args.output_log or os.path.join(log_dir, f"deepseek_debug_{timestamp}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"=== TRACEBACK ===\n{traceback_text}\n\n=== DEEPSEEK DIAGNOSIS & FIX ===\n{fix_advice}\n")

    print(f"[+] Diagnosis complete. Log saved to {log_path}\n", file=sys.stderr)
    print(fix_advice)

if __name__ == "__main__":
    main()
