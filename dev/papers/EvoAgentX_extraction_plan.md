# 📄 EvoAgentX — Paper Extraction Plan
# ══════════════════════════════════════════════════════════════════════
# الورقة: EvoAgentX: An Automated Framework for Evolving Agentic Workflows
# arXiv: 2507.03616 (EMNLP 2025 Demo)
# GitHub: EvoAgentX/EvoAgentX (3.1K stars, 1,105 commits)
# المؤلفون: Yingxu Wang, Siwei Liu, Jinyuan Fang, Zaiqiao Meng
# التقييم: 95/100 🟢 ممتازة — أولوية قصوى
# ══════════════════════════════════════════════════════════════════════

---

## البيانات الأساسية

```yaml
arXiv: 2507.03616
Venue: EMNLP 2025 (Demo Track)
GitHub: https://github.com/EvoAgentX/EvoAgentX
Stars: 3,100+
Commits: 1,105
License: MIT
Language: Python
Dependencies: OpenAI, Anthropic, LiteLLM, NetworkX, Pydantic
```

## الملخص (بالعربي)

EvoAgentX منصة مفتوحة المصدر لأتمتة توليد وتنفيذ وتحسين سير العمل
متعدد الوكلاء (multi-agent workflows) بشكل تطوري. تستخدم بنية من 5 طبقات:
مكونات أساسية → وكلاء → سير عمل → تحسين تطوري → تقييم.

النتائج: +7.44% HotPotQA, +10% MBPP, +10% MATH, +20% GAIA

## ليه مهمة لـ AI Earth

```
EvoAgentX = أقرب مشروع لرؤيتنا:
  ✅ Self-evolving workflows (التطور اللي عايزينه)
  ✅ 5-layer modular architecture (نفس فلسفة الـ 7 layers)
  ✅ 3 optimizers: TextGrad + AFlow + MIPRO (قطع LEGO جاهزة)
  ✅ Multi-agent by design
  ✅ Open source + well tested + documented
  ✅benchmarks حقيقية + أرقام
```

## النتائج الرئيسية

| Benchmark | Metric | Before | After | Improvement |
|-----------|--------|--------|-------|-------------|
| HotPotQA | F1 Score | baseline | +7.44% | ✅ |
| MBPP | pass@1 | baseline | +10.00% | ✅ |
| MATH | solve rate | 66% → 76% | +10.00% | ✅ |
| GAIA | overall accuracy | baseline | +20.00% | ✅ |

---

## 🔍 تحليل الكود — هل ينفكك لقطع؟

```
evoagentx/
├── actions/          ← ✂️ قطعة مستقلة (أفعال الوكلاء)
├── agents/           ← ✂️ قطعة مستقلة (تعريف الوكلاء)
├── app/              ← 🔒 Session كامل (واجهة الويب)
├── benchmark/        ← ✂️ قطعة مستقلة (التقييم)
├── core/             ← ✂️ قطع مستقلة (الأساس)
├── evaluators/       ← ✂️ قطعة مستقلة (التقييم)
├── frameworks/       ← ✂️ قطعة مستقلة (multi-agent debate)
├── hitl/             ← ✂️ قطعة مستقلة (human-in-the-loop)
├── memory/           ← ✂️ قطعة مستقلة (الذاكرة)
├── models/           ← ✂️ قطعة مستقلة (النماذج)
├── optimizers/       ← ✂️ قطع مستقلة (3 optimizers)
├── prompts/          ← ✂️ قطعة مستقلة (القوالب)
├── rag/              ← ✂️ قطعة مستقلة (البحث)
└── tools/            ← ✂️ قطعة مستقلة (الأدوات)

النتيجة: قابلة للتفكيك بشكل ممتاز ✂️
كل مجلد = قطعة LEGO مستقلة
```

---

## 📦 Sessions — خطة الاستخراج (10 Sessions)

### Session E1: Core Infrastructure ✂️
```yaml
المصدر: evoagentx/core/
القطع:
  - قطعة E1.1: Config Manager (YAML/JSON validation)
  - قطعة E1.2: Logging System (performance tracking)
  - قطعة E1.3: Storage Manager (persistence + caching)
  - قطعة E1.4: File Handler (workflow state management)
الوجهة في AI Earth: ai_earth/core/
المنهجية: انقل الكود حرفياً من evoagentx/core/
التقدير: ~200 سطر
```

### Session E2: Agent Definitions ✂️
```yaml
المصدر: evoagentx/agents/
القطع:
  - قطعة E2.1: Agent Base Class (LLM agent interface)
  - قطعة E2.2: Agent Config (model + tools + prompts)
  - قطعة E2.3: Agent Executor (run + stream + parse output)
الوجهة في AI Earth: ai_earth/agents/hub/
التقدير: ~300 سطر
```

### Session E3: Workflow Engine ✂️
```yaml
المصدر: evoagentx/actions/ + workflow logic in core/
القطع:
  - قطعة E3.1: DAG Workflow (custom nodes, edges, conditional branches)
  - قطعة E3.2: Linear Workflow (simple sequential)
  - قطعة E3.3: Workflow Executor (parallel execution patterns)
  - قطعة E3.4: Workflow Generator (auto-generate from task description)
الوجهة في AI Earth: ai_earth/workflow/pipeline/
التقدير: ~400 سطر
هذه القطعة أهم قطعة — سير العمل هو قلب النظام
```

