# 🔄 مخططات تدفق البيانات — Data Flow Diagrams
# ══════════════════════════════════════════════════════════════════════
# النسخة: 1.0
# التاريخ: 2026-06-09
# الغرض: كل تدفق بيانات في AI Earth مرسوم وموثق
# ══════════════════════════════════════════════════════════════════════

---

## 1. تدفق الطلب الرئيسي (Main Request Flow)

```
┌──────┐    task.md     ┌─────────────┐    AgentSpec    ┌──────────────┐
│ USER │──────────────▶│ Layer 1:    │───────────────▶│ Layer 3:     │
│ (F.) │               │ BOOT        │                │ AGENT HUB    │
└──────┘               │             │                │              │
                        │ env_config  │                │ soul         │
                        │ api_pool    │                │ memory_init  │
                        │ model_reg   │                │ tool_bind    │
                        │ schema_reg  │                │ skill_bind   │
                        │ kernel      │                │ bdi_init     │
                        └──────┬──────┘                └──────┬───────┘
                               │                              │
                               ▼                              │
                        ┌─────────────┐                      │
                        │ Layer 2:    │◀─────────────────────┘
                        │ CAPABILITIES│
                        │             │
                        │ intent      │──▶ goal_spec.json
                        │ tool_catalog│──▶ tool_catalog.yaml
                        │ skill_cat   │──▶ skill_catalog.yaml
                        │ meta_init   │──▶ trajectory.json
                        │             │
                        │ ASSEMBLE:   │
                        │ PROMPT =    │
                        │  soul       │
                        │  + tools    │
                        │  + skills   │
                        │  + goal     │
                        │  + memory   │
                        └──────┬──────┘
                               │
                    ╔══════════╧═══════════════════════════════╗
                    ║  GENERATION LOOP (Layer 4: Pipeline)     ║
                    ║                                          ║
                    ║  ┌──────────────────────────────────┐   ║
                    ║  │ Gen N:                            │   ║
                    ║  │                                    │   ║
                    ║  │  1. Safety Check                   │   ║
                    ║  │     budget_ok? halluc_ok?          │   ║
                    ║  │         │                           │   ║
                    ║  │         ▼                           │   ║
                    ║  │  2. Route Model                    │   ║
                    ║  │     planner/worker/critic?         │   ║
                    ║  │         │                           │   ║
                    ║  │         ▼                           │   ║
                    ║  │  3. Run Target Agent               │   ║
                    ║  │     LLM call + tool use            │   ║
                    ║  │     → target_agent.py artifacts    │   ║
                    ║  │         │                           │   ║
                    ║  │         ▼                           │   ║
                    ║  │  4. Evaluate                       │   ║
                    ║  │     ├─ open_task_eval              │   ║
                    ║  │     ├─ constitutional_eval         │   ║
                    ║  │     ├─ cognitive_signals           │   ║
                        │     └─ skill_extract (if > 70)     │   ║
                        │         │                           │   ║
                        │         ▼                           │   ║
                        │  5. Evolution Check                 │   ║
                        │     ├─ regime_detection             │   ║
                        │     ├─ evo_skill_loop               │   ║
                        │     └─ meta_optimizer               │   ║
                        │         │                           │   ║
                        │         ▼                           │   ║
                        │  6. Feedback                        │   ║
                        │     ├─ spin_section                 │   ║
                        │     ├─ regime_section               │   ║
                        │     ├─ enhanced_section             │   ║
                        │     ├─ meta_instruction             │   ║
                        │     ├─ skill_recommendations        │   ║
                        │     └─ bdi_belief_update            │   ║
                        │         │                           │   ║
                        │         ▼                           │   ║
                        │  7. Decision:                       │   ║
                        │     score_met? → END               │   ║
                        │     budget_out? → HALT             │   ║
                        │     else → Gen N+1                 │   ║
                        │                                      │   ║
                        └──────────────────────────────────────┘   ║
                                                                    ║
                        ╚════════════════╤═════════════════════════╝
                                       │
                        ┌───────────────▼───────────────────┐
                        │ Layer 5: SAFETY & AUDIT            │
                        │                                     │
                        │ telemetry events ──▶ event_log     │
                        │ budget report   ──▶ budget.json    │
                        │ halluc report   ──▶ halluc.json    │
                        │ regression test ──▶ test_results   │
                        └───────────────┬───────────────────┘
                                       │
                        ┌───────────────▼───────────────────┐
                        │ Layer 6: MEMORY INTEGRATION        │
                        │                                     │
                        │ working_mem    ◀── context         │
                        │ episodic_mem   ◀── run history     │
                        │ semantic_mem   ◀── facts learned   │
                        │ procedural_mem ◀── skills gained   │
                        │ knowledge_graph── new nodes/edges  │
                        │ experience_log ── run outcome      │
                        │ papers_engine  ── new research     │
                        └───────────────┬───────────────────┘
                                       │
                        ┌───────────────▼───────────────────┐
                        │ Layer 7: INSIGHT & EVOLUTION       │
                        │                                     │
                        │ task_evo    ── complexity tracking  │
                        │ output_evo  ── quality tracking    │
                        │ system_evo  ── capability tracking │
                        │ prediction  ── forecasting         │
                        │ driven      ── proactive suggestions│
                        └───────────────────────────────────┘
```

