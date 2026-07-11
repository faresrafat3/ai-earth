# Project Idea Discovery Protocol — لا توجد فكرة نهائية بعد

## المبدأ

حاليًا لا نملك فكرة مشروع نهائية. لدينا اسم/اتجاه عام فقط.

الهدف ليس الدفاع عن فكرة مبكرة، بل استخراج الفكرة من:

- الأبحاث الحديثة.
- المجالات العلمية الناضجة.
- المشاريع المفتوحة.
- الشركات والمنتجات الناجحة.
- الترندات الحقيقية لا الإعلامية.
- مشاكل التكلفة والذكاء والتوسع.

القاعدة:

> لا نبني MVP قبل أن نمر بمرحلة discovery واسعة ومقارنة أطروحات.

---

## شروط الفكرة التي نبحث عنها

الفكرة يجب أن تجمع أكبر قدر ممكن من:

1. ذكاء أعلى أو قدرة معرفية أكبر.
2. تكلفة أقل أو استخدام أذكى للموارد.
3. قابلية توسع سريعة.
4. اعتماد على علوم/أدبيات قوية.
5. إمكانية بناء MVP بسرعة.
6. ارتباط بمشكلة حقيقية ومؤلمة.
7. قابلية دفاع أو تراكم بيانات/خبرة.
8. ليست hype فقط.
9. مناسبة لمواردنا الحالية.
10. قابلة للاختبار خلال أسبوع.

---

## طريقة البحث

كل محور يمر بثلاث مراحل:

### 1. Online Round

جمع 10–20 مصدرًا:

- papers
- surveys
- GitHub projects
- companies/products
- benchmarks
- blog posts التقنية الجادة

### 2. Offline Audit

استبعاد:

- hype.
- claims بلا قياس.
- أفكار تحتاج رأس مال ضخم.
- مشاريع لا تخفض التكلفة ولا تزيد الذكاء.
- أفكار لا تناسب فرد/فريق صغير.

### 3. Thesis Extraction

نستخرج candidate thesis:

```text
Thesis:
Scientific base:
Why now:
MVP:
Cost advantage:
Intelligence advantage:
Risks:
1-week validation:
```

---

## المحاور الكبرى التي يجب مسحها

## A. Cost-Aware Adaptive Inference

- model routing
- cascades
- FrugalGPT
- RouteLLM
- inference FinOps
- caching/batching/quantization
- value of information

## B. Agentic Systems / AI Workers

- multi-agent workflows
- long-horizon agents
- task decomposition
- agent reliability
- memory
- tool use
- workflow automation

## C. AI for Research / Evidence Engines

- literature discovery
- claim verification
- scientific audit
- paper-to-code
- research copilots
- citation graph reasoning

## D. AI Evaluation / Verification

- LLM-as-judge
- verifier gain
- cross-family verification
- uncertainty calibration
- benchmark contamination
- reliability metrics

## E. Multimodal / World Models / Robotics

- VLA models
- embodied intelligence
- world models
- simulation
- planning
- action-grounded reasoning

## F. Personal Cognitive Systems

- memory agents
- personal knowledge systems
- AI companion/collaborator
- cognitive operating systems
- attention and productivity augmentation

## G. Local / Edge / Cheap AI

- small models
- quantization
- local inference
- on-device agents
- privacy-preserving assistants
- hybrid local-cloud routing

## H. AI Infrastructure / Compound AI Systems

- orchestration
- LangGraph/DSPy/LlamaIndex
- observability
- cost governance
- model gateways
- evaluation loops

## I. AI for Science / Discovery

- drug discovery
- materials
- theorem proving
- automated experimentation
- simulation + ML
- lab agents

## J. Data / Knowledge / Retrieval

- RAG 2.0
- structured extraction
- knowledge graphs
- semantic caching
- data flywheels
- web agents

---

## Scoring Matrix

كل candidate يأخذ 1–5 في:

| المعيار | السؤال |
|---|---|
| Intelligence gain | هل يزيد القدرة؟ |
| Cost advantage | هل يخفض التكلفة؟ |
| Speed to MVP | هل يبنى بسرعة؟ |
| Scientific maturity | هل له أدبيات قوية؟ |
| Market pain | هل المشكلة مؤلمة؟ |
| Scalability | هل يتوسع؟ |
| Moat/data flywheel | هل يتحسن مع الاستخدام؟ |
| Personal fit | هل يناسب قدراتنا ومواردنا؟ |
| Low hype | هل بعيد عن الدعاية؟ |
| 1-week validation | هل يمكن اختباره سريعًا؟ |

نحسب:

```text
Total = sum(scores)
Risk-adjusted = Total - hype_penalty - capital_penalty
```

---

## مخرجات مرحلة Discovery

نريد في النهاية:

## Top 3 Theses

كل واحدة بصيغة:

```text
Name:
Thesis:
Problem:
Scientific base:
Why now:
MVP:
Who needs it:
Why cheap:
Why intelligent:
Risks:
Validation plan:
```

ثم نختار واحدة فقط للبناء.

---

## القرار الحالي

`Cheap Genius Router` هو candidate قوي، لكنه ليس الفكرة النهائية.

لا نقرر قبل مسح المحاور الكبرى.

---

## قاعدة عدم التسرع

أي فكرة تبدو جذابة يجب أن تسأل:

1. هل هي مبنية على مجال ناضج؟
2. هل هناك مشاريع موجودة تثبت الطلب؟
3. ما الذي سنفعله أفضل أو أرخص؟
4. هل يمكن لشخص واحد بناء نسخة أولى؟
5. هل فيها data/learning loop؟
6. هل يمكن اختبارها خلال أسبوع؟

إذا لا، تُحفظ كـ idea لا thesis.
