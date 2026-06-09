# 🌍 AI EARTH — المخطط المعماري الرئيسي
# ══════════════════════════════════════════════════════════════════════
# النسخة: 0.1 (الأساس المعماري)
# التاريخ: 2026-06-09
# المالك: Fares Rafat (F.)
# المعماري: Arena Agent (A.) — تصميم، AI Agent تنفيذ
# المرجع: faresrafat3/GENESIS → AI Earth Migration
# ══════════════════════════════════════════════════════════════════════

---

## 0. الفلسفة المؤسسة

```
"الثابت كله بيتغير"
"ذكي وهشيد"  — لا يوجد شيء نهائي، كل شيء قابل للتطور
"مفيش حاجة تعدي من غير ما تكون: مجربة، مفتوحة، مفصلة، من A لـ Z"
```

AI Earth ليس منتج — إنه **نظام بيئي حي** (Living Ecosystem):
- كل مكون قابل للاستبدال الساخن (Hot-Swappable)
- كل مكون له نسخة (Versioned)
- كل مكون قابل للتطور (Evolvable)
- لا توجد حالة "نهائية" — فقط حالة "حالية"

---

## 1. خريطة الطبقات السبع (The 7 Layers)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        🌍 AI EARTH                                   │
│                  The Living Intelligence Ecosystem                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Layer 7: INSIGHT & EVOLUTION                                       │
│  ├── Analytics Dashboard                                            │
│  ├── Task Evolution Tracker (Task Evo)                              │
│  ├── Output Evolution Tracker (Output Evo)                          │
│  ├── System Evolution Engine (All Evo)                              │
│  └── Prediction Curves & Forecasting                                │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Layer 6: MEMORY & KNOWLEDGE                                 │   │
│  │  ├── Papers Engine (مصدر أولاً — الأوراق العلمية)            │   │
│  │  ├── Dev Knowledge Store                                      │   │
│  │  ├── Memory Layer (4-tier: Working/Episodic/Semantic/Proc)   │   │
│  │  ├── Knowledge Graph (concepts + relations + contradictions) │   │
│  │  ├── Experience Log (runs, failures, successes)              │   │
│  │  └── Product Specs (feature definitions)                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Layer 5: SAFETY & TELEMETRY                                 │   │
│  │  ├── Budget Guard (per-agent, per-run, per-task)             │   │
│  │  ├── Hallucination Guard (evidence-anchored)                 │   │
│  │  ├── Escalation Policy (warn → pause → halt)                 │   │
│  │  ├── Telemetry Engine (event-by-event audit trail)            │   │
│  │  └── Regression Harness (golden tasks + benchmark suite)     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Layer 4: WORKFLOW ENGINE                                    │   │
│  │  ├── Pipeline (Main) — مسار التنفيذ الرئيسي                 │   │
│  │  │   ├── Pre-processing → Intent → Execution → Eval → Feedback│  │
│  │  ├── Driven Engine — القيادة الذكية                         │   │
│  │  │   ├── Proactive task suggestion                          │   │
│  │  │   ├── Idle-time research & self-audit                    │   │
│  │   │   └── Background optimization                           │   │
│  │  ├── Integrations Hub                                        │   │
│  │  │   ├── OpenRouter / LLM Providers                         │   │
│  │   │   ├── MCP Servers (4: memory/recon/health/outreach)      │   │
│  │   │   ├── Search APIs (Serper + Jina)                       │   │
│  │   │   └── External Services (future)                        │   │
│  │  └── Loops Engine                                            │   │
│  │      ├── Generation Loop (existing orchestrator)             │   │
│  │      ├── Awareness Loop (5-min tick, zero LLM cost)         │   │
│  │      ├── Reflection Loop (Micro/Light/Deep/Strategic)       │   │
│  │      ├── Self-Learning Loop (dopaminergic feedback)         │   │
│  │      └── Meta-Optimization Loop (TextGrad trajectory)       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Layer 3: AGENT SYSTEM                                       │   │
│  │  ├── Agent Hub (creation + soul + registry)                  │   │
│  │  │   ├── AgentSpec: Soul + Memory + Tools + Skills + BDI     │   │
│  │  │   ├── AgentRegistry: CRUD + search + REST-ready           │   │
│  │  │   └── Soul System: SOUL.md + AGENTS.md per agent         │   │
│  │  ├── Agent Swarm (multi-agent coordination)                  │   │
│  │  │   ├── Orchestrator Agent (supervisor)                     │   │
│  │  │   ├── Research Agent (papers + web search)                │   │
│  │  │   ├── Coding Agent (implementation)                       │   │
│  │  │   ├── Critic Agent (evaluation + judgment)                │   │
│  │  │   ├── Meta Agent (self-improvement)                       │   │
│  │  │   └── Specialist Agents (domain-specific, spawnable)     │   │
│  │  ├── For LLM — واجهة التفاعل مع النماذج                    │   │
│  │  │   ├── Model Router (planner/worker/critic/fallback)       │   │
│  │  │   ├── Prompt Compiler (dynamic assembly)                  │   │
│  │  │   ├── Candidate Search (N candidates → critique → rank)  │   │
│  │  │   └── Cost Optimizer (token-aware routing)                │   │
│  │  └── Communication Layer                                      │   │
│  │      ├── EventBus (pub/sub between agents)                    │   │
│  │      ├── Peer Network (inter-instance)                       │   │
│  │      └── MCP Protocol (tool discovery)                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Layer 2: CAPABILITY ENGINES                                 │   │
│  │  ├── Tool Hub (dynamic tool discovery + sandbox)              │   │
│  │  │   ├── ToolSpec schema (name/desc/io/preconditions)        │   │
│  │  │   ├── ToolRegistry (register/discover/catalog/invoke)     │   │
│  │  │   ├── SandboxExecutor (tmpdir subprocess)                  │   │
│  │  │   └── Tool Catalog YAML (injected in system prompts)     │   │
│  │  ├── Skill Engine (5-stage lifecycle)                        │   │
│  │  │   ├── Skill + SkillContract (P,O,A,V,F)                   │   │
│  │  │   ├── SkillLibrary (CRUD + frontier + maintenance)        │   │
│  │  │   ├── SkillEvaluator (sandbox pytest)                     │   │
│  │  │   ├── SkillExtractor (from successful agents)             │   │
│  │  │   ├── SkillGraph (HSEG: dep/comp/red/alt)                │   │
│  │  │   ├── SkillRetriever (BM25 + semantic hybrid)            │   │
│  │  │   └── EvoSkillLoop (Proposer + Builder agents)           │   │
│  │  ├── Meta Engine (TextGrad + trajectory analysis)            │   │
│  │  │   ├── TextVariable + TextLoss + TGD                       │   │
│  │  │   ├── GenerationTrajectory (full run history)             │   │
│  │  │   ├── ProposerAgent (meta-level suggestions)              │   │
│  │  │   └── MetaOptimizer (orchestrator entry point)            │   │
│  │  └── Concept Engine (cognitive concept formation)            │   │
│  │      ├── Anomaly Detection (deviation from expected)         │   │
│  │      ├── Crisis Paradigm (how system responds to anomalies)  │   │
│  │      ├── Concept Formation (new abstractions from patterns)  │   │
│  │      └── Leverage Points (where intervention is most impactful) │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Layer 1: INFRASTRUCTURE (AI Earth Core)                     │   │
│  │  ├── Environment Config (settings, profiles, environments)   │   │
│  │  ├── API Key Pool (rotation + fallback)                       │   │
│  │  ├── Model Registry (available models + capabilities)        │   │
│  │  ├── Schema Registry (artifact schemas v1.x)                 │   │
│  │  ├── Decision Log (DECISION-001..NNN)                         │   │
│  │  ├── Boot Sequence (dependency injection + service lifecycle) │   │
│  │  └── Kernel (immutable invariants)                            │   │
│  │      ├── SafeGuard (security scanner)                         │   │
│  │      ├── Preservation Invariants (11 rules)                   │   │
│  │      └── Hash-Locked Verifier                                 │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. خريطة التدفق الرئيسية (Master Data Flow)

