# Discovery Round 6 — RAG / Knowledge / Retrieval / Data Flywheels

## لماذا هذا المحور محوري؟

كل المسارات السابقة تحتاج knowledge layer:

- Citation Integrity يحتاج retrieval والتحقق من المصادر.
- Evidence Tables تحتاج استخراج claims من corpus.
- Research Agents تحتاج literature retrieval.
- Local Document Intelligence تحتاج private RAG.
- Agent Memory تحتاج retrieval + provenance.
- Evaluation يحتاج ground-truth/evidence stores.

لذلك RAG/Knowledge ليس مجرد feature؛ قد يكون البنية العميقة المشتركة.

---

# Online Round — مصادر واتجاهات

## 1. Graph Retrieval-Augmented Generation (GRAG)

الرابط: https://www.emergentmind.com/topics/graph-retrieval-augmented-generation-grag

يتناول GraphRAG وGRAG كاتجاه يتجاوز flat vector retrieval. النقطة المهمة: graph retrieval يفيد خصوصًا في multi-hop reasoning وrelational queries، لكن ليس بالضرورة في simple lookup.

**الأثر:** لا نستخدم GraphRAG دائمًا؛ نحتاج router يقرر متى graph retrieval يستحق تكلفته.

---

## 2. Awesome GraphRAG

الرابط: https://github.com/DEEP-PolyU/Awesome-GraphRAG

قائمة محدثة جدًا بأعمال GraphRAG، وتذكر أعمال حديثة مثل:

- LinearRAG
- MemGraphRAG
- ProbeRAG
- LegalGraphRAG
- LogicPoison
- GraphRAG Benchmark

**الأثر:** المجال نشط جدًا ويتطور بسرعة؛ توجد فرص في benchmark, safety, legal/reliable RAG.

---

## 3. A-RAG: Scaling Agentic RAG via Hierarchical Retrieval Interfaces

الرابط: https://arxiv.org/html/2602.03442v1

يقترح agentic retrieval عبر hierarchical interfaces. يقارن Naive RAG, GraphRAG, HippoRAG2, LinearRAG, FaithfulRAG, MA-RAG.

**الأثر:** retrieval لم يعد خطوة ثابتة؛ صار فعلًا agentic decision process.

---

## 4. RAGPerf

الرابط: https://arxiv.org/html/2603.10765v1

Benchmark end-to-end لـ RAG systems، يهتم بقياس pipeline traces وجودة الإجابة.

**الأثر:** RAG لا يقاس بالretriever فقط أو answer فقط؛ يجب end-to-end.

---

## 5. When to Use Graphs in RAG / GraphRAG-Bench

الرابط: https://arxiv.org/abs/2506.05690

سؤال الورقة نفسه ممتاز:

> متى تفيد الرسوم البيانية في RAG؟

تقول إن GraphRAG لا يتفوق دائمًا، ويجب تحديد سيناريوهات الاستفادة.

**الأثر:** نفس فلسفتنا: لا تستخدم التقنية لأنها جميلة؛ استخدمها عندما الشروط تبررها.

---

## 6. RAG State of the Art 2026

الرابط: https://techwithcolonel.com/artifact/rag-state-of-the-art-2026.html

يعرض اتجاهات مثل:

- LazyGraphRAG
- HippoRAG
- LightRAG
- Long-context vs RAG
- Agentic search
- Hybrid routing

النقطة المهمة:

> السؤال لم يعد RAG أم لا، بل أي خليط من cache/context/retrieval/graph/agentic search تحتاجه هذه query class؟

---

## 7. Long Context vs RAG

ظهر في جداول RAG research أن هناك مقارنة مهمة:

- long context قد يتفوق في بعض مهام QA.
- RAG أفضل عندما corpus كبير جدًا، freshness مهمة، source attribution مطلوبة، أو التكلفة عالية.

**الأثر:** RAG نفسه يحتاج routing ضد long-context/caching.

---

## 8. Cache-Augmented Generation / Semantic Caching

من اتجاهات AI FinOps وRAG:

- cache قد يكون أفضل من RAG عندما knowledge base محدود ومتكرر.
- semantic caching يقلل calls لكنه يخاطر false positives.

**الأثر:** knowledge retrieval ليس دائمًا search؛ أحيانًا cache هو المسار الأرخص.

---

## 9. HTMLRAG / Structure-Preserving Retrieval

اتجاه يستخدم HTML/structure بدل plain text للحفاظ على semantics.

**الأثر:** document intelligence يحتاج preservation of structure: tables, headings, citations, layout.

---

## 10. LegalGraphRAG / Domain GraphRAG

ظهور LegalGraphRAG وغيره يعني أن GraphRAG قد يكون قويًا في domains ذات علاقات منظمة: قانون، طب، علم.

**الأثر:** domain-specific knowledge graphs قد تكون moat.

---

# Offline Audit

## ما الحقيقي؟

1. RAG الأساسي أصبح commodity.
2. GraphRAG/Agentic RAG قوي في multi-hop/relational tasks، لكنه مكلف وقد لا يفيد في simple lookup.
3. Long-context ينافس RAG في بعض الحالات.
4. Caching قد يهزم retrieval في knowledge bases المتكررة.
5. Evaluation أهم من architecture: هل retrieval فعلاً يدعم claim؟
6. Domain structure مهم جدًا: legal/science/biomedical/document workflows.

## ما الـ hype؟

1. “GraphRAG أفضل دائمًا” خطأ.
2. “RAG مات بسبب long context” خطأ.
3. “Agentic RAG لكل query” مكلف ومبالغ فيه.
4. “Vector DB = knowledge” تبسيط.
5. “Knowledge graph يبني نفسه تلقائيًا بلا أخطاء” خطير.

