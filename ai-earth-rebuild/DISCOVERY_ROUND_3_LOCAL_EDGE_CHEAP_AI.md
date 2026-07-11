# Discovery Round 3 — Local / Edge / Cheap AI

## الهدف

استكشاف اتجاه:

> هل المستقبل الأقوى لمشروعنا هو استخدام نماذج صغيرة/محلية/هجينة لتقليل التكلفة والاعتماد على السحابة، مع التصعيد فقط عند الحاجة؟

هذا المحور مهم لأنه يضرب مباشرة شرطنا: **ذكاء + رخص + توسع**.

---

# Online Round — مصادر واتجاهات

## 1. Small Language Models and Edge AI: 2026 Shift

الرابط: https://zylos.ai/research/2026-02-07-small-language-models-edge-ai

يتحدث عن انتقال الصناعة إلى SLMs وedge AI بسبب:

- latency
- privacy
- cost
- offline availability

يشير إلى hybrid architectures:

> SLMs handle routine tasks locally, cloud LLMs handle complex edge cases.

هذا قريب جدًا من Cheap Genius.

---

## 2. Edge AI in 2026

الرابط: https://www.unifiedaihub.com/blog/edge-ai-in-2026-processing-intelligence-where-data-is-generated

يركز على تشغيل الذكاء حيث تُولد البيانات. أمثلة:

- كاميرات ذكية.
- مصانع.
- أجهزة طبية.
- field service.
- hybrid edge-cloud.

---

## 3. Key Edge AI Trends 2026

الرابط: https://www.n-ix.com/edge-ai-trends/

يركز على quantization, pruning, SLMs, hybrid edge-cloud.

مهم لأنه يوضح أن local AI ليس فقط شات؛ هناك استخدامات enterprise حقيقية.

---

## 4. Top Small Language Models 2026

الرابط: https://www.intuz.com/blog/best-small-language-models

يسرد نماذج مثل:

- Phi
- Gemma
- Mistral
- Llama 3.2
- Qwen

ويؤكد أن SLMs مناسبة للمهام المحددة والمنظمة.

---

## 5. Enterprise Guide to SLMs

الرابط: https://hyperion-consulting.io/en/insights/slm-small-language-models-enterprise-2026

يناقش مهام SLMs المناسبة:

- classification
- extraction
- sentiment
- Q&A over context
- short summarization
- form filling
- template generation

ويوضح أن SLMs ليست بديلًا عامًّا للـ frontier models، بل مكون في architecture هجينة.

---

## 6. SLMQuant

الرابط: https://arxiv.org/abs/2511.13023

Benchmark لتكميم small language models. مهم لأنه يقول إن SLMs لها حساسية quantization مختلفة عن LLMs، ولا يمكن نقل تقنيات LLM compression مباشرة.

---

## 7. Edge-First Language Model Deployment

الرابط: https://arxiv.org/pdf/2505.16508

يناقش metrics للـ edge SLMs تشمل:

- quality
- responsiveness
- energy
- cost

مهم جدًا لأنه يوسع مفهوم cost من dollars إلى latency/energy.

---

## 8. LLM-SLM Collaboration Survey

الرابط: https://arxiv.org/html/2510.13890

Survey عن تعاون النماذج الصغيرة والكبيرة. يقدم taxonomy لأهداف التعاون:

- performance enhancement
- cost-effectiveness
- cloud-edge privacy
- trustworthiness

مهم لأنه يعطي أساس علمي لفكرة hybrid local-cloud.

---

# Offline Audit

## ما الحقيقي؟

1. SLMs مناسبة جدًا للمهام المنظمة والمتكررة.
2. local/edge AI يوفر:
   - خصوصية.
   - تكلفة أقل.
   - latency أقل.
   - offline availability.
3. hybrid local-cloud هو النمط الأكثر واقعية.
4. quantization/pruning ليست تفاصيل؛ تؤثر في الجودة.
5. SLMs ليست بديلًا كاملًا للـ LLMs، بل طبقة أولى.

## ما الـ hype؟

1. “SLMs = GPT-4 locally” مبالغة.
2. معظم الادعاءات عن 80–90% quality تعتمد على مهام محددة.
3. edge deployment أصعب من API بسبب hardware, updates, monitoring.
4. الخصوصية وحدها ليست market unless في قطاعات حساسة.

---

# Candidate Theses

## Thesis A — Local-First AI Router

### المشكلة