```
USER INPUT (Task)
     │
     ▼
┌─────────────────────────────────────────┐
│ Layer 1: BOOT                           │
│ ├── Load Env Config                     │
│ ├── Init API Pool + Model Registry      │
│ ├── Load Kernel Invariants              │
│ └── Start Telemetry                     │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Layer 3: AGENT CREATION                 │
│ ├── AgentSpec.for_task(task_name)       │
│ ├── Load Soul → SOUL_SECTION            │
│ ├── Init Memory (4-tier)                │
│ └── Bind Tools + Skills                 │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Layer 2: CAPABILITY ASSEMBLY            │
│ ├── INTENT_ENGINE → GoalSpec            │
│ ├── TOOL_HUB → catalog()                │
│ ├── SKILL_ENGINE → catalog()            │
│ ├── META_ENGINE → trajectory init       │
│ └── Assemble META_AGENT_PROMPT          │
│     = SOUL + TOOLS + SKILLS + GOAL      │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Layer 4: WORKFLOW EXECUTION             │
│                                         │
│  ═══════ GENERATION LOOP ═══════        │
│  │                                      │
│  ├── Safety Check (budget + halluc)     │
│  │                                      │
│  ├── Run Target Agent (LLM call)        │
│  │   ├── Model Router selects model     │
│  │   ├── Prompt Compiler builds prompt  │
│  │   ├── Agent executes with tools      │
│  │   └── Produces artifacts             │
│  │                                      │
│  ├── Evaluation (CRITIC_ENGINE)         │
│  │   ├── Open task eval (evidence-based)│
│  │   ├── Constitutional eval (rules)    │
│  │   ├── Cognitive signals (enhanced)   │
│  │   └── Skill extraction (if success)  │
│  │                                      │
│  ├── Evolution Check                    │
│  │   ├── Regime Detection (3 signals)   │
│  │   ├── EvoSkill Loop (if needed)      │
│  │   └── Meta Optimization (TextGrad)   │
│  │                                      │
│  ├── Feedback Generation                │
│  │   ├── SPIN (semantic gap)            │
│  │   ├── Regime section                 │
│  │   ├── Enhanced cognitive section     │
│  │   ├── Meta instruction               │
│  │   ├── Skill recommendations          │
│  │   └── BDI belief update              │
│  │                                      │
│  └── Loop or Terminate                  │
│      ├── Score threshold met? → END     │
│      ├── Budget exhausted? → HALT       │
│      └── Continue → next gen            │
│                                         │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Layer 5: SAFETY & AUDIT                 │
│ ├── Telemetry Event Stream              │
│ ├── Budget Report                       │
│ ├── Hallucination Report                │
│ └── Regression Check                    │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Layer 6: MEMORY INTEGRATION             │
│ ├── Save to Working Memory (context)    │
│ ├── Extract Episodic (run history)      │
│ ├── Update Semantic (facts learned)     │
│ ├── Update Procedural (skills gained)   │
│ ├── Update Knowledge Graph              │
│ ├── Update Experience Log               │
│ └── Feed Papers Engine (new research)   │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Layer 7: INSIGHT & EVOLUTION            │
│ ├── Task Evo: how tasks evolved         │
│ ├── Output Evo: how quality improved    │
│ ├── All Evo: system-wide evolution      │
│ ├── Prediction curves                   │
│ ├── Gap analysis                        │
│ └── Proactive suggestions (Driven)      │
└─────────────────────────────────────────┘
```

