# Discovery Round 1 — AI for Research / Evidence Engines

## لماذا بدأنا بهذا المحور؟

لأنه يجمع شروطنا:

- ذكاء عميق.
- تكلفة منخفضة نسبيًا.
- قابلية بناء MVP بسرعة.
- اعتماد على الأدبيات.
- ارتباط مباشر بطريقة تفكيرنا: تدقيق، بحث، استبعاد hype، بناء evidence.

---

## Online Round — مصادر واتجاهات

## 1. AI4Research Survey

الرابط: https://arxiv.org/html/2507.01903v2

تصنيف شامل لـ AI في البحث العلمي عبر:

- scientific comprehension
- academic surveys
- scientific discovery
- academic writing
- peer review

مهم لأنه يوضح أن المجال أكبر من “literature review tool”. يوجد اتجاه كامل نحو AI يشارك في دورة البحث.

## 2. Biological AI Agents Survey

الرابط: https://pmc.ncbi.nlm.nih.gov/articles/PMC12936789/

استعرض 115 دراسة عن AI agents في البيولوجيا، ويؤكد أن agents تتحول من مجرد RAG إلى co-investigators تستخدم أدوات وقواعد بيانات وتجارب مغلقة الحلقة.

مهم لأنه يوضح أن research agents ليست hype فقط في البيولوجيا، لكنها تحتاج reliability/evaluation.

## 3. Deep Research Agents in Biomedical Scenarios

الرابط: https://www.jmir.org/2026/1/e88195/PDF

يناقش OpenAI Deep Research وأمثاله في الطب والبيولوجيا. يذكر أن deep research agents تستطيع توليد evidence tables بسرعة، لكن citation accuracy مشكلة كبيرة.

مهم لأنه يثبت الطلب والفائدة، ويكشف pain واضح: citation correctness.

## 4. Detecting and Correcting Reference Hallucinations

الرابط: https://arxiv.org/html/2604.03173v1

يركز على citation/reference hallucinations في أدوات البحث التجارية، ويذكر Benchmarks مثل DRBench وFACT وCiteGuard وGhostCite.

مهم جدًا لأن citation verification قد يكون wedge قوي.

## 5. GPTZero ICLR/NeurIPS hallucination investigations

روابط:

- https://gptzero.me/news/iclr-2026/
- https://gptzero.me/news/neurips/

يدعي العثور على hallucinated citations في أوراق مؤتمرية كبرى.

مهم لأنه يدل على مشكلة حقيقية في peer review والنشر: citation hallucination تسربت إلى papers.

## 6. AI Research Tools Landscape 2026

روابط:

- https://papersflow.ai/blog/best-ai-research-tools-2026
- https://paperguide.ai/blog/academic-research-ai/

تذكر أدوات مثل:

- Semantic Scholar
- Elicit
- Consensus
- Scite
- SciSpace
- Connected Papers
- Research Rabbit
- NotebookLM
- PapersFlow/Paperguide

مهم لمعرفة السوق والمنافسين.

---

# Offline Audit

## ما هو الحقيقي هنا؟

الحقيقي:

1. الباحثون يحتاجون discovery/screening/synthesis.
2. أدوات البحث موجودة وكثيرة.
3. citation hallucination مشكلة فعلية ومؤلمة.
4. deep research agents مفيدة لكنها غير موثوقة بما يكفي.
5. التحقق من الأدلة/citations مجال واضح وقياسي.

## ما هو hype؟

1. “AI scientist fully autonomous” غالبًا hype.
2. “agent يكتب literature review كامل” بدون citation verification خطر.
3. أدوات تولد نصًا أكاديميًا بدون evidence grounding ليست كافية.
4. multi-agent research teams قد تكون مكلفة ومعقدة قبل وجود verifier قوي.

---

# Candidate Theses من هذا المحور

## Thesis A — Citation Integrity Engine

### المشكلة

AI والباحثون يكتبون citations خاطئة أو مختلطة أو مزيفة. المراجعين لا يملكون وقتًا للتحقق يدويًا.

### الأطروحة

> أداة تتحقق من كل citation داخل paper/report: هل الورقة موجودة؟ هل المؤلفون/العنوان صحيحون؟ وهل المصدر يدعم claim المجاور؟

