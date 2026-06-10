<p align="center">
  <h1 align="center">🌍 AI Earth</h1>
  <p align="center"><strong>The Living Intelligence Ecosystem</strong></p>
  <p align="center">
    <em>Self-evolving AI agent platform built from LEGO pieces extracted from research papers</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" />
  <img src="https://img.shields.io/badge/tests-118%20passing-brightgreen" />
  <img src="https://img.shields.io/badge/LEGO%20pieces-192%20files-orange" />
  <img src="https://img.shields.io/badge/lines-37%2C519-purple" />
  <img src="https://img.shields.io/badge/source-EvoAgentX%20(arXiv%3A2507.03616)-red" />
</p>

---

## 🌍 What is AI Earth?

AI Earth is a **self-evolving AI agent platform** organized as LEGO pieces extracted verbatim from open-source research papers. Every component is:

- 📄 **From papers** — extracted verbatim from peer-reviewed research
- 🧪 **Tested** — 118 tests all passing
- 🧱 **Composable** — LEGO pieces that snap together
- 🧬 **Evolvable** — 6 built-in optimization methods

## 🏗️ Architecture — 7 Layers

```
┌─────────────────────────────────────────────────┐
│  🌍 AI EARTH — The Living Intelligence Ecosystem │
├─────────────────────────────────────────────────┤
│                                                   │
│  L7: 🧬 Optimizers                               │
│      SEW · AFlow · TextGrad · MIPRO              │
│      EvoPrompt · MapElites                        │
│                                                   │
│  L6: 📊 Evaluation                               │
│      Evaluator + 10 Benchmarks                   │
│                                                   │
│  L5: 🧠 Memory + RAG                             │
│      ShortTerm · LongTerm · Manager               │
│      RAG Pipeline (35 files)                      │
│                                                   │
│  L4: 🔄 Workflow Engine                          │
│      WorkFlowGraph · SequentialWorkFlow           │
│      Operators · Actions · Generator              │
│                                                   │
│  L3: 🤖 Agents + Actions                         │
│      Agent · Action · Toolkit                     │
│                                                   │
│  L2: 💬 Models + Prompts                         │
│      BaseLLM · PromptTemplate                     │
│                                                   │
│  L1: ⚙️ Core                                     │
│      BaseModule · Registry · Config               │
│                                                   │
└─────────────────────────────────────────────────┘
```

## 🚀 Quick Start

```python
from ai_earth.orchestrator import AIEarth

# Create the platform
earth = AIEarth()

# Build a workflow using fluent API
workflow = (
    earth.builder()
    .goal("Analyze customer feedback and generate insights")
    .task("parse", description="Parse raw feedback",
          inputs={"raw_text": "Raw feedback"},
          outputs={"structured": "Parsed data"},
          prompt="Parse: {raw_text}")
    .task("analyze", description="Sentiment analysis",
          inputs={"structured": "Parsed data"},
          outputs={"analysis": "Sentiment"},
          prompt="Analyze: {structured}")
    .task("report", description="Generate report",
          inputs={"analysis": "Sentiment"},
          outputs={"report": "Final report"},
          prompt="Report: {analysis}")
    .sequential()
    .build()
)

# Create graph from spec
graph = earth.create_workflow_from_spec(workflow)

# Track parameters for optimization
class Config:
    temperature = 0.7
    model = "gpt-4"

config = Config()
earth.track_parameter(config, "temperature")
earth.track_parameter(config, "model", name="llm")

# Save and manage
earth.save_workflow("feedback-analyzer", graph)
print(earth.stats())
```

## 🧬 6 Optimizers

