# Discovery Round 36 — Formal Methods / Theorem Proving / Verification / Mathematical AI

## الهدف

استكشاف مجال formal verification وAI for math:

- theorem proving
- Lean/Coq/Isabelle
- autoformalization
- verified code generation
- formal specs
- proof repair
- compiler/verifier feedback loops
- hallucination-free reasoning

هذا محور عميق جدًا لأنه يقدم عكس LLM probabilistic guessing: مخرجات قابلة للتحقق آليًا.

---

# Online Round — مصادر واتجاهات

## 1. Lean 4 Auto-Formalized Mathematics Breakthroughs

الرابط: https://www.cs.virginia.edu/~rmw7my/Courses/AgenticAISpring2026/Major%20Breakthroughs%20in%20Lean%204-Based%20Auto-Formalized%20Mathematics.html

يعرض تقدم كبير في Lean 4 theorem proving، مع أنظمة تحقق أداء عالي في MiniF2F وIMO-style benchmarks. الفكرة المركزية:

> عندما يخرج النظام proof في Lean، لا يحتاج الإنسان لفحصه يدويًا؛ Lean يتحقق.

**الأثر:** formal verification يحول “الثقة” من judge إلى proof checker.

---

## 2. Prover Agent

الرابط: https://arxiv.org/abs/2506.19923

Agent يجمع informal reasoning LLM + formal prover + Lean feedback + auxiliary lemmas.

يحقق 88.1% على MiniF2F.

**الأثر:** agents + verifier feedback يمكن أن تكون قوية عندما verifier حتمي.

---

## 3. ArXivLean / MathArena

الرابط: https://matharena.ai/arxivlean/

Benchmark جديد يأخذ theorem-like statements من arXiv حديث، ويطلب Lean proofs. كل النماذج أقل من 20% على research-level math.

**الأثر:** benchmarks القديمة تتشبع، لكن research-level formal math ما زال صعبًا جدًا.

---

## 4. Vericoding Benchmark

الرابط: https://arxiv.org/pdf/2509.22908

Benchmark لـ formally verified program synthesis. يربط code generation بالـ formal specs/proofs.

**الأثر:** مستقبل code agents قد يكون “verified code”، لا فقط tests.

---

## 5. Autoformalization Survey

الرابط: https://arxiv.org/html/2505.23486v1

Survey عن autoformalization في عصر LLMs. يغطي:

- DeepSeek-Prover
- LeanDojo
- ProofNet
- Lean Workbook
- Goedel-Prover
- BFS-Prover
- Kimina-Prover

**الأثر:** مجال سريع التطور حول تحويل الرياضيات الطبيعية إلى formal statements/proofs.

---

## 6. APOLLO

الرابط: https://arxiv.org/html/2505.05758v5

نظام proof repair يجمع LLM + Lean compiler + agents + solvers. يحقق تحسينات كبيرة بتكلفة sampling أقل.

**الأثر:** هذا بالضبط نموذج “LLM يولد، verifier يصلح/يرشد”.

---

## 7. Pipeline for verifying LLM-generated math solutions

الرابط: https://arxiv.org/html/2602.20770

Pipeline يستخدم Solver LLM + Translator LLM + Prover LLM + Lean للتحقق من حلول رياضية.

**الأثر:** يمكن استخدام proof assistants لتقييم reasoning quality، لا final answer فقط.

---

## 8. Lean4 competitive edge

الرابط: https://venturebeat.com/ai/lean4-how-the-theorem-prover-works-and-why-its-the-new-competitive-edge-in

يوضح اتجاه startup ecosystem حول Lean4 وverified code/hallucination-free AI.

**الأثر:** formal methods قد تصبح بنية ثقة تجارية.

---

# Offline Audit

## ما الحقيقي؟

1. formal proof checking يعطي ground truth قوي جدًا.
2. LLMs تتحسن بسرعة عندما تتلقى feedback من verifier.
3. theorem proving benchmarks القديمة تتشبع، لكن research-level لا يزال صعبًا.
4. verified code generation مجال ناشئ ومهم.
5. formalization itself bottleneck كبير.
6. استخدام Lean/Coq يحتاج خبرة ومكتبات.

## ما الـ hype؟

1. “hallucination-free AI” لكل المجالات.
2. كل reasoning يمكن formalize بسهولة.
3. proof assistant يغني عن domain experts.
4. verified code جاهز للإنتاج العام الآن.
5. formal methods رخيصة دائمًا؛ قد تكون مكلفة معرفيًا.

---

# التحليل العميق

## 1. هذا أقوى مجال للـ verifier الحقيقي

في معظم مجالاتنا، verifier ضعيف أو LLM-as-judge.

هنا verifier حتمي:

```text
Lean accepts / rejects
```

هذا يجعل المجال مثاليًا لـ:

- generation
- repair
- search
- feedback loops
- data flywheel