### Session E4: Prompt Template System ✂️
```yaml
المصدر: evoagentx/prompts/
القطع:
  - قطعة E4.1: PromptTemplate (dynamic assembly)
  - قطعة E4.2: Input Descriptions + JSON Schema
  - قطعة E4.3: Tool-aware formatting
الوجهة في AI Earth: ai_earth/agents/llm_interface/prompt_compiler.py
التقدير: ~200 سطر
```

### Session E5: TextGrad Optimizer 🔒 (كامل)
```yaml
المصدر: evoagentx/optimizers/textgrad/
السبب 🔒: TextGrad مترابط — variable + loss + gradient + step
لازم ياخد كامل من غير تغيير
الوجهة في AI Earth: ai_earth/capabilities/meta_engine/
ملاحظة: النسخة دي مختلفة عن اللي في GENESIS — دي MAS-specific
التقدير: ~350 سطر
```

### Session E6: AFlow Optimizer ✂️
```yaml
المصدر: evoagentx/optimizers/aflow/
القطع:
  - قطعة E6.1: Workflow Topology Optimizer (graph mutation)
  - قطعة E6.2: Node-level optimization
  - قطعة E6.3: Ensemble approach (multiple candidates)
الوجهة في AI Earth: ai_earth/insight/system_evolution.py
التقدير: ~300 سطر
هذه القطعة فريدة — تحسين بنية سير العمل نفسه
```

### Session E7: MIPRO Optimizer ✂️
```yaml
المصدر: evoagentx/optimizers/mipro/ (inspired by DSPy)
القطع:
  - قطعة E7.1: Prompt + Tool co-optimization
  - قطعة E7.2: Mini-batch instruction proposal
الوجهة في AI Earth: ai_earth/capabilities/meta_engine/
التقدير: ~250 سطر
```

### Session E8: Evaluation Framework ✂️
```yaml
المصدر: evoagentx/evaluators/ + evoagentx/benchmark/
القطع:
  - قطعة E8.1: LLM-based Evaluator (generic)
  - قطعة E8.2: Benchmark Runner (HotPotQA, MBPP, MATH, GAIA)
  - قطعة E8.3: Metrics Calculator (F1, pass@1, solve rate)
الوجهة في AI Earth: ai_earth/workflow/critic/
التقدير: ~300 سطر
```

### Session E9: Tool System ✂️
```yaml
المصدر: evoagentx/tools/
القطع:
  - قطعة E9.1: Search Tools (Exa, Tavily, Serper)
  - قطعة E9.2: MCP Toolkit (Model Context Protocol)
  - قطعة E9.3: Crawler Toolkit
  - قطعة E9.4: Code Execution Tool
الوجهة في AI Earth: ai_earth/capabilities/tool_hub/tools/
التقدير: ~400 سطر
```

### Session E10: Memory + RAG ✂️
```yaml
المصدر: evoagentx/memory/ + evoagentx/rag/
القطع:
  - قطعة E10.1: Vector Store (embedding-based retrieval)
  - قطعة E10.2: RAG Pipeline (query → retrieve → augment)
  - قطعة E10.3: Memory Manager (cross-session)
الوجهة في AI Earth: ai_earth/memory/
التقدير: ~250 سطر
```

---

## 📊 ملخص الاستخراج

```
Sessions الإجمالية:       10
قطع LEGO الإجمالية:      28 قطعة
السطور المتوقعة:          ~2,950 سطر
من غير تغيير (🔒):        Session E5 فقط (TextGrad)
قابلة للتفكيك (✂️):       9 Sessions

الأولوية:
  Session E3 (Workflow Engine) — الأهم
  Session E6 (AFlow Optimizer) — الأفخم
  Session E2 (Agent Definitions) — الأساس
  Session E5 (TextGrad MAS) — الأعمق
  الباقي: مهم بس يتبع الأساس
```

---

## 🎮 بعد الاستخراج — إيه اللي هيبقى عندك

```
من EvoAgentX لوحدها هتحصل على:

  📦 Workflow Engine (DAG + Linear + Auto-gen)
  🤖 Agent Layer (base class + config + executor)
  📝 Prompt Templates (dynamic assembly)
  🧬 3 Optimizers (TextGrad + AFlow + MIPRO)
  📊 Evaluation Framework
  🛠️ Tool System (Search + MCP + Crawler + Code)
  🧠 Memory + RAG
  📐 Core Infrastructure

  = 28 قطعة LEGO قابلة للتركيب
  = تغطي Layer 2 + Layer 3 + Layer 4 + Layer 7 من AI Earth
```

---

## ⚠️ ما أخذناه

```yaml
- Web UI (app/) — مش محتاجينه دلوقتي
- Wonderful_workflow_corpus — بيانات تجريبية بس
- HITL (human-in-the-loop) — مهم بس Phase 5+
- Multi-agent debate framework — هنستخدمه لما نوصل Phase 4
```

---

## ما تركناه ولماذا

```yaml
- Web app: AI Earth هيستخدم واجهة مختلفة (vibe AI)
- HITL: مرحلة متقدمة — مش أساسية دلوقتي
- Workflow corpus: بيانات تجريبية — مش كود أساسي
- Debate framework: هيكون Session منفصل من ورقة تانية
```

---

_هذا الملف هو خطة الاستخراج الأولى — القالب لكل ورقة تالية._
_آخر تحديث: 2026-06-09_
