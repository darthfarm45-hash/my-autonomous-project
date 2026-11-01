#!/usr/bin/env python3
"""
Staff Reviewer Harness (Zero-Cost Architecture)
Packages git diffs into a strict staff-level security, architecture,
and optimization audit report using Google Gemini (Free Tier) or local Ollama.
"""

import os
import sys
import argparse
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, "scripts"))
from ai_bridge import query_staff_reviewer

def get_git_diff(target: str = None) -> str:
    cmd = ["git", "diff"]
    if target:
        cmd.append(target)
    try:
        diff = subprocess.check_output(cmd, cwd=WORKSPACE_ROOT, text=True)
        if not diff.strip():
            diff = subprocess.check_output(["git", "diff", "--staged"], cwd=WORKSPACE_ROOT, text=True)
        if not diff.strip():
            diff = subprocess.check_output(["git", "diff", "HEAD~1"], cwd=WORKSPACE_ROOT, text=True)
        return diff
    except Exception as e:
        return f"[Error retrieving git diff]: {e}"

def main():
    parser = argparse.ArgumentParser(description="Package git diffs for Staff Code Review.")
    parser.add_argument("--target", "-t", type=str, default=None, help="Target git commit/ref to diff against.")
    parser.add_argument("--output", "-o", type=str, default="specs/AUDIT_REPORT.md", help="File to write audit report.")

    args = parser.parse_args()

    diff_text = get_git_diff(args.target)
    if not diff_text.strip():
        print("[!] No git diff detected. Please ensure you have changes or commits.", file=sys.stderr)
        sys.exit(0)

    prompt = (
        "# Staff-Level Code Review Request\n\n"
        "Please perform a rigorous staff-level code review of the following git diff.\n"
        "Examine:\n"
        "1. Security vulnerabilities (OWASP, injection, memory leaks, auth flaws)\n"
        "2. Architectural integrity and modular separation\n"
        "3. Performance optimizations and computational bottlenecks\n"
        "4. Test coverage completeness and unhandled edge cases\n\n"
        "## Git Diff\n"
        f"```diff\n{diff_text}\n```\n"
    )

    print("[*] Conducting Staff Code Review via Google Gemini (Free Tier) / Ollama...", file=sys.stderr)
    review = query_staff_reviewer(prompt)
    full_report = f"{prompt}\n\n## Staff Review Feedback\n\n{review}\n"

    output_path = os.path.join(WORKSPACE_ROOT, args.output)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_report)

    print(f"[+] Staff audit report generated at: {output_path}")

if __name__ == "__main__":
    main()
