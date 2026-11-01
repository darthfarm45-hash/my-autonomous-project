#!/usr/bin/env python3
"""
Zero-Cost Multi-Agent AI Bridge
100% Free Architecture utilizing:
- Groq Cloud (Free Tier) -> The QA Product Manager (Test Generation via Llama 3.3 70B)
- Local Ollama (Apple Silicon M4) -> The Infinite Laborer (Code Generation via Qwen 2.5 14B)
- OpenRouter (Free Tier) -> The QA Debugger (Traceback Diagnosis via DeepSeek R1 :free)
- Google Gemini (Free Tier) -> The Staff Code Reviewer & Architect (Gemini 1.5 Pro / Flash)
"""

import os
import sys
import json
import urllib.request
import urllib.error

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    v = v.strip().strip('"').strip("'")
                    if k not in os.environ:
                        os.environ[k] = v

load_env()

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b")

# =====================================================================
# 1. LOCAL OLLAMA (The Infinite Laborer - 100% Free & Offline)
# =====================================================================
def query_ollama(prompt: str, system: str = None, model: str = None) -> str:
    url = f"{OLLAMA_HOST.rstrip('/')}/api/generate"
    payload = {
        "model": model or OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "top_p": 0.9}
    }
    if system:
        payload["system"] = system

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res.get("response", "")
    except Exception as e:
        return f"[Local Ollama Error]: Could not connect to {url}: {e}"

# =====================================================================
# 2. GROQ (The QA Product Manager - 100% Free Tier via Llama 3.3 70B)
# =====================================================================
def query_groq(prompt: str, system: str = None, model: str = "openai/gpt-oss-120b") -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("[AI Bridge] GROQ_API_KEY not found in .env; falling back to local Ollama.", file=sys.stderr)
        return query_ollama(prompt, system=system or "You are a Senior QA Product Manager.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}", "User-Agent": "AutonomousAgent/1.0"}
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {"model": model, "messages": messages, "temperature": 0.2}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[AI Bridge] Groq API call failed ({e}); falling back to local Ollama.", file=sys.stderr)
        return query_ollama(prompt, system=system)

# Alias for Product Manager test generation
def query_product_manager(prompt: str, system: str = None) -> str:
    return query_gemini(prompt, system=system or "You are a Senior QA Product Manager. Generate comprehensive PyTest suites with strict edge case coverage.")

# =====================================================================
# 3. OPENROUTER (The QA Debugger - 100% Free Tier via DeepSeek R1 :free)
# =====================================================================
def query_openrouter(prompt: str, system: str = None, model: str = "openrouter/free") -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        # Fallback to Groq DeepSeek Distill or local Ollama
        if os.environ.get("GROQ_API_KEY"):
            return query_gemini(prompt, system=system, model="deepseek-r1-distill-llama-70b")
        return query_ollama(prompt, system=system or "You are an expert surgical code debugger.")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}", "User-Agent": "AutonomousAgent/1.0",
        "HTTP-Referer": "https://github.com/connorking/autonomous-workspace",
        "X-Title": "Autonomous Agent Workspace"
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {"model": model, "messages": messages, "temperature": 0.1}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[AI Bridge] OpenRouter API call failed ({e}); falling back to local Ollama.", file=sys.stderr)
        return query_ollama(prompt, system=system)

# Alias for QA Debugger traceback fixing
def query_qa_debugger(prompt: str, system: str = None) -> str:
    return query_gemini(prompt, system=system or "You are an expert surgical code debugger. Analyze the traceback and provide the corrected code.")

# =====================================================================
# 4. GOOGLE GEMINI (The Staff Code Reviewer & Architect - 100% Free Tier)
# =====================================================================
def query_gemini(prompt: str, system: str = None, model: str = "gemini-2.5-flash") -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[AI Bridge] GEMINI_API_KEY not found in .env; falling back to local Ollama.", file=sys.stderr)
        return query_ollama(prompt, system=system or "You are a Principal Software Architect and Security Auditor.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    contents = [{"parts": [{"text": prompt}]}]
    payload = {"contents": contents}
    if system:
        payload["systemInstruction"] = {"parts": [{"text": system}]}

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"[AI Bridge] Gemini API call failed ({e}); falling back to local Ollama.", file=sys.stderr)
        return query_ollama(prompt, system=system)

# Alias for Staff Code Reviewer audit
def query_staff_reviewer(prompt: str, system: str = None) -> str:
    return query_gemini(prompt, system=system or "You are a Principal Software Architect and Security Auditor. Review the code diff for security, architecture, and edge cases.")