---

## 3. من GENESIS إلى AI Earth — خريطة الهجرة الكاملة

### 3.1 المكونات الموجودة (ما نملكه الآن)

| # | المكون | الموقع في GENESIS | وجهته في AI Earth | الحالة |
|---|--------|-------------------|-------------------|--------|
| 1 | Orchestrator (1915 سطر) | `genesis/orchestrator.py` | Layer 4: Pipeline Main | ✅ مبني |
| 2 | Web Search Tool | `genesis/tools/web_search.py` | Layer 2: Tool Hub | ✅ مبني |
| 3 | Intent Engine | `genesis/goal_specification.py` | Layer 2: Capability | ✅ مبني |
| 4 | Critic Engine (Open) | `genesis/open_task_evaluator.py` | Layer 4: Eval Stage | ✅ مبني |
| 5 | Critic Engine (Rules) | `genesis/constitutional_evaluator.py` | Layer 5: Safety | ✅ مبني |
| 6 | Cognitive Bridge | `genesis/enhanced_pipeline_bridge.py` | Layer 2: Concept Engine | ✅ مبني |
| 7 | Evolution Engine | `genesis/orchestrator.py` (inline) + `virtual_genesis/` | Layer 2: Evolution | ✅ مبني |
| 8 | Feedback Engine | `genesis/spin_feedback.py` | Layer 4: Feedback Stage | ✅ مبني |
| 9 | Context Manager | `genesis/context_manager.py` | Layer 6: Memory | ✅ مبني |
| 10 | Research Memory | `genesis/research_memory.py` | Layer 6: Memory | ✅ مبني |
| 11 | API Key Pool | `tools/api_key_pool.py` | Layer 1: Infrastructure | ✅ مبني |
| 12 | Model Registry | `tools/model_registry.py` | Layer 1: Infrastructure | ✅ مبني |
| 13 | Virtual Genesis | `virtual_genesis/` | Layer 2: Concept Engine | ✅ مبني |
| 14 | 937 Test | `tests/` | Layer 5: Regression | ✅ مبني |
| 15 | Skill Engine (Phase 2 code) | `genesis/skill_engine/` | Layer 2: Skill Engine | 🔶 جزئي |
| 16 | Paper + Theory | `PAPER/` + 122 ملف MD | Layer 6: Papers | ✅ مبني |

