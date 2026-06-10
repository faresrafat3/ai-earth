<p align="center">
  <h1 align="center">🌍 AI Earth</h1>
  <p align="center"><strong>The Living Intelligence Ecosystem</strong></p>
  <p align="center">
    <em>Self-evolving AI agent platform built from LEGO pieces extracted from research papers</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" />
  <img src="https://img.shields.io/badge/tests-554%20passing-brightgreen" />
  <img src="https://img.shields.io/badge/LEGO%20pieces-725%20files-orange" />
  <img src="https://img.shields.io/badge/lines-197%2C836-purple" />
  <img src="https://img.shields.io/badge/papers-7%20extracted-red" />
</p>

---

## 🌍 What is AI Earth?

AI Earth is a **self-evolving AI agent platform** built by extracting verbatim source code from 6 major open-source research frameworks (88K+ ⭐ combined) and composing them into a unified, composable system with a 7-phase self-evolution loop.

Every component is:
- 📄 **From papers** — extracted verbatim from peer-reviewed research
- 🧪 **Tested** — 460 tests all passing
- 🧱 **Composable** — 6 LEGO pieces that snap together via CrossPieceBridge
- 🧬 **Self-evolving** — 7-phase evolution loop with 6 strategies

---

## 🧱 LEGO Pieces (6 Research Papers)

| # | LEGO Piece | Source | ⭐ | Files | Lines | Tests | Components |
|---|---|---|---|---|---|---|---|
| 1 | **EvoAgentX** | arXiv:2507.03616 (EMNLP 2025) | — | 192 | 35,569 | 118 | Workflow Engine + 6 Optimizers + Agents + Memory |
| 2 | **DSPy** | Stanford NLP (ICLR 2024) | 28K | 148 | 31,774 | 98 | Signatures + 8 Predictors + 15 Teleprompters |
| 3 | **Mem0** | mem0ai/mem0 | 25K | 144 | 27,419 | 45 | Memory + 13 Embeddings + 25 Vector Stores + 19 LLMs |
| 4 | **Model Router** | AI Earth Platform | — | 2 | 1,240 | 47 | Unified LLM Interface (7 providers, caching, cost tracking) |
| 5 | **LangGraph** | langchain-ai/langgraph | 25K | 86 | 31,327 | 41 | Graph Engine + Channels + Pregel + Prebuilt Agents |
| 6 | **CrewAI** | crewAIInc/crewAI | 22K | 153 | 40,301 | 49 | Multi-Agent Crews + Flow + Memory + Knowledge + Tools |
| | **Total** | | **142K+** | **836** | **197,836** | **554** | |

---

## 🧬 Self-Evolving Agent Core

The platform's intelligence — a 7-phase evolution loop that uses all LEGO pieces:

```
Observe → Plan → Execute → Evaluate → Reflect → Evolve → Remember
   ↓         ↓        ↓         ↓         ↓        ↓        ↓
 Mem0    DSPy/LG   CrewAI    DSPy     Self      EvoAgentX   Mem0
 context  plan     agents   metrics  critique  optimizers  memory
```

### 6 Evolution Strategies:
1. **prompt_optimize** — DSPy MIPRO / EvoPrompt
2. **workflow_evolve** — EvoAgentX SEW / AFlow
3. **agent_refine** — CrewAI agent tuning
4. **memory_augment** — Mem0 context enrichment
5. **graph_restructure** — LangGraph topology optimization
6. **hybrid** — Combine multiple strategies

### Usage:
```python
from ai_earth.self_evolve import SelfEvolveCore

core = SelfEvolveCore(quality_threshold=0.8)
result = core.evolve(
    task="Build a research summary pipeline",
    max_iterations=5,
    strategy="hybrid",
)
print(f"Score: {result.final_metrics.overall_score()}")
```

---

## 🔗 Cross-Piece Bridge

The orchestrator composes all LEGO pieces:

```python
from ai_earth.orchestrator import AIEarth

earth = AIEarth()

# Create components from different LEGO pieces
earth.create_langgraph("research_graph")          # LangGraph
earth.create_crew("team", [                        # CrewAI
    {"name": "analyst", "role": "Analyst", "goal": "Analyze"},
    {"name": "writer", "role": "Writer", "goal": "Write"},
])
earth.create_memory("context")                     # Mem0

# Compose into a unified workflow
pipeline = earth.compose("research_pipeline",
    graph_name="research_graph",
    crew_agents=["analyst", "writer"],
    memory_store="context",
)
```

---

## 🏗️ Architecture — 7 Layers