---

## 2. تدفق Tool Hub

```
Agent needs tool
       │
       ▼
┌─────────────────┐
│ catalog()       │───▶ YAML string ──▶ injected in PROMPT
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ get_tool(name)  │────▶│ ToolRegistry     │
└────────┬────────┘     │                  │
         │              │ tools = {        │
         │              │   "web_search":  │
         │              │     ToolSpec(…)  │
         │              │   "code_exec":   │
         │              │     ToolSpec(…)  │
         │              │ }                │
         │              └──────────────────┘
         │
         ▼
┌─────────────────┐
│ invoke(name,    │     ┌──────────────────┐
│         args)   │────▶│ SandboxExecutor  │
└────────┬────────┘     │                  │
         │              │ tmpdir + subprocess
         │              │ timeout + capture │
         │              └──────────────────┘
         │
         ▼
    ToolResult
    (output + errors + artifacts)
```

---

## 3. تدفق Skill Engine

```
Successful Gen (score > 70)
       │
       ▼
┌──────────────────┐
│ SkillExtractor   │──── reads target_agent.py
│                  │──── identifies reusable patterns
│                  │──── LLM generates skill code
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│ SkillEvaluator   │────▶│ SandboxExecutor  │
│                  │     │ runs pytest      │
│                  │     │ on skill code    │
│                  │◀──── results: pass/fail│
└────────┬─────────┘     └──────────────────┘
         │
    pass? │
    ┌─────┴─────┐
    │ NO        │ YES
    ▼           ▼
  Discard   ┌──────────────────┐
            │ SkillLibrary     │
            │ register(skill)  │
            │                  │
            │ Skill = {        │
            │   SKILL.md       │
            │   scripts/*.py   │
            │   tests/*.py     │
            │   .memory.md     │
            │ }                │
            └────────┬─────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   catalog()    retrieve()    evolve()
   for prompt   for feedback  on failure

EvoSkill Loop (on failure):
       │
       ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ FailureCollector │────▶│ ProposerAgent    │────▶│ SkillBuilder     │
│ gathers fails    │     │ analyzes why     │     │ materializes fix │
└──────────────────┘     │ proposes change  │     │ new skill version│
                         └──────────────────┘     └──────────────────┘
```

---

## 4. تدفق Meta Engine (TextGrad)

```
Gen 1 artifacts     Gen 2 artifacts    ...   Gen N artifacts
       │                   │                      │
       └───────────────────┴──────────────────────┘
                           │
                           ▼
               ┌──────────────────────┐
               │ GenerationTrajectory │
               │                      │
               │ points = [           │
               │   {gen:1, score:45}, │
               │   {gen:2, score:62}, │
               │   ...                │
               │   {gen:N, score:88}  │
               │ ]                    │
               └──────────┬───────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │ TextVariable         │
               │ value = agent_code   │
               │ requires_grad = True │
               └──────────┬───────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │ TextLoss             │
               │ loss = 100 - score   │
               │ description = "why"  │
               └──────────┬───────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │ TGD.backward()       │
               │ gradient = LLM says  │
               │ "what patterns led   │
               │  to improvement"     │
               └──────────┬───────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │ TGD.step()           │
               │ new instruction for  │
               │ Feedback Agent       │
               │ = meta_instruction   │
               └──────────────────────┘
```