### 3.2 المكونات المطلوب بناؤها (ما نحتاجه)

| # | المكون | الطبقة | المرحلة | الأولوية |
|---|--------|--------|---------|----------|
| 1 | Tool Hub | Layer 2 | Phase 1 | 🔴 عالية |
| 2 | Skill Engine (إكمال) | Layer 2 | Phase 2 | 🔴 عالية |
| 3 | Meta Engine | Layer 2 | Phase 3 | 🟡 متوسطة |
| 4 | Agent Hub | Layer 3 | Phase 4 | 🔴 عالية |
| 5 | Safety Engine | Layer 5 | Phase 5 | 🟡 متوسطة |
| 6 | Telemetry Engine | Layer 5 | Phase 5 | 🟡 متوسطة |
| 7 | Model Router | Layer 3 | Phase 1 | 🔴 عالية |
| 8 | Prompt Compiler | Layer 3 | Phase 2 | 🟡 متوسطة |
| 9 | Candidate Search | Layer 3 | Phase 3 | 🟡 متوسطة |
| 10 | Agent Swarm Orchestration | Layer 3 | Phase 4 | 🔴 عالية |
| 11 | Driven Engine | Layer 4 | Phase 5 | 🟢 منخفضة |
| 12 | Awareness Loop | Layer 4 | Phase 5 | 🟢 منخفضة |
| 13 | Reflection Loop | Layer 4 | Phase 5 | 🟢 منخفضة |
| 14 | Knowledge Graph | Layer 6 | Phase 4 | 🟡 متوسطة |
| 15 | Evolution Dashboard | Layer 7 | Phase 6 | 🟢 منخفضة |

---

## 4. بنية المجلدات المستهدفة (Target Directory Structure)