## 2. formal methods تعطي pattern عام

النمط:

```text
natural language spec → formal spec → candidate proof/code → verifier feedback → repair → certified output
```

هذا pattern يمكن نقله إلى مجالات أخرى:

- policy-to-control
- SOP-to-workflow
- contract playbook
- compliance rules
- tests for code

## 3. Autoformalization هي bottleneck

أصعب شيء ليس proof فقط، بل:

> هل صغنا الشيء الصحيح رسميًا؟

هذا يشبه كل محاورنا:

- تحويل القانون إلى obligations.
- تحويل SOP إلى workflow.
- تحويل claim إلى evidence query.

## 4. Formal verification يوضح حدود “evidence”

Evidence grounding يقول: المصدر يدعم claim.
Formal verification يقول: البرهان يثبت theorem.

الأول احتمالي/تفسيري.
الثاني حتمي/منطقي.

قد نحتاج spectrum:

```text
citation support < tests < formal proof
```

---

# Candidate Theses

## Thesis A — Natural Language to Formal Checklist / Spec

### المشكلة

معظم القواعد والسياسات مكتوبة بلغة طبيعية.

### الأطروحة

> تحويل نصوص طبيعية إلى specs/checklists شبه رسمية قابلة للتحقق.

### MVP

- SOP/policy text
- extract formal-ish rules
- validate examples

### يربط formal methods بـ policy/workflow.

---

## Thesis B — Verified Workflow Compiler

### المشكلة

workflows المستخرجة من SOPs أو policies قد تحتوي تناقضات أو missing steps.

### الأطروحة

> compile workflow إلى state machine/checkable rules، واكشف unreachable states, missing approvals, contradictions.

### MVP

- workflow JSON
- rules
- checker
- report

### قوي جدًا كامتداد لـ Policy-to-Workflow Mapper.

---

## Thesis C — LLM Output Formalization Auditor

### المشكلة

LLM outputs تحتوي claims لا يمكن التحقق منها بسهولة.

### الأطروحة

> يحاول تحويل claim إلى شكل قابل للتحقق: equation, rule, test, query, proof obligation.

### MVP

- claim in
- classify verification type
- generate test/check/query

### عميق جدًا.

---

## Thesis D — Verified Code Patch Assistant

### المشكلة

coding agents تمر tests لكنها قد تظل غير صحيحة.

### الأطروحة

> يضيف spec/proof/test obligations للكود المولد، بدل الاعتماد على unit tests فقط.

### MVP

- Python function + docstring
- generate property tests or simple formal spec
- run verifier/tests

### عملي أكثر من Lean الكامل.

---

## Thesis E — Formal Reasoning Gym

### المشكلة

تعلم التفكير الصارم صعب.

### الأطروحة

> تدريب على تحويل أفكار طبيعية إلى formal statements/proofs/checks.

### يندمج مع Research Thinking Gym.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|
| NL to Formal Checklist/Spec | 5 | 4 | 3 | 4 | 5 | 21 |
| Verified Workflow Compiler | 5 | 5 | 4 | 5 | 5 | 24 |
| LLM Output Formalization Auditor | 5 | 4 | 3 | 4 | 5 | 21 |
| Verified Code Patch Assistant | 5 | 4 | 3 | 5 | 4 | 21 |
| Formal Reasoning Gym | 5 | 4 | 4 | 4 | 4 | 21 |

---

# أقوى Candidate

# Verified Workflow Compiler

## لماذا؟

لأنه يربط formal methods بمجالاتنا العملية.

بدل theorem proving عام، نستخدم formal-ish verification للتحقق من workflows:

- هل كل خطوة لها owner؟
- هل يوجد approval قبل action خطير؟
- هل هناك path بدون evidence؟
- هل deadlines متناقضة؟
- هل loop لا ينتهي؟

هذا قابل للبناء أكثر من proving IMO theorem.

---

# علاقة هذا بباقي المحاور

## مع Policy-to-Workflow

الخطوة التالية الطبيعية: تحقق من workflow.

## مع SOP-to-Workflow

تحويل SOP إلى workflow ثم check consistency.

## مع Agent Security

تحقق من permissions/approval paths.

## مع Software Engineering

verified code/tests.

## مع Learning

formal reasoning training.

---

# الخلاصة العميقة

Formal Methods يقول لنا:

> الثقة العالية تأتي عندما نستطيع تحويل نص إلى شيء قابل للتحقق آليًا.

الصيغة:

```text
natural language → formal-ish representation → checker/verifier → repair loop
```

وهذا قد يكون missing layer في Evidence OS.

---

# Candidates مضافة

نضيف إلى Top Candidates:

1. Verified Workflow Compiler
2. Natural Language to Formal Checklist/Spec
3. LLM Output Formalization Auditor
4. Verified Code Patch Assistant

ولا نقرر بعد.
