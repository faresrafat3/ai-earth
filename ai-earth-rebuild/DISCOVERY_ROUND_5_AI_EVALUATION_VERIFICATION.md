# Discovery Round 5 — AI Evaluation / Verification

## الهدف

استكشاف مجال تقييم وموثوقية أنظمة AI:

- LLM-as-judge
- verifier gain
- hallucination benchmarks
- benchmark contamination
- factuality
- citation/evidence verification
- judge bias
- evaluation infrastructure

هذا المحور مهم لأنه قد يكون الجذر الأعمق لكل شيء: إذا لم نعرف كيف نقيس، لا نعرف كيف نبني.

---

# Online Round — مصادر واتجاهات

## 1. LLM Benchmarks in 2026

الرابط: https://www.lxt.ai/blog/llm-benchmarks/

يوضح أن benchmarks كثيرة أصبحت saturated مثل MMLU, GSM8K, HumanEval، وأن benchmarks الحديثة الأهم هي:

- SWE-bench Verified
- LiveCodeBench
- HLE
- GAIA
- HELM
- HalluLens

**الأثر:** لا بد من domain-specific, contamination-resistant evaluation.

---

## 2. RIKER / Document Q&A Hallucination Measurement

الرابط: https://arxiv.org/html/2603.08274

يقيس hallucination في document Q&A على نطاق ضخم، باستخدام ground-truth-first methodology بدون LLM judges. يدرس:

- model family
- context length
- temperature
- hardware

**الأثر:** ground-truth-first evaluation أقوى من LLM-judge فقط.

---

## 3. FactBench

الرابط: https://aclanthology.org/2025.acl-long.1587.pdf

Dynamic benchmark لـ factuality in-the-wild. يفكك الإجابة إلى وحدات ويسترجع evidence ثم يصنف factuality.

**الأثر:** تقييم factuality يحتاج unit decomposition + retrieval + evidence labels.

---

## 4. HalluLens

الرابط: https://arxiv.org/html/2504.17550v1

Benchmark للهلاوس، يناقش refusal/correctness tradeoff، ويظهر أن بعض طرق القياس legacy مثل TruthfulQA فيها مشاكل.

**الأثر:** لا يكفي قياس accuracy؛ يجب قياس refusal/hallucination tradeoff.

---

## 5. LLM-as-a-Judge Reliability/Bias

الرابط: https://www.adaline.ai/blog/llm-as-a-judge-reliability-bias

يناقش family bias, self-preference, formatting/verbosity bias، ويذكر Judge Reliability Harness.

**الأثر:** لا يجوز استخدام judge بدون bias audit.

---

## 6. LLM-as-a-Judge Evaluation overview

الرابط: https://www.emergentmind.com/topics/llm-as-a-judge-evaluations

يوضح أن LLM judges قد تتفق مع البشر في بعض المهام، لكنها ضعيفة في expert domains واللغات والحدود الصعبة.

**الأثر:** judges تصلح كمكمل، لا ground truth.

---

## 7. Quantifying and Mitigating Self-Preference Bias

الرابط: https://arxiv.org/html/2604.22891v2

يحاول قياس self-preference bias عبر constructed equal-quality pairs وhuman clusters.

**الأثر:** judge bias يمكن قياسه، وليس فقط التحذير منه.

---

## 8. When Does Verification Pay Off?

الرابط: https://arxiv.org/abs/2512.02304

قدم verifier gain ودرس self/intra/cross-family verification عبر 37 موديل و9 benchmarks.

**الأثر:** usefulness of verifier يجب قياسه كـ gain/precision/FPR، لا accuracy فقط.

---

# Offline Audit

## ما الحقيقي؟

1. evaluation أصبح عنق زجاجة أساسي.
2. benchmarks العامة تتشبع أو تتلوث.
3. LLM-as-judge مفيد لكنه منحاز.
4. ground-truth-first وdeterministic scoring أقوى حيث ممكن.
5. verifier usefulness يعتمد على FPR/precision/gain، لا على قوة الموديل فقط.
6. factuality تحتاج evidence-grounded decomposition.

## ما الـ hype؟

1. “LLM judge يحل التقييم” مبالغة.
2. leaderboard chasing بلا domain relevance.
3. benchmarks saturated تعطي ثقة زائفة.
4. automated eval بلا audit يصبح مصدر هلاوس جديد.