```
ai_earth/                              ← الحزمة الرئيسية (بديل genesis/)
│
├── core/                              ← Layer 1: Infrastructure
│   ├── __init__.py
│   ├── env_config.py                  ← Environment Config (profiles, settings)
│   ├── boot.py                        ← Boot Sequence (DI + service lifecycle)
│   ├── kernel.py                      ← Immutable invariants
│   ├── api_pool.py                    ← API Key Pool (from tools/api_key_pool.py)
│   ├── model_registry.py              ← Model Registry (from tools/model_registry.py)
│   ├── schema_registry.py             ← Artifact Schema Registry
│   └── decision_log.py                ← Decision Log (DECISION-NNN)
│
├── capabilities/                      ← Layer 2: Capability Engines
│   ├── __init__.py
│   │
│   ├── tool_hub/                      ← Tool Hub
│   │   ├── __init__.py
│   │   ├── registry.py                ← ToolSpec, ToolRegistry
│   │   ├── executor.py                ← SandboxExecutor
│   │   ├── catalog.py                 ← catalog() for prompt injection
│   │   └── tools/
│   │       ├── web_search.py          ← wraps genesis/tools/web_search.py
│   │       ├── code_exec.py           ← sandbox Python execution
│   │       ├── file_ops.py            ← safe file operations
│   │       ├── llm_call.py            ← wraps api_key_pool + util.py
│   │       └── skill_use.py           ← calls skill_engine.execute()
│   │
│   ├── skill_engine/                  ← Skill Engine
│   │   ├── __init__.py
│   │   ├── skill.py                   ← Skill, SkillContract(P,O,A,V,F)
│   │   ├── library.py                 ← SkillLibrary: CRUD + frontier
│   │   ├── evaluator.py              ← SkillEvaluator: sandbox pytest
│   │   ├── extractor.py              ← SkillExtractor + FailureCollector
│   │   ├── graph.py                   ← SkillGraph HSEG
│   │   ├── retriever.py              ← BM25 + semantic hybrid
│   │   ├── evolver.py                ← EvoSkillLoop + Proposer + Builder
│   │   └── skills/                    ← Skill packages (filesystem)
│   │       ├── catalog.yaml
│   │       ├── web_search_arabic/
│   │       └── evidence_tracking/
│   │
│   ├── meta_engine/                   ← Meta Engine
│   │   ├── __init__.py
│   │   ├── textgrad.py               ← TextVariable, TextLoss, TGD
│   │   ├── trajectory.py             ← GenerationTrajectory
│   │   ├── proposer.py               ← ProposerAgent
│   │   └── optimizer.py              ← MetaOptimizer (entry point)
│   │
│   └── concept_engine/               ← Concept Engine
│       ├── __init__.py
│       ├── intent.py                 ← Intent Engine (from goal_specification.py)
│       ├── anomaly.py                ← Anomaly Detection
│       ├── crisis.py                 ← Crisis Paradigm Handler
│       ├── concept_formation.py      ← New Abstractions from Patterns
│       └── leverage.py               ← Leverage Point Detection
│
├── agents/                            ← Layer 3: Agent System
│   ├── __init__.py
│   │
│   ├── hub/                           ← Agent Hub
│   │   ├── __init__.py
│   │   ├── agent.py                   ← AgentSpec (Soul+Memory+Tools+Skills+BDI)
│   │   ├── registry.py               ← AgentRegistry (CRUD + REST)
│   │   ├── soul/
│   │   │   ├── soul.py               ← AgentSoul dataclass
│   │   │   └── souls/                ← soul.md files per type
│   │   │       ├── research.soul.md
│   │   │       ├── coding.soul.md
│   │   │       ├── critic.soul.md
│   │   │       ├── meta.soul.md
│   │   │       └── default.soul.md
│   │   └── shared_agents.md           ← Shared rules (AGENTS.md)
│   │
│   ├── memory/                        ← Agent Memory (4-tier)
│   │   ├── __init__.py
│   │   ├── manager.py                ← AgentMemoryManager
│   │   ├── working.py                ← Working Memory (context window)
│   │   ├── episodic.py               ← Episodic Memory (timestamped)
│   │   ├── semantic.py               ← Semantic Memory (facts)
│   │   └── procedural.py            ← Procedural Memory → Skill Bridge
│   │
│   ├── swarm/                         ← Agent Swarm
│   │   ├── __init__.py
│   │   ├── orchestrator_agent.py     ← Supervisor
│   │   ├── research_agent.py         ← Papers + web search
│   │   ├── coding_agent.py           ← Implementation
│   │   ├── critic_agent.py           ← Evaluation + judgment
│   │   ├── meta_agent.py             ← Self-improvement
│   │   └── specialist/               ← Domain-specific agents
│   │
│   ├── llm_interface/                 ← For LLM
│   │   ├── __init__.py
│   │   ├── router.py                 ← Model Router (planner/worker/critic)
│   │   ├── prompt_compiler.py        ← Dynamic Prompt Assembly
│   │   ├── candidate_search.py       ← N candidates → critique → rank
│   │   └── cost_optimizer.py         ← Token-aware routing
│   │
│   └── communication/                ← Agent Communication
│       ├── __init__.py
│       ├── event_bus.py              ← Pub/sub between agents
│       ├── peer_network.py           ← Inter-instance
│       └── mcp_protocol.py           ← Tool discovery protocol
│
├── workflow/                           ← Layer 4: Workflow Engine
│   ├── __init__.py
│   ├── pipeline.py                   ← Main Pipeline (from orchestrator.py)
│   │   ├── sections/                 ← Pipeline Sections
│   │   │   ├── s0_boot.py
│   │   │   ├── s1_goal.py
│   │   │   ├── s2_memory.py
│   │   │   ├── s3_prompts.py
│   │   │   ├── s4_generation.py
│   │   │   ├── s5a_evaluation.py
│   │   │   ├── s5b_feedback.py
│   │   │   └── s6_output.py
│   │   └── orchestrator.py           ← Generation Loop Controller
│   │
│   ├── driven.py                     ← Driven Engine (proactive)
│   ├── loops.py                      ← All Loop Types
│   │   ├── generation_loop.py
│   │   ├── awareness_loop.py
│   │   ├── reflection_loop.py
│   │   ├── learning_loop.py
│   │   └── meta_loop.py
│   │
│   ├── integrations/                 ← Integrations Hub
│   │   ├── openrouter.py
│   │   ├── mcp_servers.py
│   │   ├── search_apis.py
│   │   └── external.py
│   │
│   └── critic/                       ← Critic System
│       ├── open_evaluator.py         ← (from open_task_evaluator.py)
│       ├── constitutional.py         ← (from constitutional_evaluator.py)
│       └── enhanced_bridge.py        ← (from enhanced_pipeline_bridge.py)
│
├── safety/                            ← Layer 5: Safety & Telemetry
│   ├── __init__.py
│   ├── budget.py                     ← BudgetGuard
│   ├── hallucination.py              ← HallucinationGuard
│   ├── escalation.py                 ← EscalationPolicy
│   ├── telemetry.py                  ← RunTelemetry + TelemetryEvent
│   └── regression.py                 ← Regression Harness
│
├── memory/                            ← Layer 6: Memory & Knowledge
│   ├── __init__.py
│   ├── papers_engine.py              ← Papers Management
│   ├── knowledge_store.py            ← Dev Knowledge Store
│   ├── knowledge_graph.py            ← Knowledge Graph
│   ├── experience_log.py             ← Runs, failures, successes
│   ├── context.py                    ← (from context_manager.py)
│   ├── research_memory.py            ← (from research_memory.py)
│   └── product_specs.py              ← Feature definitions
│
├── insight/                           ← Layer 7: Insight & Evolution
│   ├── __init__.py
│   ├── task_evolution.py             ← Task Evo Tracker
│   ├── output_evolution.py           ← Output Evo Tracker
│   ├── system_evolution.py           ← All Evo Engine
│   ├── prediction.py                 ← Prediction Curves
│   └── dashboard.py                  ← Analytics Dashboard
│
├── schemas/                           ← Schema Registry
│   ├── tool_spec.v1.json
│   ├── skill.v1.json
│   ├── agent_spec.v1.json
│   ├── meta_result.v1.json
│   └── telemetry_event.v1.json
│
└── LEGACY_COMPAT/                     ← Backward Compatibility
    ├── __init__.py
    └── imports.py                     ← All old import paths still work
        # from genesis.tools.web_search import web_search → works
        # from genesis.goal_specification import run_goal_specification → works

# ══════════════════════════════════════════
# OUTSIDE THE PACKAGE (Infrastructure)
# ══════════════════════════════════════════

dev/                                   ← This directory
├── architecture/                      ← Architecture docs (we create)
├── methodologies/                     ← Agent methodology files
├── papers/                            ← AI Agent fills this
├── memory/                            ← AI Agent fills this
├── insights/                          ← Evolution reports
└── product/                           ← Feature specs

PAPER/                                 ← Research paper (existing)
tests/                                 ← 937+ tests (existing, growing)
runs/                                  ← Run outputs (existing)
tasks/                                 ← Task definitions (existing)
.env.example                           ← Environment template
```

