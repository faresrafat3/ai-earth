# Session Log — 2026-06-10: Anti-Hang Hardening + Real LLM Self-Evolution

## Context
Previous session HUNG for 30+ minutes running the full test suite (592 tests
with unbounded real LLM calls). The workspace snapshot was lost because the
turn never completed. Everything pushed to GitHub survived; the un-pushed
self-evolve real-LLM work was lost and has been REBUILT this session (better).

## Golden Rules (learned the hard way)
1. **NEVER run the full test suite in one command.** Run in chunks:
   - `pytest tests/ --ignore=tests/lego -m "not llm" -q --timeout=90`  (~30s, ZERO API calls)
   - `pytest tests/lego/ -q --timeout=90`                              (~30s)
   - `pytest tests/ --ignore=tests/lego -m llm -q --timeout=180`       (~45s, ~25 real calls)
2. **Every bash command gets an explicit timeout** (`timeout -k 5 N cmd`).
3. **Every test is capped** via pytest.ini (`timeout = 90`, thread method).
4. **LLM calls are budgeted** everywhere:
   - `llm_pool`: max 4 attempts/call, 30s HTTP timeout, 200 calls/run budget
     (env: AI_EARTH_HTTP_TIMEOUT, AI_EARTH_MAX_ATTEMPTS, AI_EARTH_MAX_CALLS_PER_RUN)
   - `SelfEvolveCore`: `llm_budget_per_cycle=6`, `max_cost_usd` lifetime cap.
5. Environment resets between sessions: reinstall via
   `pip install -r requirements.txt` (~2 min) and recreate `.env`
   (keys live ONLY in .env — gitignored; ask user if lost).

## What was done this session
- **v2.3.2** 🛡️ Anti-hang: pytest.ini (per-test 90s cap), `pytest-timeout` dep,
  bounded key rotation (max 4 attempts, 2 keys/provider), configurable HTTP
  timeouts, LLM call budget guard, `@pytest.mark.llm` markers (fast suite = 0 calls),
  fixed missing `overdue` dep (evoagentx), fixed `WorkFlowNode.status` test bug
  (test asserted `.state`; real API is `.status` — test had never actually run).
- **v2.4.0** 🧬 Real LLM Self-Evolution (rebuilt lost work, improved):
  - `_observe`: LLM analyzes the task → `[llm]` observation
  - `_execute`: LLM ACTUALLY performs up to 3 sub-tasks (outputs tagged `source: llm`)
  - `_evaluate`: LLM-as-Judge 0-1 score blended 60/40 with heuristic floor;
    REAL token/cost numbers (removed simulated `iteration*1500` tokens)
  - `_reflect`: LLM proposes the next-iteration improvement → `[llm]` reflection
  - `_ask_llm()`: budgeted, never raises, graceful heuristic fallback
  - `llm=True` default (production). `llm=False` = deterministic offline mode
    for structural tests (NOT mock — nothing fakes AI output, labels say heuristic)
  - API `/evolve` accepts `"llm": bool` in request body
  - 4 new e2e tests in `TestRealLLMEvolution` (marked `llm`)

## Test counts (all green)
- Fast structural: 174 passed (0 API calls)
- LEGO suite:      298 passed
- LLM integration:  14 passed (~25 real calls, ~$0.001)
- TOTAL:           486

## Live proof (real output from evolution cycle, $0.0003/cycle)
Task: "Design a smart caching strategy for a multi-provider LLM router"
- LLM observation: "...hybrid caching strategy combining time-based expiration..."
- LLM-executed sub-task: "...multi-tier caching: Local LRU + per-provider cache..."
- LLM reflection: "Implement a dynamic cache eviction policy based on real-time
  usage patterns and response times..."
- Score 0.610 (judged by real LLM), 5 calls, $0.000302

## Key file map
- `ai_earth/llm_pool.py`      — key pool, 21 keys, anti-hang guards
- `ai_earth/self_evolve.py`   — 7-phase loop, now truly intelligent
- `ai_earth/model_router.py`  — unified chat() over the pool
- `pytest.ini`                — per-test 90s hard cap, `llm` marker
- `.env`                      — ALL keys (gitignored; recreate if env resets)

## Next candidates
- Wire real LLM into executor.py strategies (CrewAI/LangGraph/AutoGen paths)
- Research Discovery: use Serper + LLM to find & summarize new papers (capabilities/research_discovery.py exists)
- Memory: persist learnings across sessions via data/vault
- Fix xpassed tests (51 in lego) — tighten xfail markers
- Version bump ai_earth/__init__.py (still says 2.3.0)
