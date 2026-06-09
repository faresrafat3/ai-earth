# 🗺️ خريطة المكونات — GENESIS → AI Earth Migration Map
# ══════════════════════════════════════════════════════════════════════
# النسخة: 1.0
# التاريخ: 2026-06-09
# الغرض: خريطة تفصيلية لكل مكون — من أين أتى وإلى أين يذهب
# ══════════════════════════════════════════════════════════════════════

---

## 0. كيف تقرأ هذه الخريطة

```
لكل مكون:
  ORIGIN: من أين أتى في GENESIS
  DESTINATION: أين يذهب في AI Earth
  SOURCE_PAPERS: الأوراق البحثية المرتبطة
  DEPENDS_ON: ماذا يحتاج ليعمل
  FEEDS_INTO: من يعتمد عليه
  MIGRATION_STRATEGY: كيف ننقله (wrap/refactor/rewrite)
```

---

## 1. Layer 1: Infrastructure (البنية التحتية)

### 1.1 Environment Config
```yaml
ORIGIN: .env.example + hardcoded values in orchestrator.py
DESTINATION: ai_earth/core/env_config.py
MIGRATION_STRATEGY: EXTRACT + CENTRALIZE
  - كل env var في مكان واحد
  - profiles: dev/staging/production
  - validation at boot
DEPENDS_ON: nothing (foundation)
FEEDS_INTO: everything
```

### 1.2 API Key Pool
```yaml
ORIGIN: tools/api_key_pool.py
DESTINATION: ai_earth/core/api_pool.py
MIGRATION_STRATEGY: MOVE (as-is with header docs)
DEPENDS_ON: env_config
FEEDS_INTO: router, llm_call tool, research_agent
```

### 1.3 Model Registry
```yaml
ORIGIN: tools/model_registry.py
DESTINATION: ai_earth/core/model_registry.py
MIGRATION_STRATEGY: MOVE + EXTEND
  - أضف: capability tags (planner/worker/critic)
  - أضف: cost tracking per model
  - أضف: fallback chains
DEPENDS_ON: env_config
FEEDS_INTO: router, prompt_compiler, cost_optimizer
```

### 1.4 Schema Registry
```yaml
ORIGIN: planned (AGENT_DEVELOPMENT_CONTEXT.md §6)
DESTINATION: ai_earth/schemas/
MIGRATION_STRATEGY: CREATE NEW
  - tool_spec.v1.json
  - skill.v1.json
  - agent_spec.v1.json
  - meta_result.v1.json
  - telemetry_event.v1.json
DEPENDS_ON: nothing
FEEDS_INTO: all engines (validation)
```

### 1.5 Decision Log
```yaml
ORIGIN: AGENT_DEVELOPMENT_CONTEXT.md §9 (6 decisions)
DESTINATION: ai_earth/core/decision_log.py
MIGRATION_STRATEGY: EXTRACT + AUTOMATE
  - كل قرار جديد يُسجَّل تلقائياً
  - timestamp + context + impact + who decided
DEPENDS_ON: nothing
FEEDS_INTO: telemetry, insight
```

### 1.6 Boot Sequence
```yaml
ORIGIN: orchestrator.py main() (first ~100 lines)
DESTINATION: ai_earth/core/boot.py
MIGRATION_STRATEGY: EXTRACT + STRUCTURE
  - Dependency injection container
  - Service lifecycle management
  - Health checks at startup
DEPENDS_ON: env_config, api_pool, model_registry, schema_registry
FEEDS_INTO: pipeline
```

### 1.7 Kernel (Immutable Invariants)
```yaml
ORIGIN: NEW (inspired by Garrus800-stack/genesis-agent)
DESTINATION: ai_earth/core/kernel.py
MIGRATION_STRATEGY: CREATE NEW
  - 11 Preservation Invariants
  - Hash-locked scanner + verifier
  - Immutable safety constants
DEPENDS_ON: nothing
FEEDS_INTO: safety_engine, all operations
```

---

## 2. Layer 2: Capability Engines (محركات القدرات)