---

## 5. مراحل الهجرة (Migration Phases) — الجدول الزمني

### Phase 0: التأسيس (الأسبوع 0) — نحن هنا الآن
- [x] فهم المشروع الحالي بالكامل
- [x] تصميم المخطط المعماري (هذا الملف)
- [x] كتابة ملفات المنهجية
- [ ] مراجعة F. والموافقة على الخطة
- [ ] إنشاء فرع `ai_earth` من `main`

### Phase 1: Tool Hub + Model Router (الأسبوع 1)
- [ ] بناء `ai_earth/core/` (Layer 1)
- [ ] بناء `ai_earth/capabilities/tool_hub/`
- [ ] بناء `ai_earth/agents/llm_interface/router.py`
- [ ] بناء `ai_earth/LEGACY_COMPAT/`
- [ ] اختبارات: 35+ جديدة
- [ ] القاعدة: كل الـ 937 tests القديمة تمر

### Phase 2: Skill Engine (الأسابيع 2-4)
- [ ] إكمال `ai_earth/capabilities/skill_engine/`
- [ ] بناء SkillExtractor + SkillEvaluator
- [ ] بناء EvoSkillLoop
- [ ] أول skill حقيقي: `web_search_arabic/`
- [ ] اختبارات: 60+ جديدة