---

# التحليل العميق

## 1. المشكلة ليست retrieval فقط، بل routing بين أنماط knowledge access

لدينا مسارات مختلفة:

- no retrieval
- semantic cache
- vector RAG
- keyword/BM25
- graph traversal
- long-context preload
- agentic multi-step search
- web search
- human/source verification

السؤال الحقيقي:

> أي route معرفي أرخص كفاية لهذه query؟

هذا يربط RAG بمحور Cheap Genius.

---

## 2. Evidence grounding هو المنتج، retrieval مجرد وسيلة

المستخدم لا يريد “documents retrieved”.

يريد:

- claim supported?
- source exists?
- contradiction?
- exact quote?
- confidence?
- what is missing?

إذن النظام يجب أن ينتقل من retrieval إلى evidence operations.

---

## 3. Data flywheel ممكن يظهر من التصحيح البشري

كل مرة يصحح المستخدم:

- source relevance
- claim support
- false citation
- extraction error

نحصل على training/evaluation data.

هذه قد تكون moat أقوى من مجرد wrapper.

---

## 4. Knowledge systems تحتاج cost-aware composition

GraphRAG قد يكون قويًا، لكنه مكلف. Agentic RAG أقوى، لكنه أغلى. Long-context أسهل، لكنه قد يكون مكلفًا. Cache أرخص، لكنه قد يخطئ.

إذن candidate قوي:

> Knowledge Route Optimizer

---

# Candidate Theses

## Thesis A — Knowledge Route Optimizer

### المشكلة

الفرق تستخدم RAG أو GraphRAG أو long-context بالحدس.

### الأطروحة

> أداة تختار أرخص مسار معرفة مناسب لكل query: cache, vector, graph, long-context, agentic search, web.

### MVP

Input:

- corpus
- eval questions
- route configs

Output:

- route performance
- cost/latency
- recommended routing policy

### لماذا قوي؟

يجمع Cheap Genius + RAG/Knowledge.

---

## Thesis B — Evidence Grounding Layer

### المشكلة

RAG systems تجيب مصادر، لكن لا تثبت أن claim مدعوم فعلاً.

### الأطروحة

> طبقة تحول retrieval إلى evidence judgment: claim ↔ source support.

### MVP

- extract claim
- retrieve candidate sources
- classify support/contradict/irrelevant
- output evidence table

### يندمج مع

Citation Integrity Engine.

---

## Thesis C — Private Knowledge RAG for Documents

### المشكلة

المؤسسات لديها وثائق حساسة ولا تريد إرسالها كلها للسحابة.

### الأطروحة

> RAG محلي/هجين: local embedding + local SLM extraction + cloud escalation فقط للحالات الصعبة.

### MVP

- local corpus ingestion
- local search
- local answer/extraction
- confidence/escalation

### يندمج مع

Private Document Extraction SLM.

---

## Thesis D — RAG Failure Profiler

### المشكلة

عندما RAG يخطئ، لا نعرف السبب:

- retrieval miss
- chunking error
- context overload
- generator hallucination
- citation mismatch
- stale data

### الأطروحة

> trace-level profiler يصنف فشل RAG.

### MVP

Run RAG queries → log retrieved docs → classify failure.

---

## Thesis E — Living Knowledge Graph for Research Domains

### المشكلة

الباحثون يحتاجون خرائط علاقات بين papers, claims, methods, datasets, contradictions.

### الأطروحة

> يبني graph ديناميكي من الأدبيات مع provenance وثقة، لا مجرد embeddings.

### MVP

مجال ضيق واحد:

- LLM evaluation papers
- أو drug repurposing
- أو AI agents reliability

### المخاطر

بناء graph صحيح صعب، لكن قد يكون moat كبير.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Knowledge Route Optimizer | 4 | 5 | 4 | 4 | 4 | 21 |
| Evidence Grounding Layer | 5 | 4 | 4 | 5 | 4 | 22 |
| Private Knowledge RAG | 4 | 5 | 4 | 5 | 4 | 22 |
| RAG Failure Profiler | 4 | 4 | 4 | 4 | 4 | 20 |
| Living Knowledge Graph | 5 | 3 | 2 | 4 | 5 | 19 |

---

# أقوى Candidates من هذا المحور

## 1. Evidence Grounding Layer

الأقوى لأنه جوهري:

> ليس retrieval، بل إثبات claim بمصدر.

## 2. Private Knowledge RAG

قوي لأنه يجمع privacy + cost + document intelligence.

## 3. Knowledge Route Optimizer

قوي جدًا كبنية تحتية، ويرتبط بـ Cheap Genius.

---

# كيف يرتبط هذا بما سبق؟

## مع Citation Integrity

Citation Integrity هو حالة خاصة من Evidence Grounding.

## مع Private Document Extraction

Private Knowledge RAG هو توسيع له.

## مع Cost-to-Quality Profiler

Knowledge Route Optimizer يحتاج profiler.

## مع Agent Cost Governor

Agentic RAG يحتاج cost governor.

---

# الخلاصة العميقة

المجال يقول لنا:

> المعرفة ليست retrieval. المعرفة هي route + evidence + provenance + cost.

وهذا يقود إلى مشروع محتمل أكبر:

# Evidence-Aware Knowledge Router

نظام يقرر:

- هل أستخدم cache؟
- هل أستخدم vector RAG؟
- هل أستخدم graph؟
- هل أستخدم web؟
- هل أستخدم long context؟
- هل المصدر يدعم claim؟
- ما تكلفة كل مسار؟

---

# القرار

نضيف إلى Top Candidates:

1. Evidence Grounding Layer
2. Private Knowledge RAG
3. Knowledge Route Optimizer

ولا نقرر بعد.