| Optimizer | Lines | Source | What it does |
|-----------|-------|--------|-------------|
| **SEW** | 931 | Self-Evolving Workflow | Evolutionary workflow optimization (5 schemes) |
| **TextGrad** | 675 | TextGrad (Zou et al.) | Textual gradient backpropagation on prompts |
| **AFlow** | 302 | AFlow (MetaGPT) | Workflow topology evolution via LLM |
| **MIPRO** | 1,610 | DSPy (Stanford) | Multi-prompt instruction co-optimization |
| **EvoPrompt** | 1,127 | EvoPrompt | Genetic algorithm prompt optimization |
| **MapElites** | 175 | Quality-Diversity | Multi-dimensional quality diversity search |

## 📊 Stats

```
📁 Python files:      228
📝 Lines of code:     37,519
🧱 LEGO files:        192
🧪 Tests:             118 (ALL PASSING ✅)
🧬 Optimizers:        6 methods
📦 Git commits:       7
📄 Source paper:      EvoAgentX (arXiv:2507.03616, EMNLP 2025)
```

## 📁 Project Structure

```
ai-earth/
├── ai_earth/
│   ├── orchestrator.py              ← 🚀 The main platform
│   ├── __init__.py
│   └── lego/
│       └── evoagentx/               ← 🧱 All LEGO pieces
│           ├── core/                ← L1: BaseModule, Registry, Config
│           ├── models/              ← L2: BaseLLM, LLMOutputParser
│           ├── prompts/             ← L2: PromptTemplate
│           ├── agents/              ← L3: Agent, AgentManager
│           ├── actions/             ← L3: Action, ActionInput
│           ├── tools/               ← L3: Tool, Toolkit
│           ├── workflow/            ← L4: WorkFlowGraph, Operators
│           ├── memory/              ← L5: ShortTerm, LongTerm, Manager
│           ├── rag/                 ← L5: RAG Pipeline (35 files)
│           ├── evaluators/          ← L6: Evaluator
│           ├── benchmark/           ← L6: 10 Benchmarks
│           ├── optimizers/          ← L7: 6 Optimizers + Engine
│           │   └── engine/          ← ParamRegistry, BaseOptimizer
│           ├── storages/            ← Vector/Graph stores
│           └── utils/               ← Utilities + MIPRO utils
│               └── stubs/           ← Lightweight stubs for heavy deps
├── tests/
│   ├── conftest.py
│   ├── test_ai_earth_boot.py        ← 11 boot tests
│   └── lego/
│       ├── test_evoagentx_workflow.py  ← 31 workflow tests
│       └── test_evoagentx_optimizers.py ← 76 optimizer tests
├── dev/
│   ├── architecture/                ← Master blueprint + component maps
│   ├── methodologies/               ← 4 methodology documents
│   ├── papers/                      ← Extraction plans per paper
│   └── sessions/                    ← Session logs
├── schemas/                         ← Artifact schemas
└── requirements.txt
```

## 📄 Source Paper

**EvoAgentX: An Automated Framework for Evolving Agentic Workflows**
- arXiv: [2507.03616](https://arxiv.org/abs/2507.03616)
- Venue: EMNLP 2025 (Demo Track)
- GitHub: [EvoAgentX/EvoAgentX](https://github.com/EvoAgentX/EvoAgentX) (3.1K ⭐)
- Authors: Yingxu Wang, Siwei Liu, Jinyuan Fang, Zaiqao Meng
- Results: +7.44% HotPotQA, +10% MBPP, +10% MATH, +20% GAIA

## 🔮 Roadmap

- [x] Phase 0: Architecture + Methodologies
- [x] Phase 1: EvoAgentX Extraction (E3-E6 complete)
- [x] AI Earth Orchestrator
- [ ] Phase 2: Extract from DSPy (28K ⭐)
- [ ] Phase 3: Extract from Mem0 (48K ⭐)
- [ ] Phase 4: LLM Integration (Model Router)
- [ ] Phase 5: Evolution Dashboard

## 📜 License

LEGO pieces are extracted verbatim from EvoAgentX (MIT License).
AI Earth platform code is by Fares Rafat.

---

<p align="center">
  <strong>اللي يقدر يواكب ماشي 🚀</strong>
</p>