### Phase 3: Meta Engine (الأسبوع 5)
- [ ] بناء `ai_earth/capabilities/meta_engine/`
- [ ] TextGrad implementation
- [ ] GenerationTrajectory analysis
- [ ] اختبارات: 40+ جديدة

### Phase 4: Agent Hub + Swarm + Knowledge Graph (الأسابيع 6-7)
- [ ] بناء `ai_earth/agents/hub/` (Soul + Registry)
- [ ] بناء `ai_earth/agents/memory/` (4-tier)
- [ ] بناء `ai_earth/agents/swarm/`
- [ ] بناء `ai_earth/memory/knowledge_graph.py`
- [ ] اختبارات: 50+ جديدة

### Phase 5: Safety + Telemetry + Driven (الأسبوع 8)
- [ ] بناء `ai_earth/safety/`
- [ ] بناء `ai_earth/workflow/driven.py`
- [ ] بناء `ai_earth/workflow/loops/`
- [ ] اختبارات: 45+ جديدة

### Phase 6: Insight + Evolution Dashboard (الأسبوع 9)
- [ ] بناء `ai_earth/insight/`
- [ ] Task Evo + Output Evo + All Evo
- [ ] Prediction curves
- [ ] اختبارات: 30+ جديدة

### Phase 7: التكامل النهائي (الأسبوع 10)
- [ ] نقل orchestrator.py إلى pipeline sections
- [ ] إزالة LEGACY_COMPAT (كل شيء على البنية الجديدة)
- [ ] CI/CD pipeline
- [ ] Documentation كاملة
- [ ] إجمالي اختبارات: 1100+ (937 حالي + ~260 جديدة)

---

## 6. القواعد الذهبية (Golden Rules)

```
RULE G1: لا تكسر أي test موجود — أبداً
RULE G2: كل component جديد له اختبارات خاصة
RULE G3: كل ملف له header: Source + Stolen from + Usage + Integration
RULE G4: backward compatibility مقدسة — الـ imports القديمة تشتغل
RULE G5: الأوراق العلمية = المصدر الأول (مجربة + مفتوحة + كود متاح)
RULE G6: كل artifact له schema version (schema_registry.py)
RULE G7: كل قرار يُسجَّل في decision_log.py
RULE G8: كل component قابل للاستبدال الساخن (hot-swappable)
RULE G9: كل مكون له to_dict() + from_dict() (JSON-serializable)
RULE G10: المنهجية في dev/methodologies/ — الـ AI Agent يقرأها ويتبعها
```

---

## 7. محاور التطور الثلاثة (Evolution Axes)

