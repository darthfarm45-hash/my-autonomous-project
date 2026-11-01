# MASTER_SPEC_TEMPLATE.md
*100% Zero-Cost Autonomous Multi-Agent Specification*

---

## 1. Project Overview & Architecture
- **Project Name:** [INSERT PROJECT NAME]
- **Target Tech Stack:** Python 3.12 / PyTest / Pydantic
- **Zero-Cost AI Roster:**
  - **Chief Architect & Staff Reviewer:** Google Gemini 1.5 Pro / Flash (Free Tier)
  - **QA Product Manager:** Groq Cloud Llama 3.3 70B (Free Tier)
  - **Infinite Laborer:** Local Ollama Qwen 2.5:14B on Apple Silicon M4 (100% Offline / $0)
  - **QA Debugger:** OpenRouter DeepSeek R1 `:free` (Free Tier)
  - **General Contractor:** Devin / Local Autonomous Orchestrator

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
│   ├── ai_bridge.py
│   ├── autonomous_orchestrator.py
│   ├── deepseek_debugger.py
│   ├── claude_reviewer.py
│   └── self_heal_runner.py
└── specs/
    └── MASTER_SPEC.md
```

---

## 2. Phase 2: QA Product Manager Prompts (Groq Llama 3.3 70B)
The orchestrator prompts Groq before coding begins:
> **Prompt for Groq (Product Manager):**
> *"Act as the Senior QA Product Manager for [PROJECT NAME]. Review the architecture in MASTER_SPEC.md. Generate a comprehensive suite of PyTest unit and integration tests covering standard execution, invalid inputs, edge cases, and failure recovery. Output complete test files to be placed in `tests/` before implementation begins."*

---

## 3. Phase 3: Numbered Micro-Tasks for Qwen 2.5:14b (Local Ollama)
The orchestrator scripts each micro-task (under 100 lines of code) via:
`python3 scripts/ollama_worker.py --prompt "<TASK_PROMPT>" --output "<TARGET_FILE>"`

1. **Micro-Task 1: Core Data Models**
   - Prompt: *"Implement Pydantic models for [Entity] in `src/models/[entity].py` with strict validation."*
2. **Micro-Task 2: Service Layer & Business Logic**
   - Prompt: *"Implement service functions in `src/services/[service].py` adhering to the interfaces required by `tests/`."*
3. **Micro-Task 3: Integration Adapters**
   - Prompt: *"Implement external connectors and data parsers in `src/api/[module].py`."*

---

## 4. Phase 4: Self-Healing & Debugging via OpenRouter (DeepSeek R1 Free)
If `pytest` fails during development:
1. The orchestrator captures the stdout/stderr traceback.
2. The orchestrator triggers the debugger harness:
   ```bash
   python3 scripts/deepseek_debugger.py -f logs/failure.log -c src/[failing_file].py
   ```
3. The debugger queries OpenRouter's free DeepSeek R1 model, logs the surgical fix, applies it, and re-runs `scripts/self_heal_runner.py`.

---

## 5. Phase 5: Staff Review & Audit via Google Gemini (Free Tier)
Once all tests in `tests/` pass cleanly:
1. The orchestrator packages the git diff:
   ```bash
   python3 scripts/claude_reviewer.py -o specs/AUDIT_REPORT.md
   ```
2. Google Gemini 1.5 Pro performs a staff-level security and architecture audit.
3. The build is committed to Git and pushed to GitHub:
   ```bash
   git add .
   git commit -m "feat: complete autonomous zero-cost build passing all test suites"
   git push origin main
   gh pr create --title "feat: autonomous release" --body "Automated build verified by self-healing test loop."
   ```