### 2.1 Tool Hub
```yaml
ORIGIN: genesis/tools/web_search.py (existing)
DESTINATION: ai_earth/capabilities/tool_hub/
SOURCE_PAPERS:
  - MCP Specification (Anthropic/Linux Foundation 2026)
  - MUSE-Autoskill (arXiv:2605.27366): sandbox lifecycle
DEPENDS_ON: api_pool, schema_registry
FEEDS_INTO: orchestrator (catalog injection), agents (tool use)
MIGRATION_STRATEGY: WRAP + EXTEND
  - web_search.py stays, wrapped by tool_hub/tools/web_search.py
  - new: code_exec.py, file_ops.py, llm_call.py, skill_use.py
  - ToolSpec schema for each tool
  - SandboxExecutor for safe execution
FILES:
  - registry.py: ToolSpec + ToolRegistry
  - executor.py: SandboxExecutor (tmpdir subprocess)
  - catalog.py: catalog() for prompt injection
  - tools/: individual tool wrappers
TESTS: 35+
```

### 2.2 Skill Engine
```yaml
ORIGIN: genesis/skill_engine/ (skeleton exists in Phase 2 commit)
DESTINATION: ai_earth/capabilities/skill_engine/
SOURCE_PAPERS:
  PRIMARY: MUSE-Autoskill (arXiv:2605.27366) — 5-stage lifecycle, SKILL.md
  SECONDARY: EvoSkill (arXiv:2603.02766) — 3-agent architecture, frontier
  TERTIARY: SkillOps (arXiv:2605.13716) — HSEG, hybrid retrieval
  QUATERNARY: SoK: Agentic Skills (arXiv:2602.20867) — taxonomy
DEPENDS_ON: tool_hub (SandboxExecutor), api_pool (LLM calls)
FEEDS_INTO: orchestrator (catalog + extraction + evolution), feedback
MIGRATION_STRATEGY: COMPLETE (skeleton exists, needs filling)
FILES:
  - skill.py: Skill + SkillContract(P,O,A,V,F)
  - library.py: SkillLibrary CRUD + frontier
  - evaluator.py: SkillEvaluator (sandbox pytest)
  - extractor.py: SkillExtractor + FailureCollector
  - graph.py: SkillGraph HSEG (dep/comp/red/alt edges)
  - retriever.py: BM25 + semantic hybrid
  - evolver.py: EvoSkillLoop + Proposer + Builder
  - skills/: filesystem skill packages
TESTS: 60+
```

### 2.3 Meta Engine
```yaml
ORIGIN: planned (AGENT_DEVELOPMENT_CONTEXT.md §4.2)
DESTINATION: ai_earth/capabilities/meta_engine/
SOURCE_PAPERS:
  PRIMARY: TextGrad (Stanford, zou-group/textgrad) — PyTorch-style text optimization
  SECONDARY: metaTextGrad (arXiv:2505.18524) — meta-level optimization
  TERTIARY: ExpeL — cross-episode insights
  QUATERNARY: OPTO — execution trace analysis
DEPENDS_ON: skill_engine (retrieve), critic_engine (scores)
FEEDS_INTO: orchestrator (Section 5a.5 NEW), feedback
MIGRATION_STRATEGY: CREATE NEW
FILES:
  - textgrad.py: TextVariable + TextLoss + TGD
  - trajectory.py: GenerationTrajectory
  - proposer.py: ProposerAgent
  - optimizer.py: MetaOptimizer (entry point)
TESTS: 40+
```

### 2.4 Concept Engine
```yaml
ORIGIN: multiple files (cognitive_bridge.py + GENESIS_Anomaly_*.md + GENESIS_Cognitive_*.md)
DESTINATION: ai_earth/capabilities/concept_engine/
SOURCE_PAPERS:
  - GENESIS own theories (Theory-07/08/09, Phil-07)
  - Anomaly Crisis Paradigm (F.'s theory)
  - Cognitive Economy (F.'s theory)
DEPENDS_ON: critic_engine (signals), evolution_engine (regime data)
FEEDS_INTO: meta_engine, feedback, insight
MIGRATION_STRATEGY: EXTRACT + FORMALIZE
  - intent.py ← goal_specification.py (already built)
  - anomaly.py ← from regime_transition_detector
  - crisis.py ← from GENESIS_Anomaly_Crisis_Paradigm_Theory
  - concept_formation.py ← from GENESIS_Cognitive_*.md
  - leverage.py ← from GENESIS_Anomaly_Leverage_Implementation
FILES:
  - intent.py: Intent Engine (from goal_specification.py)
  - anomaly.py: Anomaly Detection
  - crisis.py: Crisis Paradigm Handler
  - concept_formation.py: New abstractions from patterns
  - leverage.py: Leverage point detection
TESTS: 31+ (intent already tested)
```

