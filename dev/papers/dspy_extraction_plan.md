# 🧠 DSPy Extraction Plan — AI Earth LEGO Pieces
# ══════════════════════════════════════════════════════════════════════
# Paper: DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines
# Conference: ICLR 2024 (Notable)
# Stars: 28K ⭐ (stanfordnlp/dspy)
# Source: https://github.com/stanfordnlp/dspy
# Domain: Planning & Reasoning (#6 in Research Coverage Map)
# ══════════════════════════════════════════════════════════════════════

---

## 📊 Stats

```
Source files:          260 Python files
Source lines:          62,794 lines
LEGO pieces target:    50-60 files
Extraction sessions:   8 sessions
```

---

## 🎯 What DSPy Adds to AI Earth

DSPy is fundamentally different from EvoAgentX:
- EvoAgentX = workflow engine + optimizers
- DSPy = **declarative compilation framework** + reasoning strategies + teleprompters

### Unique LEGO Pieces:
1. **Signature System** — declarative I/O specs (new concept!)
2. **Module Composition** — compilable, parameterized modules
3. **Reasoning Strategies** — CoT, ReAct, PoT, Refine, BestOfN, CodeAct
4. **Adapters** — Chat, JSON, XML, TwoStep format handling
5. **Teleprompters** — BootstrapFewShot, MIPROv2, COPRO, GRPO, SimBA, BetterTogether
6. **LM Client** — unified client with caching + provider abstraction
7. **Evaluation** — systematic evaluation framework
8. **Proposer** — grounded instruction proposal

---

## 📋 Session Plan

### Session D1: Core + Primitives (Foundation) 🏗️
**Priority: CRITICAL — everything depends on this**

| File | Lines | Description |
|------|-------|-------------|
| `utils/constants.py` | 10 | Constants (IS_TYPE_UNDEFINED) |
| `utils/exceptions.py` | 205 | Exception hierarchy |
| `utils/magicattr.py` | 103 | Magic attribute access |
| `utils/saving.py` | 54 | Serialization utilities |
| `utils/annotation.py` | 70 | Decorators (experimental) |
| `utils/logging_utils.py` | 53 | Logging configuration |
| `dsp/utils/settings.py` | 323 | Global settings |
| `primitives/sandbox_serializable.py` | 124 | Sandbox serialization |
| `primitives/example.py` | 352 | Example dataclass |
| `primitives/prediction.py` | 155 | Prediction container |
| `primitives/base_module.py` | 332 | BaseModule with params |
| `primitives/module.py` | 353 | Module (compose + forward) |

**Total: ~2,084 lines**

### Session D2: Core Types + Signatures 📝
**Priority: HIGH — DSPy's unique contribution**

| File | Lines | Description |
|------|-------|-------------|
| `core/types.py` | 2,035 | Type system (LM types, messages) |
| `signatures/field.py` | 113 | InputField, OutputField |
| `signatures/signature.py` | 836 | Signature metaclass |
| `signatures/utils.py` | 10 | Signature utilities |

**Total: ~2,994 lines**

### Session D3: Predictors (Reasoning Strategies) 🧠
**Priority: HIGH — core reasoning capabilities**

| File | Lines | Description |
|------|-------|-------------|
| `predict/predict.py` | 420 | Base Predict |
| `predict/chain_of_thought.py` | 40 | Chain-of-Thought |
| `predict/react.py` | 281 | ReAct agent |
| `predict/react_v2.py` | 250 | ReAct v2 |
| `predict/program_of_thought.py` | 187 | Program-of-Thought |
| `predict/refine.py` | 245 | Refine |
| `predict/best_of_n.py` | 84 | BestOfN |
| `predict/code_act.py` | 136 | CodeAct |
| `predict/parallel.py` | 130 | Parallel execution |
| `predict/multi_chain_comparison.py` | 47 | MultiChainComparison |
| `predict/knn.py` | 49 | KNN predictor |
| `predict/retry.py` | 75 | Retry wrapper |
| `predict/aggregation.py` | 45 | Majority voting |
| `predict/parameter.py` | 1 | Parameter placeholder |

**Total: ~1,990 lines**

### Session D4: Adapters 🔌
**Priority: HIGH — format handling layer**

| File | Lines | Description |
|------|-------|-------------|
| `adapters/base.py` | 773 | Base adapter |
| `adapters/chat_adapter.py` | 323 | Chat format |
| `adapters/json_adapter.py` | 337 | JSON format |
| `adapters/xml_adapter.py` | 116 | XML format |
| `adapters/two_step_adapter.py` | 231 | TwoStep adapter |
| `adapters/baml_adapter.py` | 264 | BAML adapter |
| `adapters/utils.py` | 283 | Adapter utilities |
| `adapters/_legacy_type_markers.py` | 154 | Legacy types |
| `adapters/types/tool.py` | 559 | Tool type |
| `adapters/types/*.py` | ~200 | Other types |

**Total: ~3,240 lines**

### Session D5: Teleprompters (Optimizers) ⚡
**Priority: HIGH — optimization layer**