```
┌─────────────────────────────────────────────────────────┐
│  🌍 AI EARTH — The Living Intelligence Ecosystem         │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  🧬 Self-Evolving Core (7-phase loop + 6 strategies)     │
│                                                           │
│  🔗 CrossPieceBridge                                      │
│  ├── Model Router → Unified LLM (7 providers)            │
│  ├── DSPy → Signatures, Predictors, Teleprompters        │
│  ├── LangGraph → Graph-based Agent Orchestration         │
│  ├── CrewAI → Multi-Agent Crew Orchestration             │
│  ├── Mem0 → Persistent Memory Layer                      │
│  └── EvoAgentX → Workflow Engine + 6 Optimizers          │
│                                                           │
│  🏛️ Platform Layer                                        │
│  ├── Orchestrator (workflow management)                   │
│  ├── Kernel (immutable invariants)                        │
│  ├── Decision Log (architectural decisions)               │
│  └── Safety Layer                                         │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/faresrafat3/ai-earth.git
cd ai-earth
pip install -r requirements.txt
pytest tests/ -v  # 460 tests passing
```

### Run the evolution loop:
```python
from ai_earth.self_evolve import SelfEvolveCore

core = SelfEvolveCore()
result = core.evolve("Analyze research papers about AI", max_iterations=3)
print(core.stats())
```

---

## 📁 Project Structure

```
ai-earth/
├── ai_earth/
│   ├── orchestrator.py        # Main platform orchestrator + CrossPieceBridge
│   ├── model_router.py        # Unified LLM interface (7 providers)
│   ├── self_evolve.py         # 🧬 Self-Evolving Agent Core
│   ├── core/                  # Kernel + Decision Log
│   ├── lego/
│   │   ├── evoagentx/         # EvoAgentX (192 files, 35,569 lines)
│   │   ├── dspy/              # DSPy (148 files, 31,774 lines)
│   │   ├── mem0/              # Mem0 (144 files, 27,419 lines)
│   │   ├── langgraph_src/     # LangGraph (86 files, 31,327 lines)
│   │   ├── crewai_src/        # CrewAI (153 files, 40,301 lines)
│   │   └── stubs/             # Lightweight stubs for missing deps
│   ├── agents/                # Agent hub + communication + swarm
│   ├── capabilities/          # Skill/concept/meta engines
│   ├── memory/                # Memory layer
│   ├── workflow/              # Workflow pipeline + loops + critic
│   ├── insight/               # Insight extraction
│   └── safety/                # Safety constraints
├── tests/
│   ├── lego/                  # LEGO piece tests (398 tests)
│   ├── test_self_evolve.py    # 🧬 Evolution core tests (43 tests)
│   ├── test_cross_piece.py    # 🔗 Cross-piece integration (19 tests)
│   ├── test_ai_earth_boot.py  # Platform boot tests
│   └── test_model_router.py   # Model Router tests
└── README.md
```

---

## 📊 Platform Stats

| Metric | Value |
|---|---|
| Papers Extracted | 7 |
| Total Files | 836 |
| Total Lines | 197,836 |
| Total Tests | 554 ✅ |
| Evolution Strategies | 6 |
| LLM Providers | 7 |
| Optimizers | 6 |
| Vector Stores | 25 |
| Embedding Providers | 13 |

---

## 🗺️ Roadmap

- [x] ~~Paper #1: EvoAgentX~~ (192 files, 35,569 lines, 118 tests)
- [x] ~~Paper #2: DSPy~~ (148 files, 31,774 lines, 98 tests)
- [x] ~~Paper #3: Mem0~~ (144 files, 27,419 lines, 45 tests)
- [x] ~~Paper #4: Model Router~~ (2 files, 1,240 lines, 47 tests)
- [x] ~~Paper #5: LangGraph~~ (86 files, 31,327 lines, 41 tests)
- [x] ~~Paper #6: CrewAI~~ (153 files, 40,301 lines, 49 tests)
- [x] ~~Paper #7: AutoGen~~ (111 files, 20,206 lines, 55 tests)
- [x] ~~Cross-Piece Bridge~~ (Orchestrator connects all pieces)
- [x] ~~Self-Evolving Agent Core~~ (7-phase evolution loop)
- [x] ~~Platform API~~ (FastAPI REST, 17 endpoints)
- [x] ~~Streamlit Web UI~~ (4 pages, interactive)
- [ ] Paper #8: Semantic Kernel / OpenAI Agents SDK
- [ ] Real LLM integration (OpenAI/Anthropic/Gemini)
- [ ] Production deployment

---

## 📝 License

Research and educational use. Each LEGO piece retains its original license.

---

Built with 🧬 by [Fares Rafat](https://github.com/faresrafat3) — extracting intelligence from papers, one LEGO piece at a time.