الشركات/الأفراد يرسلون كل شيء إلى السحابة رغم أن 70–90% من المهام قد تكون بسيطة أو حساسة.

### الأطروحة

> نظام يشغل SLM محلي أولًا، ويصعّد للسحابة فقط عندما تفشل إشارات الثقة أو تتطلب المهمة معرفة/استدلال أقوى.

### MVP

- local model عبر Ollama/llama.cpp.
- k0=3 أو confidence check.
- if stable: return local answer.
- else: cloud escalation.

### لماذا قوي؟

يجمع:

- privacy
- cost reduction
- speed
- offline mode

### المخاطر

- deployment friction.
- hardware variability.
- جودة local models.

---

## Thesis B — Private Document Extraction SLM

### المشكلة

المؤسسات لديها مستندات حساسة وتحتاج extraction/classification بدون إرسال البيانات للسحابة.

### الأطروحة

> local SLM pipeline لاستخراج structured data من docs، مع cloud fallback فقط للحالات غير الواثقة.

### MVP

PDF/text → local extraction JSON → confidence/validation → cloud fallback.

### السوق

- قانون.
- طب.
- مالية.
- حكومي.

### لماذا يناسبنا؟

يتكامل مع Evidence Engine/Citation Integrity.

---

## Thesis C — Edge AI Cost Benchmark Lab

### المشكلة

الناس لا تعرف أي local model/quantization/hardware مناسب لتطبيقها.

### الأطروحة

> benchmark service يقيس quality/latency/energy/cost لمهام محددة عبر SLMs وquantizations.

### MVP

اختبار 5 models × 3 quantizations × tasks محددة.

### المخاطر

يتطلب hardware أو infrastructure.

---

## Thesis D — Hybrid Local-Cloud Agent

### المشكلة

agents السحابية مكلفة وحساسة للخصوصية.

### الأطروحة

> agent يعمل محليًا للخطوات البسيطة، ويصعّد فقط للخطوات المعقدة.

### MVP

local planner/extractor + cloud reasoner fallback.

### المخاطر

agent reliability ما زالت صعبة.

---

## Thesis E — SLM Fine-Tuning Kit for Narrow Workflows

### المشكلة

الشركات تحتاج نموذج صغير متخصص لمهمة متكررة.

### الأطروحة

> أداة تبني/تقيّم fine-tuned SLM workflow من 1000–5000 مثال.

### المخاطر

MLOps وdata prep أكبر من اللازم للفرد.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Local-First AI Router | 4 | 5 | 3 | 4 | 3 | 19 |
| Private Document Extraction SLM | 4 | 5 | 4 | 5 | 4 | 22 |
| Edge AI Cost Benchmark Lab | 3 | 4 | 3 | 3 | 3 | 16 |
| Hybrid Local-Cloud Agent | 4 | 5 | 3 | 4 | 3 | 19 |
| SLM Fine-Tuning Kit | 4 | 4 | 2 | 4 | 4 | 18 |

---

# أقوى Candidate من هذا المحور

# Private Document Extraction SLM

## لماذا؟

لأنه:

- واضح ومؤلم.
- local-first = privacy/cost.
- MVP ممكن.
- يتكامل مع Evidence Integrity.
- يمكن قياسه بسهولة: extraction F1 / cost / latency.
- لا يحتاج بناء agent كامل.

## الفكرة

> شغّل extraction محليًا أولًا، وصعّد فقط للحالات غير الواثقة.

مثال:

- أوراق علمية.
- عقود.
- تقارير طبية.
- فواتير.
- ملفات امتثال.

---

# مقارنة مع candidates السابقة

| Candidate | المجال | القوة |
|---|---|---|
| Citation Integrity Engine | AI for Research | evidence trust |
| Agent Cost Governor | Agentic Systems | runtime cost control |
| Private Document Extraction SLM | Local/Edge AI | privacy + cost + structured tasks |

---

# فكرة الدمج المحتملة

المرشح الثالث يقربنا من فكرة كبيرة:

> Evidence/Document Intelligence Layer رخيص وخصوصي.

قد يجمع:

- Citation Integrity
- Evidence Tables
- Private Document Extraction
- Local-first routing

أي:

# Cheap Genius for Documents & Evidence

هذه قد تكون أقوى من router عام لأنها domain أوضح.

---

# القرار

نضيف `Private Document Extraction SLM` إلى Top Candidates.

لا نقرر بعد.