---

## 3. Layer 3: Agent System (نظام الوكلاء)

### 3.1 Agent Hub
```yaml
ORIGIN: planned (AGENT_DEVELOPMENT_CONTEXT.md §4.2)
DESTINATION: ai_earth/agents/hub/
SOURCE_PAPERS:
  PRIMARY: OpenClaw SOUL.md (industry standard 2026)
  SECONDARY: BDI Architecture (arXiv:2512.09458)
  TERTIARY: MAGMA (arXiv:2601.03236) — best memory 2026
  QUATERNARY: MemGPT/Letta (arXiv:2310.08560)
DEPENDS_ON: concept_engine (intent), capability_engines (tools/skills)
FEEDS_INTO: workflow (orchestrator), memory
MIGRATION_STRATEGY: CREATE NEW
FILES:
  - agent.py: AgentSpec (Soul + Memory + Tools + Skills + BDI)
  - registry.py: AgentRegistry (CRUD + search)
  - soul/: AgentSoul + soul.md files
  - shared_agents.md: shared rules
TESTS: 50+
```

### 3.2 Agent Memory
```yaml
ORIGIN: context_manager.py + research_memory.py + new 4-tier design
DESTINATION: ai_earth/agents/memory/
SOURCE_PAPERS:
  - MAGMA (arXiv:2601.03236): 4 subgraphs
  - MemGPT (arXiv:2310.08560): LLM-as-OS paging
DEPENDS_ON: skill_engine (procedural bridge)
FEEDS_INTO: agent_hub (memory management), knowledge_graph
MIGRATION_STRATEGY: EXTRACT + EXTEND
  - context_manager.py → working.py
  - research_memory.py → episodic.py + semantic.py
  - NEW: procedural.py → bridge to skill_engine
FILES:
  - manager.py: AgentMemoryManager
  - working.py: Working Memory
  - episodic.py: Episodic Memory
  - semantic.py: Semantic Memory
  - procedural.py: Procedural Memory → Skill Bridge
TESTS: 30+
```

### 3.3 Agent Swarm
```yaml
ORIGIN: implicit in orchestrator.py (meta_agent + target_agent + feedback_agent)
DESTINATION: ai_earth/agents/swarm/
SOURCE_PAPERS:
  - Agentic AI Survey (arXiv:2512.09458): multi-agent patterns
  - Supervisor + specialists pattern
DEPENDS_ON: agent_hub, llm_interface, communication
FEEDS_INTO: workflow pipeline
MIGRATION_STRATEGY: EXTRACT + FORMALIZE
  - orchestrator_agent.py ← orchestrator.py logic
  - research_agent.py ← web_search + papers
  - coding_agent.py ← target_agent.py pattern
  - critic_agent.py ← open_task_evaluator + constitutional
  - meta_agent.py ← meta_engine interaction
FILES:
  - orchestrator_agent.py
  - research_agent.py
  - coding_agent.py
  - critic_agent.py
  - meta_agent.py
  - specialist/ (domain-specific, spawnable)
TESTS: 20+ (integration heavy)
```

### 3.4 LLM Interface (For LLM)
```yaml
ORIGIN: util.py (make_openai_client, run_agent) + hardcoded in orchestrator
DESTINATION: ai_earth/agents/llm_interface/
SOURCE_PAPERS:
  - API_GENESIS_Design_Arabic.md (existing design)
DEPENDS_ON: api_pool, model_registry, env_config
FEEDS_INTO: all agents (LLM access)
MIGRATION_STRATEGY: EXTRACT + ENHANCE
  - router.py ← from hardcoded model selection
  - prompt_compiler.py ← from META_AGENT_PROMPT assembly
  - candidate_search.py ← NEW (N candidates → critique → rank)
  - cost_optimizer.py ← NEW (token-aware routing)
FILES:
  - router.py: Model Router (planner/worker/critic/fallback)
  - prompt_compiler.py: Dynamic Prompt Assembly
  - candidate_search.py: N candidates → critique → rank
  - cost_optimizer.py: Token-aware routing
TESTS: 25+
```

