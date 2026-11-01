# Autonomous Super-Team Workspace (100% Zero-Cost Architecture)

A zero-touch autonomous engineering pipeline orchestrated across **100% Free Cloud Tiers** and your **Local Apple Silicon M4 Hardware**.

---

## The Zero-Cost AI Roster

| Agent / Model | Tier / Cost | Role in Pipeline | Function |
| :--- | :--- | :--- | :--- |
| **Google Gemini (1.5 Flash/Pro)** | **100% Free** | **The Chief Architect & Staff Reviewer** | Designs `MASTER_SPEC.md` and conducts pre-merge security/architecture code reviews. |
| **Groq (Llama 3.3 70B)** | **100% Free** | **The QA Product Manager** | Generates strict unit test suites and edge cases at ultra-fast inference speeds. |
| **Ollama (Qwen 2.5:14B)** | **100% Free** (Local M4) | **The Infinite Laborer** | Runs locally on your Mac's unified memory; builds models and micro-task code offline. |
| **OpenRouter (DeepSeek R1 :free)** | **100% Free** | **The QA Debugger** | Analyzes pytest failure tracebacks and returns surgical code fixes. |
| **Devin / Autonomous Script** | **Included** | **The General Contractor** | Orchestrates the self-healing test loop and manages CI/CD commits. |
| **GitHub** | **100% Free** | **Central Hub** | Remote git repository, release tags, and pull requests. |

---

## Workspace Layout

```text
autonomous-workspace/
├── .vscode/
│   └── settings.json           # Auto-formatting & pytest configuration
├── config/
│   ├── mcp_servers.json        # MCP filesystem server configuration
│   ├── node_modules/           # @modelcontextprotocol/server-filesystem
│   └── package.json
├── logs/                       # Test failure logs & debugger diagnostics
├── scripts/
│   ├── ai_bridge.py            # Zero-cost smart routing for Groq, Gemini, OpenRouter, and Ollama
│   ├── autonomous_orchestrator.py # Full autonomous pipeline runner
│   ├── deepseek_debugger.py    # OpenRouter / Groq / Ollama traceback debugger
│   ├── claude_reviewer.py      # Google Gemini staff code reviewer
│   └── self_heal_runner.py     # Pytest execution & self-healing loop
├── specs/
│   ├── MASTER_SPEC_TEMPLATE.md # Blueprint template for new projects
│   └── MASTER_SPEC.md          # Active project specification
├── src/                        # Production application code
├── tests/                      # Pytest unit & integration test suites
├── .env                        # Active free API keys
├── .env.example                # Clean environment template
└── .gitignore
```

---

## Running the Pipeline

```bash
cd ~/autonomous-workspace
python3 scripts/autonomous_orchestrator.py
```
