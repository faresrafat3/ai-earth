# Discovery Round 2 — Agentic Systems / AI Workers

## الهدف

استكشاف مجال agents ليس من زاوية hype، بل من زاوية:

- reliability
- long-horizon execution
- memory
- tool use
- security
- cost
- workflow automation
- practical MVP opportunities

---

## Online Round — مصادر واتجاهات

## 1. Beyond pass@1: Reliability Science for Long-Horizon LLM Agents

الرابط: https://arxiv.org/html/2603.29231v1

يقدم إطار reliability science للـ long-horizon agents. أهم النتائج:

- reliability decay يختلف حسب المجال.
- capability ranking وreliability ranking قد يتباعدان.
- frontier models قد يكون لها meltdown rates أعلى لأنها تتبع استراتيجيات طموحة.
- memory scaffolds قد تضر بدل أن تساعد.

**الأثر:** لا يكفي قياس success rate؛ يجب قياس reliability over time.

---

## 2. Trustworthy Agentic AI Survey

الرابط: https://arxiv.org/html/2605.23989

يركز على safety, robustness, privacy, system security في agentic AI. يقدم metrics مثل:

- catastrophic event rate
- constraint violation rate
- trace coverage
- adversarial success rate
- interruption success rate

**الأثر:** أي agent system يحتاج runtime monitoring وprocess metrics، لا outcome فقط.

---

## 3. AgentLAB — Long-Horizon Attacks

الرابط: https://arxiv.org/abs/2602.16901

benchmark لاختبار تعرض agents لهجمات طويلة المدى:

- intent hijacking
- tool chaining
- task injection
- objective drifting
- memory poisoning

**الأثر:** agent security ليست prompt injection فقط؛ الذاكرة والهدف والتسلسل كلها attack surfaces.

---

## 4. LongMemEval-V2

الرابط: https://arxiv.org/html/2605.12493

benchmark للذاكرة طويلة المدى في agents. يوضح accuracy-latency frontier وأن memory systems قد تحسن الأداء لكنها تكلف latency كبير.

**الأثر:** memory ليست خيرًا مطلقًا؛ يجب تقييم cost/latency/accuracy.

---

## 5. Survey on Security of Long-Term Memory in LLM Agents

الرابط: https://arxiv.org/html/2604.16548v1

يركز على memory poisoning, provenance, recovery, policy. يوضح أن memory هي substrate جديد للهجوم.

**الأثر:** أي نظام agent بذاكرة يحتاج memory governance.

---

## 6. Production agent trend analyses

مصادر غير أكاديمية لكنها تكشف السوق:

- long-horizon agents تحتاج failure recovery, token efficiency, cost control.
- الإنتاج الحقيقي ليس “full autopilot” بل workflows قابلة للتحقق.
- software agents تنجح أكثر لأن البيئة قابلة للاختبار.

---

# Offline Audit

## ما الحقيقي هنا؟

1. agents تدخل الإنتاج فعلًا في coding, support, internal workflows.
2. أكبر مشكلة ليست القدرة فقط، بل reliability over long horizon.
3. التكلفة والانفجار في tokens مشكلة مركزية.
4. الذاكرة مفيدة لكنها خطرة ومكلفة.
5. الأمن والـ prompt/memory injection غير محلولين.
6. software workflows أنسب مجال لأن outputs قابلة للاختبار.

## ما الـ hype؟

1. “full autonomous worker” حاليًا مبالغ فيه.
2. multi-agent بدون verification غالبًا يزيد التكلفة والفشل.
3. memory كحل سحري غير صحيح؛ قد تضر.
4. long-horizon benchmarks قد تخفي task variance ضخم.

---

# Candidate Theses من محور agents

## Thesis A — Agent Reliability Monitor

### المشكلة

agents تفشل في منتصف workflow، لكن المستخدم لا يعرف مبكرًا أن trajectory انحرفت.

### الأطروحة

> طبقة monitoring تسجل trajectory وتكشف مبكرًا: drift, repeated failures, tool misuse, objective change, memory contamination.

### MVP

يدخل agent trace ويخرج:

- risk score
- constraint violations
- loop detection
- tool error patterns
- unresolved subgoals
- “should interrupt?” decision

### العلم

