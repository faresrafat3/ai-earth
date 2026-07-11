# Discovery Round 4 — AI Infrastructure / Compound AI Systems

## الهدف

استكشاف مجال البنية التحتية لأنظمة AI المركبة:

- orchestration
- observability
- tracing
- evaluation loops
- prompt/version management
- cost governance
- AI gateways
- compound systems

هذا المحور مهم لأنه قد ينتج فكرة أعم من كل candidates السابقة: طبقة تشغيل/مراقبة/تحكم فوق أنظمة AI المركبة.

---

# Online Round — مصادر واتجاهات

## 1. Compound AI Systems Survey

الرابط: https://arxiv.org/abs/2506.04565

Survey عن Compound AI Systems، يعرفها كنظم تدمج LLMs مع retrievers, tools, agents, orchestrators. يقدم taxonomy لمحاور:

- RAG
- agents
- multimodal
- orchestration

ويذكر تحديات:

- scalability
- interoperability
- benchmarking
- coordination

**الأثر:** المجال يتحول من model-centric إلى system-centric.

---

## 2. Databricks / BAIR framing of Compound AI Systems

الرابط: https://www.databricks.com/blog/what-are-compound-ai-systems

يوضح أن compound systems تحتاج:

- coordinating components
- error handling
- end-to-end evaluation
- monitoring/debugging

**الأثر:** النظام المركب يحتاج observability وtesting مثل distributed systems.

---

## 3. AI Observability and Agent Monitoring 2026

الرابط: https://zylos.ai/research/2026-01-16-ai-observability-agent-monitoring

يذكر أن AI observability أصبح enterprise requirement، مع tracing, evals, drift detection, agent replay.

**الأثر:** هناك سوق واضح للبنية التحتية حول مراقبة LLM/agents.

---

## 4. AI Agent Observability Tools 2026

الرابط: https://futureagi.com/blog/best-ai-agent-observability-tools-2026

يوضح الفرق بين LLM observability وagent observability:

- span tree
- planner
- retrievals
- tool calls
- sub-agent handoffs
- retries
- final response

**الأثر:** agent failures تختبئ في trace، لا في final answer فقط.

---

## 5. LLM Evaluation Tools with SDK Integrations

الرابط: https://www.braintrust.dev/articles/best-llm-evaluation-tools-integrations-2025

يقارن Braintrust, Langfuse, Phoenix, MLflow, Galileo وغيرها، مع دعم LangChain/LlamaIndex/DSPy/AutoGen.

**الأثر:** السوق مزدحم، لكن لا يزال هناك مساحة لتخصصات دقيقة.

---

## 6. AI Observability Tools 2026

الرابط: https://www.getmaxim.ai/articles/ai-observability-tools-in-2026-top-5-platforms-compared/

يركز على:

- prompt versioning
- tracing
- drift
- hallucination detection
- security scanners

**الأثر:** observability يتداخل مع eval, governance, security.

---

# Offline Audit

## ما الحقيقي؟

1. Compound AI systems أصبحت النمط السائد في التطبيقات القوية.
2. كلما زاد عدد المكونات، زاد خطر:
   - silent failures
   - cost explosion
   - context drift
   - tool errors
   - untraceable decisions
3. observability/evaluation أصبح market حقيقي.
4. OpenTelemetry/trace spans معيار مهم.
5. الأدوات العامة موجودة، لكن التخصصات الدقيقة ما زالت فرصة.

## ما الـ hype؟

1. “one platform for all AI observability” غالبًا مبالغ فيه.
2. LLM-as-judge لكل شيء خطر.
3. dashboards وحدها لا تحل reliability.
4. tracing بلا policy/action مجرد مراقبة سلبية.

---

# Candidate Theses

## Thesis A — Cheap Genius Runtime Layer

### المشكلة

Compound AI systems تستهلك موارد كثيرة وتفشل بصمت.

### الأطروحة

> طبقة runtime تسجل كل spans، تقيس cost/latency/quality، وتطبق سياسات stop/escalate/downgrade.

### MVP

SDK wrapper حول LLM calls:

