# Session Log — 2026-06-10 (B): Real LLM Execution Engine

## Context
Session started from a FRESH sandbox (previous turn hung mid-pytest → snapshot
lost). Recovery took ~4 minutes following the golden rules:
`git clone` → recreate `.env` → `pip install -r requirements.txt` →
3 chunked test runs → all 486 green. Recovery protocol WORKS.

## Reminder — the user cannot kill a stuck process
Every bash command MUST carry `timeout -k 5 N`. Never run the full suite in
one command. This session: zero hangs, longest single command 75s (llm suite).

## What was done this session
- **v2.5.0** ⚡ Real LLM Execution Engine (`ai_earth/executor.py` rewritten):
  - `_ask_llm()` — budgeted per-run calls (`llm_budget_per_run=6` default),
    lifetime `max_cost_usd` cap, never raises → structural fallback
  - **LangGraph**: real 2-node graph — `plan` node (LLM drafts plan) →
    `process` node (LLM executes it); content flows through StateGraph state
  - **CrewAI**: sequential crew researcher→analyst→writer; each agent is a
    real LLM call with role prompt receiving the previous agent's real output
  - **AutoGen**: round-robin — assistant answers, critic reviews/improves
    (real 2-turn exchange, `conversation` in output)
  - **DSPy**: `Signature("task -> result")` drives structured prompt; LLM
    completion fills the output field
  - **Hybrid**: langgraph+dspy+crewai share ONE `_RunBudget` — can never
    exceed the cap regardless of piece count
  - `llm=False` → structural mode (zero calls, outputs labeled `[structural]`)
  - `ExecResult` gained `llm_calls` + `llm_cost_usd`
  - `run(..., llm=bool)` per-run override
- **API**: new `POST /execute` endpoint (task, strategy, llm, budget≤12)
- **Tests**: 25 structural executor tests → `llm=False`; benchmark.py engine
  → `llm=False`; +5 e2e `@pytest.mark.llm` (real plan/handoffs/roundrobin/
  signature/budget-guard); +3 API endpoint tests

## Test counts (all green)
- Fast structural: 177 passed (0 API calls, 37s)
- LEGO suite:      298 passed (26s)
- LLM integration:  19 passed (75s, ~$0.002)
- TOTAL:           494

## Live proof (crewai strategy, $0.0006/run)
Task: "Suggest a name for a self-evolving AI research platform"
- researcher[llm]: key facts about self-evolving AI platforms
- analyst[llm]: "name should be concise, memorable, abstract…"
- writer[llm]: "**Suggested Name: EvolvAI** …"
Chain is real — each agent received the previous agent's actual output.

## Next candidates
- Research Discovery live path: Serper + LLM summarize new papers end-to-end
- Memory: persist learnings across sessions via data/vault (survives resets)
- UI: wire /execute into Streamlit page with strategy picker
- Fix 51 xpassed lego tests — tighten xfail markers
- Benchmark: add live-LLM benchmark category (small budget, @llm marked)
