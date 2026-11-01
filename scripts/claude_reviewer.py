#!/usr/bin/env python3
"""
Claude Staff Reviewer Harness
Packages git diffs into a strict staff-level security, architecture,
and optimization audit report.
"""

import os
import sys
import argparse
import subprocess
import json
import urllib.request
import urllib.error

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

def get_git_diff(target: str = None) -> str:
    cmd = ["git", "diff"]
    if target:
        cmd.append(target)
    try:
        diff = subprocess.check_output(cmd, text=True)
        if not diff.strip():
            # If no unstaged diff, check staged or previous commit
            diff = subprocess.check_output(["git", "diff", "--staged"], text=True)
        if not diff.strip():
            diff = subprocess.check_output(["git", "diff", "HEAD~1"], text=True)
        return diff
    except Exception as e:
        return f"[Error retrieving git diff]: {e}"

def ask_claude(api_key: str, audit_prompt: str) -> str:
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4096,
        "temperature": 0.2,
        "system": "You are a Principal Software Architect and Security Auditor. Perform a rigorous, thorough code review focusing on security vulnerabilities, edge cases, scalability, and code cleanliness.",
        "messages": [
            {
                "role": "user",
                "content": audit_prompt
            }
        ]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(CLAUDE_API_URL, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json["content"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"[Error from Anthropic API]: HTTP {e.code} - {e.read().decode('utf-8')}"
    except Exception as e:
        return f"[Connection Error]: {e}"

def main():
    parser = argparse.ArgumentParser(description="Package git diffs for Claude Staff Code Review.")
    parser.add_argument("--target", "-t", type=str, default=None, help="Target git commit/ref to diff against (e.g., HEAD~1, origin/main).")
    parser.add_argument("--api-key", type=str, default=os.environ.get("ANTHROPIC_API_KEY"), help="Anthropic API key.")
    parser.add_argument("--output", "-o", type=str, default="specs/AUDIT_REQUEST.md", help="File to write audit prompt/report.")

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

    if args.api_key:
        print("[*] Sending diff to Claude API for automated review...", file=sys.stderr)
        review = ask_claude(args.api_key, prompt)
        full_report = f"{prompt}\n\n## Claude Staff Review Feedback\n\n{review}\n"
    else:
        print("[*] ANTHROPIC_API_KEY not found. Prepared review prompt for Claude web/app.", file=sys.stderr)
        full_report = prompt

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(full_report)

    print(f"[+] Audit package generated at: {args.output}")

if __name__ == "__main__":
    main()
