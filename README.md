# Autonomous Super-Team Workspace

A zero-touch autonomous engineering pipeline orchestrated across Gemini, Devin, ChatGPT, Ollama (Qwen 2.5:14b), VS Code/Cursor, DeepSeek, Claude, and GitHub.

---

## Architecture & AI Roles

| Agent / Tool | Role | Function |
| :--- | :--- | :--- |
| **Gemini (Plus)** | The Architect | Designs overarching architecture, schemas, and `MASTER_SPEC.md` |
| **Devin** | General Contractor | Drives execution, routes tasks, triggers CLI tools, manages PRs |
| **ChatGPT** | Product Manager | Generates test suites and edge case coverage before code is written |
| **Ollama (Qwen 2.5:14b)** | Infinite Laborer | High-speed, local generation of models, boilerplate, and micro-tasks |
| **VS Code / Cursor** | Factory Floor | Headless MCP server hosting, file watching, and visual inspection |
| **DeepSeek** | QA Debugger | Surgical analysis and fixes for failing test tracebacks |
| **Claude** | Staff Reviewer | Pre-merge security, architecture, and code quality audit |
| **GitHub** | CI/CD Hub | Remote repository, branches, automated actions, and PR tracking |

---

## Workspace Structure

```text
autonomous-workspace/
├── .vscode/
│   └── settings.json           # VS Code pytest & auto-format config
├── config/
│   ├── mcp_servers.json        # MCP filesystem server config
│   ├── node_modules/           # @modelcontextprotocol/server-filesystem
│   └── package.json
├── logs/                       # Test failure logs & debugger output
├── scripts/
│   ├── ollama_worker.py        # CLI bridge to local Qwen 2.5:14b
│   ├── deepseek_debugger.py    # DeepSeek traceback analyzer
│   ├── claude_reviewer.py      # Git diff packager for Claude review
│   └── self_heal_runner.py     # Autonomous test & heal loop
├── specs/
│   └── MASTER_SPEC_TEMPLATE.md # Blueprint template for new projects
├── src/                        # Production application code
├── tests/                      # Pytest unit & integration test suites
├── .env.example                # API key template for DeepSeek / Claude
└── .gitignore
```

---

## Quick Verification Commands

From inside this folder with `.venv` activated:

1. **Test Local Ollama Worker:**
   ```bash
   python3 scripts/ollama_worker.py --prompt "Write a Python function that reverses a linked list."
   ```

2. **Run Autonomous Test & Heal Loop:**
   ```bash
   python3 scripts/self_heal_runner.py
   ```

3. **Generate Audit Diff for Claude:**
   ```bash
   python3 scripts/claude_reviewer.py
   ```

4. **Launch Visual Dashboard in Cursor:**
   ```bash
   cursor .
   ```