---

# Candidate Theses

## Thesis A — Evaluation First Harness

### المشكلة

معظم الفرق تبني AI pipelines ثم تكتشف أنها لا تعرف كيف تقيس الجودة.

### الأطروحة

> أداة تبدأ من eval set وتبني harness: metrics, cost, latency, judge bias checks, reports.

### MVP

- YAML config.
- dataset.
- routes/models.
- metrics.
- report.

### لماذا قوي؟

يناسب كل مشاريع AI.

### المخاطر

سوق مزدحم: Braintrust, Langfuse, Phoenix, etc.

---

## Thesis B — Judge Bias Auditor

### المشكلة

الناس تستخدم LLM-as-judge بدون معرفة bias.

### الأطروحة

> أداة تختبر judge عبر position/format/verbosity/self-family bias وتنتج reliability report.

### MVP

Input:

- judge model
- rubric
- sample outputs

Output:

- bias report
- consistency score
- disagreement cases

### لماذا قوي؟

تخصص دقيق داخل سوق evaluation.

---

## Thesis C — Verifier Gain Calculator

### المشكلة

لا أحد يعرف هل verifier يستحق التكلفة قبل استخدامه.

### الأطروحة

> احسب verifier gain من عينة صغيرة: TPR/FPR/precision/cost، ثم قرر هل تستخدم verifier في الإنتاج.

### MVP

- candidate answers with labels
- verifier judgments
- compute gain
- recommend use / don't use

### لماذا مناسب لنا؟

قريب من تجاربنا وكلفة منخفضة.

---

## Thesis D — Hallucination & Citation Eval Suite

### المشكلة

الأدوات البحثية تنتج citations وclaims قد تكون خاطئة.

### الأطروحة

> benchmark/eval suite يقيس: citation existence, claim support, factuality, refusal, unsupported statements.

### MVP

مجموعة اختبارات صغيرة للـ research agents.

### يتداخل مع

Citation Integrity Engine.

---

## Thesis E — Ground-Truth-First Synthetic Eval Generator

### المشكلة

كثير من evals تعتمد على LLM judges أو datasets ملوثة.

### الأطروحة

> توليد tasks من ground truth معروف، ثم تقييم deterministic بدون judge.

### أمثلة

- document QA من synthetic docs.
- arithmetic/symbolic tasks.
- structured extraction with known fields.

### لماذا قوي؟

يبني evals رخيصة ونظيفة.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Evaluation First Harness | 4 | 4 | 4 | 5 | 3 | 20 |
| Judge Bias Auditor | 4 | 4 | 4 | 4 | 4 | 20 |
| Verifier Gain Calculator | 4 | 5 | 5 | 4 | 3 | 21 |
| Hallucination & Citation Eval Suite | 5 | 4 | 4 | 5 | 4 | 22 |
| Ground-Truth-First Eval Generator | 5 | 5 | 4 | 4 | 4 | 22 |

---

# أقوى Candidates من هذا المحور

## 1. Ground-Truth-First Eval Generator

قوي لأنه يتجنب LLM judge في المجالات الممكنة.

## 2. Hallucination & Citation Eval Suite

قوي لأنه يتكامل مع Citation Integrity.

## 3. Verifier Gain Calculator

قوي لأنه يحول verifier من حدس إلى قرار تكلفة/فائدة.

---

# الفكرة العميقة من هذا المحور

قبل بناء AI ذكي، ابني:

> evaluation substrate

أي طبقة تولد أو تجمع اختبارات قابلة للتحقق، وتقيّم التكلفة والدقة والتحيز.

---

# مقارنة مع candidates السابقة

| Candidate | المحور | العلاقة |
|---|---|---|
| Citation Integrity Engine | Research | تطبيق محدد للتقييم |
| Cost-to-Quality Profiler | Infrastructure | يقيس routes |
| Verifier Gain Calculator | Evaluation | يقيس فائدة verifier |
| Ground-Truth Eval Generator | Evaluation | يبني بيانات تقييم موثوقة |

قد تكون هذه كلها أجزاء من مشروع واحد:

# Evidence & Evaluation OS

---

# القرار

نضيف إلى Top Candidates:

1. Ground-Truth-First Eval Generator
2. Hallucination & Citation Eval Suite
3. Verifier Gain Calculator

ولا نقرر بعد.