- reliability science
- runtime monitoring
- process metrics
- anomaly detection

### لماذا قوي؟

كل agent production يحتاج monitoring.

### المخاطر

صعب بدون تكامل مع agent frameworks.

---

## Thesis B — Cheap Agent Workflow Router

### المشكلة

تشغيل agent كامل لكل task مكلف وغير ضروري.

### الأطروحة

> قبل تشغيل agent طويل، صنّف task: direct answer, simple tool call, short workflow, long agent, human-in-loop.

### MVP

Task input → route:

- no agent
- script/tool
- small agent
- large agent
- human review

### العلم

- routing/cascades
- task complexity estimation
- cost-aware inference

### لماذا قوي؟

يمزج Cheap Genius مع agents.

---

## Thesis C — Agent Memory Firewall

### المشكلة

agent memory عرضة لـ poisoning، drift، privacy leakage.

### الأطروحة

> طبقة تحكم في ما يدخل الذاكرة وما يخرج منها، مع provenance وexpiry وtrust score.

### MVP

- memory write classifier
- provenance tagging
- suspicious memory detection
- recall audit

### العلم

- memory security
- provenance
- retrieval safety

### المخاطر

قد يكون سابقًا للسوق إن لم تكن memory agents منتشرة كفاية.

---

## Thesis D — Verifiable Workflow Agent for Software Tasks

### المشكلة

agents العامة تفشل. لكن software tasks قابلة للاختبار.

### الأطروحة

> agent متخصص في مهام صغيرة قابلة للتحقق: يقرأ issue، يغيّر كود، يشغل tests، يفتح patch report.

### MVP

CLI agent محدود:

- task spec
- repo
- run tests
- patch
- report

### العلم

- tool-use agents
- verification through tests
- software reliability

### المخاطر

سوق مزدحم جدًا: Cursor, Claude Code, Codex, Devin-like tools.

---

## Thesis E — Agent Cost Governor

### المشكلة

agents تستهلك tokens بلا سقف واضح.

### الأطروحة

> runtime layer يفرض ميزانية، يوقف loops، يختار موديلات أرخص، ويطلب إذن عند تجاوز expected value.

### MVP

- wrapper حول agent calls
- budget meter
- loop detector
- escalation/stop rules
- cost per subgoal

### العلم

- cost-aware inference
- value of information
- runtime control

### قوي لأنه

قريب من Cheap Genius، ويدخل أي agent framework.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Agent Reliability Monitor | 4 | 4 | 3 | 5 | 4 | 20 |
| Cheap Agent Workflow Router | 4 | 5 | 4 | 4 | 3 | 20 |
| Agent Memory Firewall | 4 | 3 | 3 | 4 | 4 | 18 |
| Verifiable Software Agent | 4 | 3 | 3 | 5 | 2 | 17 |
| Agent Cost Governor | 4 | 5 | 5 | 4 | 3 | 21 |

---

# أقوى candidate من محور agents

# Agent Cost Governor

لأنه:

- واضح ومؤلم.
- MVP سريع.
- يناسب مواردنا.
- يركب فوق أي agent framework.
- يتماشى مع Cheap Genius.
- لا يحتاج بناء agent كامل.

## الفكرة

بدل بناء agent جديد، نبني:

> طبقة تتحكم في تكلفة وسلوك agents الموجودة.

تسجل:

- token spend
- retries
- loops
- tool failures
- subgoal progress
- escalation decisions

وتقرر:

- continue
- stop
- downgrade model
- escalate model
- ask human

---

# مقارنة مع محور AI for Research

## Citation Integrity Engine

قوي لأنه wedge محدد في البحث العلمي.

## Agent Cost Governor

قوي لأنه infrastructure عام فوق agents.

الفرق:

| الفكرة | نطاق | MVP | سوق |
|---|---|---|---|
| Citation Integrity | بحث علمي | واضح | أكاديمي/ناشرين |
| Agent Cost Governor | كل agents | أسرع | أوسع |

---

# القرار

محور agents أعطى candidate قوي جدًا:

> Agent Cost Governor

لكنه لا يلغي Citation Integrity. بل قد يندمجان لاحقًا:

- Research agent يحتاج Citation Integrity.
- وكل agent يحتاج Cost Governor.

نضيفه إلى Top Candidates.
