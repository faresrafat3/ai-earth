# Discovery Round 13 — AI for Software Engineering / Coding Agents / DevTools

## الهدف

استكشاف مجال AI software engineering:

- coding agents
- SWE-bench / TerminalBench
- code review agents
- test generation
- CI/CD agents
- repo understanding
- codebase memory
- developer workflow automation

هذا محور مهم لأنه من أسرع المجالات إنتاجًا وقابلية للقياس: الكود يمكن تشغيله واختباره.

---

# Online Round — مصادر واتجاهات

## 1. Coding Agent Benchmarks 2026

الرابط: https://presenc.ai/research/coding-agent-benchmarks-2026

يوضح أن SWE-bench Verified يقترب من saturation، بينما real-world PR acceptance أقل بكثير بسبب conventions وimplicit requirements.

**الأثر:** benchmark score لا يساوي productivity في repo حقيقي.

---

## 2. SWE-Bench Atlas / Auto-SWE-Bench

الرابط: https://openreview.net/forum?id=Gxw1EDSm9S

إطار لتوليد مهام SWE-bench-like تلقائيًا من GitHub PRs، متعددة اللغات، مع dockerization وtest oracle extraction.

**الأثر:** evaluation في software engineering يتجه إلى dynamic, live, reproducible tasks.

---

## 3. Beyond SWE-Bench / TerminalBench

مصادر:

- https://www.birjob.com/blog/agent-benchmarks-2026
- https://www.codesota.com/agentic

توضح أن SWE-bench قد يعطي false confidence، وأن TerminalBench/real PR metrics أصعب وأقرب للعمل الحقيقي.

**الأثر:** نحتاج evals خاصة بالrepo/workflow لا leaderboards عامة.

---

## 4. Code Review Agent Benchmark

الرابط: https://arxiv.org/html/2603.23448v1

Benchmark لوكلاء code review، يوضح أن human review comments noisy وغير كافية كـ ground truth، وأن repo-level/test-based evaluation أفضل.

**الأثر:** code review AI يحتاج verifiable test/oracle، لا similarity to human comments فقط.

---

## 5. Code-as-Agent Harness Papers

الرابط: https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers

قائمة عن code as interface للـ agents:

- SWE-bench
- SWE-lancer
- Terminal-Bench
- AppWorld
- τ-bench
- code execution traces

**الأثر:** الكود يجعل reasoning executable/verifiable، وهذا يتوافق مع فلسفتنا evaluation-first.

---

## 6. Coding Agent Leaderboards 2026

مصادر:

- https://www.codesota.com/code-generation
- https://www.morphllm.com/best-ai-model-for-coding
- https://www.marktechpost.com/2026/05/15/best-ai-agents-for-software-development-ranked-a-benchmark-driven-look-at-the-current-field/

توضح أن:

- frontier coding agents قوية جدًا.
- scaffold/model/pricing يغير الأداء.
- real-world utility تختلف عن benchmark.

---

# Offline Audit

## ما الحقيقي؟

1. coding agents مفيدة فعليًا الآن.
2. software بيئة مثالية للـ AI لأنها قابلة للاختبار.
3. benchmarks العامة بدأت تتشبع.
4. real repo conventions هي bottleneck.
5. CI/tests هي verifier قوي.
6. code review/test generation/maintenance tasks أكثر واقعية من “agent يبني مشروع كامل”.

## ما الـ hype؟

1. “AI developer مستقل بالكامل”.
2. SWE-bench = حل software engineering.
3. code review similarity = review quality.
4. generating code without tests = productivity.
5. multi-agent coding teams غالبًا cost explosion.

---

# التحليل العميق

## 1. البرمجة أقوى مجال للتقييم الحتمي

في معظم مجالات AI، نحتاج LLM judge.
في البرمجة، لدينا:

- tests
- type checks
- linters
- build
- runtime
- CI

هذا يجعل software مجال ممتاز لـ Cheap Genius + Evaluation.

## 2. الفجوة ليست كتابة الكود، بل قبول الـ PR

الـ agent قد يكتب كودًا ينجح في tests، لكنه لا يطابق:

- style
- architecture
- internal patterns
- maintainability
- security
- reviewer expectations

إذن المجال يحتاج:

> repo-specific coding intelligence

## 3. codebase memory/context هو bottleneck

الـ agent يحتاج:

- conventions
- prior decisions
- architecture map
- test strategy
- dependency graph
- owner preferences

هذا يربط المحور بـ Personal/Project Memory.

## 4. أفضل مدخل ليس بناء coding agent كامل

السوق مزدحم:

- Cursor
- Claude Code
- Codex
- Copilot
- Devin
- Aider
- Cline
- OpenHands

الفرد لا ينافسهم مباشرة.

لكن يمكن بناء:

- repo-specific evaluation harness
- PR acceptance predictor
- code review auditor
- test gap generator
- coding agent cost profiler
- failure-to-data flywheel

---

# Candidate Theses

## Thesis A — Repo-Specific Agent Eval Harness

### المشكلة

الفرق لا تعرف هل coding agent يصلح لـ repo الخاص بها.

### الأطروحة

> أداة تولد/تجمع مهام من تاريخ repo، وتشغل agents عليها، وتقيس pass/fail/cost/PR-readiness.

### MVP

- ingest GitHub repo
- mine old PRs/issues
- create replay tasks
- run candidate agents/models
- report Pareto frontier

### لماذا قوي؟

يشبه SWE-Bench Atlas لكن للاستخدام الخاص.

---

## Thesis B — PR Acceptance Predictor / Reviewer Simulator

### المشكلة

الكود قد يمر tests لكن يرفضه reviewer.

### الأطروحة

> يتعلم من تاريخ reviews في repo ويتنبأ: هل هذا PR سيُقبل؟ وما الأسباب؟

### MVP

- collect past PRs/reviews
- classify review categories
- evaluate new patch
- output risk report

### المخاطر

يحتاج بيانات repo كافية.

---

## Thesis C — Test Gap Generator

### المشكلة

الـ agents تستغل ضعف tests أو تمرر حلولًا سطحية.

### الأطروحة

> أداة تولد tests إضافية لكشف semantic bugs أو overfitting to tests.

### MVP

- input patch/function
- generate adversarial tests
- run tests
- report uncovered failures

### قوي جدًا لأن tests verifier حتمي.

---

## Thesis D — Coding Agent Cost Profiler

### المشكلة

الفرق لا تعرف أي agent/model/scaffold أرخص كافي لمهامها.

### الأطروحة

> profiler يشغل نفس tasks عبر Claude Code/Codex/Aider/OpenHands/etc ويقارن accuracy/cost/latency.

### MVP

routes config + repo tasks → Pareto frontier.

### يندمج مع Cost-to-Quality Profiler.

---

## Thesis E — Codebase Memory / CLAUDE.md Generator

### المشكلة

agents تحتاج context عن repo conventions.

### الأطروحة

> أداة تولد وتحافظ على project memory: architecture, conventions, commands, testing, pitfalls.

### MVP

- scan repo
- generate AGENTS.md / CLAUDE.md
- update from PR history
- check staleness

### قوي لأنه يحسن كل coding agents بدل منافستها.

---

## Thesis F — Code Review Agent Auditor

### المشكلة

AI code reviewers قد يعلقون تعليقات سطحية أو خاطئة.

### الأطروحة

> أداة تقيم code review comments: actionable? correct? redundant? security-relevant? style-only?

### MVP

review comments + diff + tests → review quality report.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Repo-Specific Agent Eval Harness | 5 | 4 | 4 | 5 | 5 | 23 |
| PR Acceptance Predictor | 5 | 4 | 3 | 4 | 5 | 21 |
| Test Gap Generator | 5 | 5 | 4 | 5 | 4 | 23 |
| Coding Agent Cost Profiler | 4 | 5 | 4 | 4 | 3 | 20 |
| Codebase Memory Generator | 4 | 4 | 5 | 4 | 4 | 21 |
| Code Review Agent Auditor | 4 | 4 | 4 | 4 | 4 | 20 |

---

# أقوى Candidates من هذا المحور

## 1. Test Gap Generator

لأنه يستخدم verifier حقيقي: tests.

## 2. Repo-Specific Agent Eval Harness

لأنه يحل مشكلة مهمة جدًا:

> لا يهم benchmark العام؛ المهم هل agent يعمل على repo الخاص بك؟

## 3. Codebase Memory Generator

لأنه يحسن كل coding agents بدل منافستها.

---

# علاقة هذا بباقي المحاور

## مع Evaluation

Software يوفر ground-truth tests.

## مع Data Flywheel

كل failed patch أو review يصبح training/eval data.

## مع Cheap Genius

اختيار agent/model/scaffold حسب task/cost.

## مع Personal/Project Memory

Codebase memory هي ذاكرة مشروع.

## مع Enterprise Workflow

coding agents جزء من enterprise workflows.

---

# الخلاصة العميقة

Software engineering هو أفضل مجال لتطبيق فلسفتنا لأنه:

> outputs executable, failures observable, corrections reusable.

لكن السوق مزدحم في بناء agents.

لذلك أفضل مدخل ليس “coding agent جديد”، بل:

- eval harness
- test generation
- repo memory
- cost profiling
- review auditing

---

# Candidates مضافة

نضيف إلى Top Candidates:

1. Test Gap Generator
2. Repo-Specific Agent Eval Harness
3. Codebase Memory Generator

ولا نقرر بعد.
