#!/usr/bin/env python3
"""
Autonomous Self-Healing Test Loop
Executes test suites, captures failures, and automatically routes tracebacks
to the DeepSeek debugger harness.
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def run_tests(test_path: str = "tests") -> tuple[int, str]:
    cmd = ["pytest", test_path, "-v", "--tb=short"]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return proc.returncode, proc.stdout
    except FileNotFoundError:
        return 1, "Error: pytest is not installed or not in PATH. Ensure your .venv is activated."

def main():
    parser = argparse.ArgumentParser(description="Self-healing test runner loop.")
    parser.add_argument("--test-dir", "-t", default="tests", help="Directory of tests to run.")
    parser.add_argument("--max-retries", "-r", type=int, default=3, help="Maximum self-healing attempts.")
    args = parser.parse_args()

    print(f"[*] Starting QA test run in '{args.test_dir}'...")
    ret_code, test_output = run_tests(args.test_dir)

    if ret_code == 0:
        print("\n[✓] All tests passed cleanly! No healing required.")
        sys.exit(0)

    print(f"\n[!] Test run failed with code {ret_code}.")
    
    # Save log
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tb_log = f"logs/failure_{timestamp}.log"
    with open(tb_log, "w", encoding="utf-8") as f:
        f.write(test_output)
    print(f"[*] Traceback captured in {tb_log}")

    print("\n[*] Routing failure to DeepSeek debugger harness...")
    cmd = [sys.executable, "scripts/deepseek_debugger.py", "-f", tb_log]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
