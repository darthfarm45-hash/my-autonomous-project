#!/usr/bin/env python3
"""
Ollama Worker Script: The Infinite Laborer
Bridges Devin / local automation loops to the local Qwen 2.5:14b model running in Ollama.
Generates code, data models, or boilerplate without external API limits.
"""

import os
import sys
import argparse
import json
import urllib.request
import urllib.error

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b-instruct-q4_K_M")

def query_ollama(prompt: str, system_prompt: str = None, host: str = DEFAULT_HOST, model: str = DEFAULT_MODEL) -> str:
    url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
        }
    }
    if system_prompt:
        payload["system"] = system_prompt

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "")
    except urllib.error.URLError as e:
        sys.stderr.write(f"\n[Error] Could not connect to Ollama at {url}: {e}\n")
        sys.stderr.write("Make sure Ollama is running (`open -a Ollama` or `ollama serve`).\n")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Query local Ollama Qwen model for automated code generation.")
    parser.add_argument("--prompt", "-p", type=str, help="Prompt text. If omitted, reads from standard input.")
    parser.add_argument("--system", "-s", type=str, default="You are an expert autonomous software engineer. Return clean, production-ready, strictly formatted code.", help="Optional system prompt.")
    parser.add_argument("--model", "-m", type=str, default=DEFAULT_MODEL, help=f"Ollama model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--host", type=str, default=DEFAULT_HOST, help=f"Ollama API URL (default: {DEFAULT_HOST})")
    parser.add_argument("--output", "-o", type=str, help="Optional output file path to write generated code.")

    args = parser.parse_args()

    if args.prompt:
        prompt = args.prompt
    else:
        if sys.stdin.isatty():
            print("Enter prompt (Ctrl+D to submit):", file=sys.stderr)
        prompt = sys.stdin.read().strip()

    if not prompt:
        print("[Error] No prompt provided.", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Querying local model '{args.model}'...", file=sys.stderr)
    output = query_ollama(prompt=prompt, system_prompt=args.system, host=args.host, model=args.model)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[+] Output written to {args.output}", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()
