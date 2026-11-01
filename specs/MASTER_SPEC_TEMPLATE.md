# MASTER_SPEC_TEMPLATE.md
*Autonomous Multi-Agent Execution Specification*

---

## 1. Project Overview & Architecture
- **Project Name:** [INSERT PROJECT NAME]
- **Target Tech Stack:** Python 3.12 / Node.js 22 / PyTest / FastMCP
- **Directory Structure:**
```text
.
├── config/
│   └── mcp_servers.json
├── src/
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   └── api/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── scripts/
│   ├── ollama_worker.py
│   ├── deepseek_debugger.py
│   ├── claude_reviewer.py
│   └── self_heal_runner.py
└── specs/
    └── MASTER_SPEC.md
```

---

## 2. Phase 2 Prompts: ChatGPT (QA Product Manager)
Devin will prompt ChatGPT before generating production code:
> **Prompt for ChatGPT:**
> *"Act as the QA Product Manager for [PROJECT NAME]. Review the architecture and requirements defined in MASTER_SPEC.md. Generate a comprehensive suite of PyTest unit and integration tests covering standard execution, invalid inputs, edge cases, and failure recovery. Output complete test files to be placed in `tests/` before implementation begins."*

---

## 3. Phase 3: Numbered Micro-Tasks for Qwen 2.5:14b (Ollama)
Devin will script each micro-task (under 100 lines of code) via:
`python3 scripts/ollama_worker.py --prompt "<TASK_PROMPT>" --output "<TARGET_FILE>"`

1. **Micro-Task 1: Core Data Models**
   - Prompt: *"Implement Pydantic models for [Entity] in `src/models/[entity].py` with strict validation."*
2. **Micro-Task 2: Service Layer & Business Logic**
   - Prompt: *"Implement service functions in `src/services/[service].py` adhering to the interfaces required by `tests/`."*
3. **Micro-Task 3: Integration Adapters**
   - Prompt: *"Implement external connectors and data parsers in `src/api/[module].py`."*

---

## 4. Phase 4: Self-Healing & Debugging via DeepSeek
If `pytest` fails during development:
1. Devin captures the stdout/stderr stack trace.
2. Devin triggers the debugger harness:
   ```bash
   python3 scripts/deepseek_debugger.py -f logs/failure.log -c src/[failing_file].py
   ```
3. Devin applies the surgical fix returned by DeepSeek and re-runs `scripts/self_heal_runner.py`.

---

## 5. Phase 5: Audit & Delivery via Claude & GitHub
Once all tests in `tests/` pass cleanly:
1. Devin packages the git diff:
   ```bash
   python3 scripts/claude_reviewer.py -o specs/AUDIT_REQUEST.md
   ```
2. Devin applies Claude's security and architecture adjustments.
3. Devin commits and pushes to GitHub:
   ```bash
   git add .
   git commit -m "feat: complete autonomous build passing all test suites"
   git push origin main
   gh pr create --title "feat: autonomous release" --body "Automated build verified by self-healing test loop."
   ```