### العلم/الأدبيات

- factuality verification
- citation attribution
- RAG validation
- claim-source alignment
- information retrieval

### لماذا الآن؟

- LLM-generated citations تنتشر.
- مؤتمرات كبرى بدأت ترى hallucinated references.
- Deep research agents تجعل المشكلة أكبر.

### MVP

Input:

- PDF أو markdown.

Output:

- قائمة citations.
- حالة كل citation:
  - exists / not found
  - metadata mismatch
  - unsupported claim
  - weak support
  - strong support

### لماذا رخيص؟

يمكن استخدام:

- Serper/Semantic Scholar/OpenAlex للبحث.
- Firecrawl لجلب الصفحات.
- LLM صغير للتطابق الأولي.
- LLM أقوى فقط للحالات المشكوك فيها.

### لماذا ذكي؟

لأنه لا يكتب بدل الباحث، بل يحميه من أخطر خطأ: evidence falsification.

### المخاطر

- الوصول للـ PDFs.
- paywalls.
- صعوبة claim-source alignment.

### 1-week validation

اختر 20 references من papers، بينها أخطاء مصطنعة، وقس precision/recall في اكتشافها.

---

## Thesis B — Research Evidence Table Builder

### المشكلة

الباحث يحتاج evidence table موثوق، لا مجرد ملخص.

### الأطروحة

> نظام يبني evidence table من أوراق حقيقية، مع كل claim مربوط بمصدر وسطر/فقرة.

### MVP

Query → papers → extracted claims → evidence table.

### الفرق عن الأدوات الحالية

التركيز ليس على “كتابة review”، بل على evidence objects قابلة للتفتيش.

### المخاطر

منافسة Elicit/PapersFlow/Paperguide.

### التقييم

هل كل row مدعوم بمصدر صحيح؟

---

## Thesis C — Scientific Claim Auditor

### المشكلة

الأوراق والتقارير تحتوي claims مبالغ فيها أو غير مدعومة.

### الأطروحة

> أداة تقرأ نصًا علميًا وتفصل claims إلى: مدعوم، مبالغ فيه، غير مدعوم، يحتاج دليل.

### MVP

Input: abstract/introduction/discussion.  
Output: claim audit table.

### لماذا مناسب لنا؟

يتماشى مع كل منهجيتنا: offline audit، anti-hype، evidence sufficiency.

### المخاطر

صعب جدًا بدون retrieval جيد.

---

## Thesis D — Deep Research Agent Evaluator

### المشكلة

أدوات Deep Research كثيرة، لكن لا أحد يعرف أيها يهلوس أكثر أو أدق.

### الأطروحة

> benchmark/service يختبر deep research outputs: citation accuracy، factuality، coverage، contradiction handling.

### MVP

اعطِ نفس query لعدة agents، ثم قيّم:

- references exist?
- source supports claim?
- missing key papers?
- fabricated citations?

### المخاطر

قد يحتاج وصول لعدة agents مدفوعة.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Citation Integrity Engine | 4 | 4 | 5 | 5 | 3 | 21 |
| Evidence Table Builder | 4 | 3 | 4 | 4 | 3 | 18 |
| Scientific Claim Auditor | 5 | 3 | 3 | 4 | 4 | 19 |
| Deep Research Agent Evaluator | 4 | 3 | 3 | 4 | 3 | 17 |

---

# النتيجة الأولية للمحور

أقوى candidate من هذا المحور:

# Citation Integrity Engine

لأنه:

- مشكلة واضحة.
- قابلة للاختبار بسرعة.
- غير مكلفة كبداية.
- مرتبطة مباشرة بالهلاوس والبحث العلمي.
- لها wedge واضح قبل بناء research agent كامل.

## الفكرة العميقة

بدل أن نبني “باحث AI كامل”، نبني أولًا:

> طبقة ثقة Evidence Integrity Layer

لأن كل research agent يحتاجها.

---

# القرار

هذا المحور أعطى candidate قوي جدًا، لكنه ليس قرارًا نهائيًا.

ينتقل إلى قائمة Top Candidates للمقارنة مع محاور أخرى.