- trace spans
- cost per route
- policy decisions
- retries/failures
- route comparison

### لماذا قوي؟

يجمع Resource Manager + Cost Governor + Routing.

---

## Thesis B — AI Workflow Flight Recorder

### المشكلة

عندما يفشل agent/compound pipeline، لا يعرف المطور أين حدث الخطأ.

### الأطروحة

> تسجيل trace قابل لإعادة التشغيل لكل خطوة: prompt, model, tool, retrieval, output, cost, latency.

### MVP

Local trace viewer + JSONL/SQLite.

### الفرق عن Langfuse/Phoenix

تركيز على cheap/self-hosted/experiment-first، لا enterprise dashboard.

### المخاطر

سوق observability مزدحم.

---

## Thesis C — Cost-to-Quality Profiler

### المشكلة

المطور لا يعرف أي route يعطي أفضل cost/quality لمهمته.

### الأطروحة

> أداة تشغل نفس task عبر routes مختلفة وتبني Pareto frontier: accuracy vs cost vs latency.

### MVP

Input: eval set + routes config.  
Output: Pareto chart + recommended route.

### لماذا قوي؟

يرتبط مباشرة بشرطنا: ذكاء ورخص.

---

## Thesis D — Compound AI Failure Taxonomy Engine

### المشكلة

فشل compound systems لا يظهر في final answer فقط.

### الأطروحة

> نظام يصنف failure حسب span:
- retrieval failure
- prompt failure
- tool failure
- verifier failure
- aggregation failure
- cost runaway

### MVP

Trace in → failure taxonomy out.

### المخاطر

يحتاج بيانات traces متنوعة.

---

## Thesis E — Local Experiment Harness for AI Systems

### المشكلة

الباحث/المطور يحتاج يجرب routes وmodels وpolicies بسرعة بدون SaaS.

### الأطروحة

> harness محلي لتجارب AI systems: routing, evals, cost, traces, reports.

### MVP

CLI:

```text
run config.yaml
compare routes
produce report.md
```

### لماذا مناسب لنا؟

نحن بالفعل بنينا نواة منه.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Cheap Genius Runtime Layer | 4 | 5 | 4 | 5 | 4 | 22 |
| AI Workflow Flight Recorder | 3 | 4 | 5 | 4 | 3 | 19 |
| Cost-to-Quality Profiler | 4 | 5 | 5 | 5 | 3 | 22 |
| Failure Taxonomy Engine | 4 | 4 | 3 | 4 | 4 | 19 |
| Local Experiment Harness | 4 | 4 | 5 | 4 | 3 | 20 |

---

# أقوى Candidates من هذا المحور

## 1. Cost-to-Quality Profiler

أداة عملية جدًا:

> أعطني task/eval set وroutes، أعطيك Pareto frontier وأرخص route كافي.

هذه فكرة قوية لأنها لا تنافس observability platforms مباشرة؛ بل تساعد الناس يختاروا route.

## 2. Cheap Genius Runtime Layer

أوسع وأقوى، لكن أكبر حجمًا.

---

# مقارنة مع candidates السابقة

| Candidate | من محور | ملاحظة |
|---|---|---|
| Citation Integrity Engine | Research | wedge واضح |
| Agent Cost Governor | Agents | runtime control |
| Private Document Extraction SLM | Local AI | privacy/cost domain |
| Cost-to-Quality Profiler | Infrastructure | universal evaluation/profiling |
| Cheap Genius Runtime Layer | Infrastructure | platform direction |

---

# الفكرة العميقة من المحور

بدل بناء application مباشر، يمكن بناء:

> طبقة قياس واختيار للأنظمة المركبة.

أي:

- لا نقرر أي route أفضل بالحدس.
- نشغل routes ونقيس cost/quality/latency.
- نستخرج Pareto frontier.
- نختار policy.

هذا ينسجم جدًا مع كل تجربتنا.

---

# القرار

نضيف إلى Top Candidates:

1. Cost-to-Quality Profiler
2. Cheap Genius Runtime Layer

ولا نقرر بعد.