### 3.5 Communication
```yaml
ORIGIN: NEW (inspired by Garrus800 EventBus + PeerNetwork)
DESTINATION: ai_earth/agents/communication/
MIGRATION_STRATEGY: CREATE NEW
FILES:
  - event_bus.py: Pub/sub between agents
  - peer_network.py: Inter-instance communication
  - mcp_protocol.py: Tool discovery protocol
TESTS: 15+
```

---

## 4. Layer 4: Workflow Engine (محرك سير العمل)

### 4.1 Pipeline (Main)
```yaml
ORIGIN: genesis/orchestrator.py (1915 lines)
DESTINATION: ai_earth/workflow/pipeline/
MIGRATION_STRATEGY: DECOMPOSE (break 1915 lines into sections)
  - s0_boot.py: boot sequence
  - s1_goal.py: goal specification (Section 0)
  - s2_memory.py: memory loading (Section 2)
  - s3_prompts.py: prompt assembly (Section 3)
  - s4_generation.py: generation loop (Section 4)
  - s5a_evaluation.py: evaluation stages (Section 5a)
  - s5b_feedback.py: feedback generation (Section 5b)
  - s6_output.py: output formatting (Section 6)
  - orchestrator.py: thin orchestrator calling sections
DEPENDS_ON: ALL layers
FEEDS_INTO: ALL layers (artifacts)
TESTS: existing 937 must still pass
```

### 4.2 Critic System
```yaml
ORIGIN:
  - open_task_evaluator.py → workflow/critic/open_evaluator.py
  - constitutional_evaluator.py → workflow/critic/constitutional.py
  - enhanced_pipeline_bridge.py → workflow/critic/enhanced_bridge.py
  - spin_feedback.py → workflow/critic/feedback.py
MIGRATION_STRATEGY: MOVE + CLEAN
DEPENDS_ON: llm_interface, evidence_log
FEEDS_INTO: feedback section, skill extraction, regime detection
TESTS: 67+ (existing)
```

### 4.3 Driven Engine
```yaml
ORIGIN: NEW (inspired by WingedGuardian/GENesis-AGI idle-time behavior)
DESTINATION: ai_earth/workflow/driven.py
MIGRATION_STRATEGY: CREATE NEW
  - Proactive task suggestion
  - Idle-time research & self-audit
  - Background optimization
  - "The system you come back to on Monday is sharper than the one you left on Friday"
TESTS: 15+
```

### 4.4 Loops
```yaml
ORIGIN: implicit in orchestrator + planned
DESTINATION: ai_earth/workflow/loops/
MIGRATION_STRATEGY: EXTRACT + CREATE
  - generation_loop.py ← orchestrator main loop
  - awareness_loop.py ← NEW (5-min tick, zero LLM cost)
  - reflection_loop.py ← NEW (Micro/Light/Deep/Strategic)
  - learning_loop.py ← NEW (dopaminergic feedback)
  - meta_loop.py ← meta_engine integration
TESTS: 20+
```

### 4.5 Integrations
```yaml
ORIGIN: scattered (Serper in web_search, OpenRouter in util.py)
DESTINATION: ai_earth/workflow/integrations/
MIGRATION_STRATEGY: EXTRACT + CENTRALIZE
FILES:
  - openrouter.py: OpenRouter API wrapper
  - mcp_servers.py: 4 MCP servers (memory/recon/health/outreach)
  - search_apis.py: Serper + Jina Reader
  - external.py: future external services
TESTS: 10+
```

---

## 5. Layer 5: Safety & Telemetry