---

## 5. تدفق الذاكرة (Memory Flow)

```
┌─────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM                      │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Tier 1: WORKING (context window)                │ │
│  │                                                   │ │
│  │ current_task + current_prompt + current_gen     │ │
│  │ SIZE: ~4K tokens                                 │ │
│  │ OVERFLOW → page to Tier 2                        │ │
│  └──────────────────────┬──────────────────────────┘ │
│                         │                             │
│                         │ session end / overflow      │
│                         ▼                             │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Tier 2: EPISODIC (run history)                  │ │
│  │                                                   │ │
│  │ {run:53, gen:1, score:45, task:"micro_task"}    │ │
│  │ {run:53, gen:2, score:62, task:"micro_task"}    │ │
│  │ SIZE: SQLite + JSON files                        │ │
│  │ SURPRISE-WEIGHTED: anomalies saved with weight   │ │
│  └──────────────────────┬──────────────────────────┘ │
│                         │                             │
│                         │ consolidation               │
│                         │ (pattern extraction)        │
│                         ▼                             │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Tier 3: SEMANTIC (knowledge graph)              │ │
│  │                                                   │ │
│  │ CONCEPTS ──REFERENCES──▶ PAPERS                  │ │
│  │   │                    │                         │ │
│  │   └──CONTRADICTS──▶ CONCEPT2                    │ │
│  │        │                                         │ │
│  │   ELABORATES──▶ DETAIL                          │ │
│  │                                                   │ │
│  │ SIZE: unlimited (atemporal facts)                │ │
│  └──────────────────────┬──────────────────────────┘ │
│                         │                             │
│                         │ skill extraction             │
│                         ▼                             │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Tier 4: PROCEDURAL (skill library)              │ │
│  │                                                   │ │
│  │ Skill: web_search_arabic (score: 85, used: 12)  │ │
│  │ Skill: evidence_tracking (score: 78, used: 5)   │ │
│  │ SIZE: filesystem (skills/)                       │ │
│  │ MAINTENANCE: merge, repair, retire, add_validator│ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

## 6. تدفق التطور (Evolution Flow)

```
┌─────────────────────────────────────────────────────────┐
│                    EVOLUTION SYSTEM                       │
│                                                           │
│  Run N completes                                         │
│       │                                                   │
│       ├──▶ Task Evolution Tracker                        │
│  │    │    complexity_score[run_N] = X                   │
│  │    │    scope_breadth[run_N] = "medium"               │
│  │    │    domain_diversity[run_N] = 3                   │
│  │    │                                                   │
│  │    ├──▶ Output Evolution Tracker                      │
│  │    │    score_trajectory = [45, 62, 71, 78, 85]       │
│  │    │    hallucination = [0.3, 0.2, 0.15, 0.1, 0.08]  │
│  │    │    convergence_gen = 3                            │
│  │    │                                                   │
│  │    ├──▶ System Evolution Tracker                      │
│  │    │    skill_count = 5 (+1 new)                      │
│  │    │    regime_stability = 7 runs                      │
│  │    │    meta_gradient = 0.12                           │
│  │    │    knowledge_nodes = 142                          │
│  │    │                                                   │
│  │    └──▶ Prediction Engine                             │
│  │         next_score = 87 ± 4                           │
│  │         regime_risk = LOW                             │
│  │         recommended_task = "harder"                   │
│  │                                                        │
│  └──▶ Evolution Report (dev/insights/evolution_reports/)  │
│                                                           │
│  Signals:                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ GRADUATION  │  │ PLATEAU     │  │ REGRESSION  │      │
│  │ ready for   │  │ need new    │  │ STOP and    │      │
│  │ harder task │  │ capabilities│  │ investigate │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

_هذه المخططات هي المرجع لفهم تدفق البيانات في AI Earth._