```
                    ┌─────────────────────┐
                    │   TASK EVOLUTION     │
                    │   تطور المهام        │
                    │                     │
                    │  كيف تتغير طبيعة    │
                    │  المهام مع الوقت؟    │
                    │  من بسيط → مركب     │
                    │  من محدد → مفتوح    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ OUTPUT           │  │ SYSTEM           │  │ PREDICTION       │
│ EVOLUTION        │  │ EVOLUTION        │  │ CURVES           │
│ تطور المخرجات    │  │ التطور الشامل    │  │ منحنيات التنبؤ   │
│                  │  │                  │  │                  │
│ كيف يتحسن        │  │ كيف يتطور النظام │  │ أين سيكون النظام │
│ الجودة؟          │  │ ككل؟             │  │ بعد K runs؟      │
│ score over time  │  │ architecture     │  │ forecasting      │
│ hallucination ↓  │  │ changes over     │  │                  │
│ evidence ↑       │  │ time             │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

### مقاييس التطور (Evolution Metrics):

| المحور | المقياس | المصدر | الهدف |
|--------|---------|--------|-------|
| Task Evo | complexity_score(task) | INTENT_ENGINE | بيان اتجاه التعقيد |
| Task Evo | scope_coverage(task) | goal_spec.json | نطاق أكبر مع الوقت |
| Output Evo | overall_score(gen_N) | CRITIC_ENGINE | تحسن أحادي الاتجاه |
| Output Evo | hallucination_rate(gen_N) | evidence_log.json | تناقص |
| Output Evo | evidence_score(gen_N) | open_task_eval.json | تزايد |
| System Evo | skill_count(run_N) | SKILL_ENGINE | تزايد |
| System Evo | tool_usage_diversity(run_N) | TELEMETRY | تنوع أكبر |
| System Evo | meta_gradient_magnitude(gen_N) | META_ENGINE | تقل → استقرار |
| System Evo | regime_transitions(run_N) | regime_report.json | تناقص → نضج |

---

## 8. ورقة اللعبة (The Cheat Sheet) — للـ AI Agent

```yaml
# عندما يقول F.:
"ابدأ بالـ Tool Hub":
  → اقرأ: dev/methodologies/code_execution_rules.md
  → أنشئ: ai_earth/capabilities/tool_hub/
  → ارجع لـ: AGENT_DEVELOPMENT_CONTEXT.md §4.2 TOOL_HUB
  → اختبر: 35+ tests
  → commit: "feat: Tool Hub — Phase 1 complete, 35 tests"

"ابدأ بالـ Skill Engine":
  → اقرأ: dev/methodologies/code_execution_rules.md
  → أنشئ: ai_earth/capabilities/skill_engine/
  → ارجع لـ: AGENT_DEVELOPMENT_CONTEXT.md §4.2 SKILL_ENGINE
  → اختبر: 60+ tests
  → commit: "feat: Skill Engine — Phase 2 complete, 60 tests"

"ابحث عن ورقة":
  → اقرأ: dev/methodologies/scientific_research_rules.md
  → طبق الشروط الصارمة (مفتوحة + مجربة + كود + A-Z)
  → احفظ في: dev/papers/
  → أضف لـ: dev/memory/

"تتبع التطور":
  → اقرأ: dev/methodologies/evolution_tracking_protocol.md
  → أنشئ تقرير في: dev/insights/evolution_reports/
```

---

## 9. حالة المشروع الحالية (Snapshot)

```
Date: 2026-06-09
Source: faresrafat3/GENESIS (main branch)
Commits: 196
Branches: 14
Files: 232 Python
Tests: 937 passing
Runs: 53+ on GPQA
Papers/Theories: 122 MD files

Migration Status:
  Phase 0: ████████░░ 80% (architecture designed, awaiting approval)
  Phase 1: ░░░░░░░░░░  0%
  Phase 2: ██░░░░░░░░ 15% (skill_engine skeleton exists)
  Phase 3: ░░░░░░░░░░  0%
  Phase 4: ░░░░░░░░░░  0%
  Phase 5: ░░░░░░░░░░  0%
  Phase 6: ░░░░░░░░░░  0%
  Phase 7: ░░░░░░░░░░  0%
```

---

_هذا الملف هو المرجع المعماري الوحيد لأي AI Agent يعمل على AI Earth._
_يُحدَّث بعد كل phase — كل تغيير يُسجَّل في decision_log.py_