### 5.1 Safety Engine
```yaml
ORIGIN: constitutional_evaluator.py (partial) + planned
DESTINATION: ai_earth/safety/
SOURCE_PAPERS: arXiv:2512.09458 (Safety Supervisor concept)
FILES:
  - budget.py: BudgetGuard
  - hallucination.py: HallucinationGuard
  - escalation.py: EscalationPolicy (warn → pause → halt)
TESTS: 25+
```

### 5.2 Telemetry
```yaml
ORIGIN: NEW
DESTINATION: ai_earth/safety/telemetry.py
FILES:
  - telemetry.py: RunTelemetry + TelemetryEvent
  - reporter.py: run_summary.json
TESTS: 20+
```

### 5.3 Regression Harness
```yaml
ORIGIN: existing 937 tests + tasks/gpqa_subset_20
DESTINATION: ai_earth/safety/regression.py
FILES:
  - regression.py: golden tasks + benchmark suite
TESTS: uses existing test suite
```

---

## 6. Layer 6: Memory & Knowledge

### 6.1 Papers Engine
```yaml
ORIGIN: PAPER/ directory + 122 MD files
DESTINATION: ai_earth/memory/papers_engine.py + dev/papers/
MIGRATION_STRATEGY: EXTRACT + ORGANIZE
  - كل ورقة لها ملف في dev/papers/
  - index في papers_index.json
  - Knowledge Graph edges: DERIVED_FROM
TESTS: 10+
```

### 6.2 Knowledge Graph
```yaml
ORIGIN: NEW
DESTINATION: ai_earth/memory/knowledge_graph.py
MIGRATION_STRATEGY: CREATE NEW
  - Node types: Concept, Paper, Skill, Tool, Agent, Pattern, Anomaly
  - Edge types: REFERENCES, CONTRADICTS, SUPERSEDES, ELABORATES, etc.
  - Intent-guided retrieval
  - Dual-stream consolidation: episodic → semantic
TESTS: 20+
```

---

## 7. Layer 7: Insight & Evolution

### 7.1 Task Evolution
```yaml
ORIGIN: NEW
DESTINATION: ai_earth/insight/task_evolution.py
TRACKS: complexity_score, scope_breadth, domain_diversity, success_rate
TESTS: 10+
```

### 7.2 Output Evolution
```yaml
ORIGIN: NEW
DESTINATION: ai_earth/insight/output_evolution.py
TRACKS: score_trajectory, hallucination_trajectory, convergence_speed
TESTS: 10+
```

### 7.3 System Evolution
```yaml
ORIGIN: NEW
DESTINATION: ai_earth/insight/system_evolution.py
TRACKS: skill_count, regime_stability, meta_gradient, knowledge_nodes
TESTS: 10+
```

---

## 8. Legacy Compatibility Layer

### LEGACY_COMPAT/
```yaml
ORIGIN: NEW (safety net for migration)
DESTINATION: ai_earth/LEGACY_COMPAT/
MIGRATION_STRATEGY: CREATE + MAINTAIN until Phase 7
PURPOSE:
  - from genesis.tools.web_search import web_search → works
  - from genesis.goal_specification import run_goal_specification → works
  - All old import paths continue to function
  - In Phase 7: evaluate removal (if all consumers updated)
FILES:
  - __init__.py
  - imports.py: all old paths → new paths
TESTS: existing tests verify this works
```

---

## 9. ملخص الأرقام

```
TOTAL FILES TO CREATE:     ~80 new Python files
TOTAL TESTS TO ADD:        ~260 new tests (937 → ~1200)
TOTAL PHASES:              7 phases
TOTAL WEEKS (estimated):   10 weeks
TOTAL LAYERS:              7 layers
TOTAL COMPONENTS:          25+ major components
TOTAL SOURCE PAPERS:       19+ research papers

MIGRATION STRATEGIES:
  MOVE (as-is):       4 components (api_pool, model_registry, etc.)
  WRAP + EXTEND:      3 components (web_search → tool_hub, etc.)
  EXTRACT + REFACTOR: 8 components (from orchestrator.py)
  CREATE NEW:         10+ components (agent_hub, swarm, driven, etc.)
  COMPLETE:           2 components (skill_engine, concept_engine)
```

---

_هذه الخريطة هي المرجع لكل عملية نقل مكون من GENESIS إلى AI Earth._