| File | Lines | Description |
|------|-------|-------------|
| `teleprompt/teleprompt.py` | 23 | Base Teleprompter |
| `teleprompt/vanilla.py` | 24 | LabeledFewShot |
| `teleprompt/ensemble.py` | 34 | Ensemble |
| `teleprompt/bootstrap.py` | 303 | BootstrapFewShot |
| `teleprompt/mipro_optimizer_v2.py` | 866 | MIPROv2 |
| `teleprompt/copro_optimizer.py` | 355 | COPRO |
| `teleprompt/bettertogether.py` | 631 | BetterTogether |
| `teleprompt/grpo.py` | 635 | GRPO |
| `teleprompt/simba.py` | 377 | SIMBA |
| `teleprompt/random_search.py` | 174 | RandomSearch |
| `teleprompt/utils.py` | 464 | Teleprompt utils |
| `teleprompt/simba_utils.py` | 271 | SIMBA utils |
| `teleprompt/bootstrap_trace.py` | 136 | Bootstrap trace |
| `teleprompt/bootstrap_finetune.py` | 334 | Bootstrap finetune |
| `teleprompt/knn_fewshot.py` | 68 | KNN FewShot |
| `teleprompt/infer_rules.py` | 137 | InferRules |
| `teleprompt/signature_opt.py` | 66 | Signature optimizer |
| `teleprompt/teleprompt_optuna.py` | 89 | Optuna wrapper |
| `teleprompt/avatar_optimizer.py` | 219 | Avatar optimizer |
| `teleprompt/gepa/` | ~952 | GEPA optimizer |

**Total: ~6,012 lines**

### Session D6: Clients (LM Layer) 🔗
**Priority: MEDIUM — LM abstraction**

| File | Lines | Description |
|------|-------|-------------|
| `clients/base_lm.py` | 905 | BaseLM interface |
| `clients/lm.py` | 832 | LM implementation |
| `clients/openai_format.py` | 943 | OpenAI format |
| `clients/cache.py` | 301 | Response cache |
| `clients/provider.py` | 264 | Provider abstraction |
| `clients/__init__.py` | 101 | Client exports |
| `clients/_litellm.py` | 43 | LiteLLM wrapper |
| `clients/embedding.py` | 195 | Embedding client |
| `clients/lm_local.py` | 436 | Local LM |
| `clients/databricks.py` | 356 | Databricks client |
| `clients/openai.py` | 213 | OpenAI client |
| `clients/utils_finetune.py` | 137 | Finetune utils |
| `clients/disk_serialization.py` | 74 | Disk serialization |

**Total: ~4,900 lines**

### Session D7: Evaluate + Datasets 📊
**Priority: MEDIUM — evaluation framework**

| File | Lines | Description |
|------|-------|-------------|
| `evaluate/evaluate.py` | 399 | Evaluator |
| `evaluate/metrics.py` | 348 | Metrics |
| `evaluate/auto_evaluation.py` | 140 | Auto evaluation |
| `datasets/dataset.py` | 115 | Dataset base |
| `datasets/dataloader.py` | 183 | DataLoader |
| `datasets/colors.py` | 89 | Colors dataset |
| `datasets/gsm8k.py` | 60 | GSM8K dataset |
| `datasets/hotpotqa.py` | 83 | HotPotQA dataset |
| `datasets/math.py` | 47 | MATH dataset |

**Total: ~1,664 lines**

### Session D8: Utils + Streaming + Propose 🔧
**Priority: MEDIUM — utilities**

| File | Lines | Description |
|------|-------|-------------|
| `utils/callback.py` | 392 | Callback system |
| `utils/parallelizer.py` | 246 | Parallel executor |
| `utils/asyncify.py` | 52 | Async helpers |
| `utils/syncify.py` | 50 | Sync helpers |
| `utils/hasher.py` | 53 | Hashing utils |
| `utils/inspect_history.py` | 131 | History inspection |
| `utils/lazy_import.py` | 165 | Lazy imports |
| `utils/caching.py` | 10 | Cache helpers |
| `utils/unbatchify.py` | 90 | Unbatchify |
| `utils/usage_tracker.py` | 67 | Usage tracking |
| `utils/dummies.py` | 193 | Dummy utilities |
| `utils/langchain_tool.py` | 37 | LangChain tool |
| `utils/mcp.py` | 38 | MCP integration |
| `streaming/streaming_listener.py` | 415 | Streaming |
| `propose/grounded_proposer.py` | 417 | Grounded proposer |
| `propose/dataset_summary_generator.py` | 126 | Dataset summary |
| `propose/propose_base.py` | 6 | Base proposer |
| `propose/utils.py` | 182 | Propose utils |
| `retrievers/retrieve.py` | 51 | Retrieve base |
| `retrievers/embeddings.py` | 234 | Embedding retriever |

**Total: ~3,005 lines**

---

## 📦 External Dependencies (Stubs Needed)

```
litellm      — heavy, multi-provider LLM client
openai       — OpenAI API client
diskcache    — disk-based caching
json_repair  — JSON repair utility
tenacity     — retry logic
cachetools   — caching tools
gepa         — GEPA optimizer
httpx        — HTTP client
anyio        — async I/O
regex        — advanced regex
```

---

## 🗓️ Timeline

```
Session D1: Core + Primitives     → Foundation (everything depends on this)
Session D2: Types + Signatures    → DSPy's unique contribution
Session D3: Predictors            → Reasoning strategies
Session D4: Adapters              → Format handling
Session D5: Teleprompters         → Optimizers
Session D6: Clients               → LM abstraction
Session D7: Evaluate + Datasets   → Evaluation
Session D8: Utils + Streaming     → Utilities
```

**Target: 50-60 LEGO pieces, ~26,000 lines extracted verbatim**
