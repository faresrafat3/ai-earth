# Discovery Round 9 — Multimodal / World Models / Robotics / Embodied AI

## الهدف

استكشاف مجال الذكاء المتجسد والعالمي:

- multimodal foundation models
- vision-language-action models (VLA)
- world models
- robotics foundation models
- simulation
- embodied evaluation
- physical AI infrastructure

مع سؤال عملي:

> هل يوجد مدخل مناسب لفرد/فريق صغير، أم أن المجال يحتاج رأس مال وعتاد كبير؟

---

# Online Round — مصادر واتجاهات

## 1. World Model for Robot Learning Survey

الرابط: https://arxiv.org/html/2605.00080v1

Survey شامل حتى 2026 عن world models للروبوتات. يوضح انتقال الروبوتات من task-specific policies إلى foundation-model-driven embodied intelligence. يركز على:

- world models as policies
- world models as simulators
- video/action prediction
- long-horizon reliability
- action-conditioned consistency

**الأثر:** العالم يتجه إلى نماذج تتنبأ بالمستقبل وتخطط، لا مجرد VLA reactive.

---

## 2. World Model for Robot Learning Project

الرابط: https://ntumars.github.io/wm-robot-survey/

يعرض taxonomies مهمة:

- predict-then-act
- video-action shared backbone
- expert fusion
- latent-space planning

**الأثر:** هناك فجوة بين future-frame realism وutility الفعلية للسيطرة على الروبوت.

---

## 3. VLA Models Survey

الرابط: https://arxiv.org/abs/2505.04769

Survey عن Vision-Language-Action models وتطورها من RT-1/RT-2 إلى OpenVLA وOcto وغيرها. يغطي:

- observation encoders
- reasoning backbones
- action decoders
- diffusion policies
- hierarchical architectures

**الأثر:** VLA هو “LLM + رؤية + فعل”، لكنه لا يزال يعاني من data scarcity وsim-to-real.

---

## 4. Foundation Models in Robotics

الرابط: https://arxiv.org/html/2604.15395v1

يناقش تحديات foundation models في الروبوتات:

- inference latency
- high compute cost
- lack of physical grounding
- embodiment bias
- safety risks
- interpretability

**الأثر:** robotics foundation models ليست سهلة الإنتاج، لكنها تولد احتياجات بنية تحتية ضخمة.

---

## 5. Robotic Manipulation / World Models Survey

الرابط: https://arxiv.org/html/2511.02097v2

يركز على manipulation، VLM/VLA، future scene prediction، hierarchical System 1/2 architectures.

**الأثر:** تقسيم slow reasoning vs fast action يظهر بقوة — يشبه Cheap Genius لكن في physical domain.

---

## 6. Physical AI / Robotics Companies 2026

الرابط: https://www.evsint.com/top-robotics-foundation-model-embodied-ai-companies-2026/

يرصد شركات مثل:

- Physical Intelligence
- Google DeepMind
- Skild AI
- NVIDIA GR00T
- Figure AI
- 1X
- Tesla Optimus

**الأثر:** المجال يتحول إلى ecosystem كبير، لكن الدخول المباشر لبناء model/robot صعب جدًا.

---

## 7. Embodied AI Predictions 2026

الرابط: https://dtsbourg.me/en/articles/predictions-embodied-ai

يناقش قيود deployment:

- النماذج لازم تعمل on-device أو edge.
- OpenVLA ~7B، pi0 ~3B، GR00T ~2.2B.
- الروبوت لا يستطيع حمل H100.

**الأثر:** cost/latency/edge constraints محورية.

---

## 8. Physical AI Ecosystem / Robotics Infrastructure

الرابط: https://www.etftrends.com/artificial-intelligence-content-hub/robotics-update-physical-ai-ecosystem/

يتحدث عن scaling of Physical AI وrobot foundation models كـ intelligence layer قابلة للترخيص.

**الأثر:** قد تظهر طبقات infrastructure حول robotics models، مثل eval/sim/data/monitoring.

---

## 9. Robotics/VLA Infrastructure Startups

الرابط: https://viewpoints.fov.ventures/p/10-early-stage-startups-to-watch-in-2026

يشير إلى شركات تبني platforms لتدريب ونشر VLA models، simulation/world models، safety systems.

**الأثر:** المدخل الواقعي قد يكون tooling وليس الروبوت نفسه.

---

# Offline Audit

## ما الحقيقي؟

1. الذكاء يتوسع من نص إلى multimodal/action.
2. VLA/world models مجال متسارع جدًا.
3. robotics foundation models تحتاج data, simulation, hardware, safety.
4. world models مهمة للتخطيط الطويل وتجنب reactive failures.
5. edge inference والتكلفة والlatency محورية.
6. evaluation/simulation/data tooling قد تكون فرصًا أفضل من بناء robot model.

## ما الـ hype؟

1. “humanoid robots everywhere in 2026” مبالغ فيه.
2. VLA generalization ما زالت محدودة.
3. demos لا تعني reliability في العالم الحقيقي.
4. world model video realism لا يعني usefulness للتحكم.
5. بناء robotics foundation model ليس مناسبًا لفرد/فريق صغير.

---

# التحليل العميق

## 1. المجال مغرٍ لكنه capital-intensive

بناء:

- robot hardware
- VLA model
- large robot dataset
- simulation stack
- real-world evaluation

يتطلب رأس مال وفريق وبيانات.

لذلك لا ندخل من باب “نبني روبوت”.

## 2. أين يمكن لفرد/فريق صغير الدخول؟

في طبقات:

- evaluation
- simulation tasks
- data cleaning/annotation
- failure analysis
- route selection between models
- safety/monitoring
- documentation/evidence for robot behavior
- synthetic task generation

## 3. robotics يعيد نفس أنماطنا لكن بأعلى stakes

- cost-aware inference: الروبوت لا يقدر يستخدم frontier model دائمًا.
- early stopping: القرار يجب أن يكون سريع.
- verifier: هل الفعل آمن؟
- evidence: هل perception صحيح؟
- memory: هل robot يتذكر environment؟
- observability: trace لكل action.

## 4. world models = prediction substrate

في LLMs، كنا نقيس answer distribution.
في robotics، المهم:

> future state distribution.

السؤال:

- هل النموذج يتنبأ بنتيجة الفعل؟
- هل الخطأ يتراكم؟
- هل prediction مفيد للتحكم؟

هذا يشبه EXP0/EXP13 لكن في physical trajectories.

---

# Candidate Theses

## Thesis A — Robotics/Embodied AI Evaluation Harness

### المشكلة

VLA/world model demos كثيرة، لكن تقييمها غير موحد، وخاصة من حيث:

- safety
- long-horizon consistency
- action feasibility
- cost/latency
- sim-to-real risk

### الأطروحة

> harness يقيم VLA/world model policies على tasks موحدة، ويقيس failure modes لا success فقط.

### MVP

بدون hardware:

- simulation tasks.
- compare open VLA/world model outputs إن أمكن.
- trace prediction/action failures.

### المخاطر

يتطلب access لنماذج/محاكيات.

---

## Thesis B — Embodied Task Generator & Validator

### المشكلة

تقييم الروبوتات يحتاج tasks متنوعة وقابلة للتحقق.

### الأطروحة

> توليد مهام embodied/simulated مع success criteria واضحة، لتقييم agents/robots.

### MVP

- text task → simulated environment spec.
- expected constraints.
- validation checklist.

### لماذا قوي؟

يشبه Ground-Truth Eval Generator لكن للـ embodied AI.

---

## Thesis C — Robot Action Trace Auditor

### المشكلة

عندما يفشل robot/agent، final outcome لا يكفي. نحتاج trace audit.

### الأطروحة

> أداة تحلل action traces وتحدد: perception error, planning error, action execution error, safety violation.

### MVP

يعمل على simulated traces أو logs.

### يندمج مع

Agent Reliability Monitor.

---

## Thesis D — World Model Utility Profiler

### المشكلة

world models قد تنتج فيديوهات مستقبلية جميلة لكنها غير مفيدة للتحكم.

### الأطروحة

> أداة تقيس whether predictions improve downstream planning/control، لا frame realism فقط.

### MVP

على toy/simulation tasks:

- compare policy with/without predictive model.
- measure planning success, cost, error compounding.

### عميق لكنه أصعب.

---

## Thesis E — Edge VLA Cost/Latency Profiler

### المشكلة

robotics models يجب أن تعمل ضمن قيود edge.

### الأطروحة

> profiler يقيس latency/memory/action quality لموديلات VLA/SLM على edge hardware أو simulated constraints.

### MVP

قد يبدأ كمراجعة/benchmark بدون hardware كبير.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Robotics Evaluation Harness | 4 | 3 | 2 | 4 | 4 | 17 |
| Embodied Task Generator | 4 | 4 | 3 | 4 | 4 | 19 |
| Robot Action Trace Auditor | 4 | 4 | 3 | 4 | 4 | 19 |
| World Model Utility Profiler | 5 | 3 | 2 | 4 | 5 | 19 |
| Edge VLA Cost Profiler | 3 | 5 | 3 | 3 | 3 | 17 |

---

# أقوى Candidates من هذا المحور

## 1. Embodied Task Generator & Validator

لأنه لا يتطلب روبوت حقيقي كبداية، ويتصل بالـ evaluation-first philosophy.

## 2. Robot Action Trace Auditor

لأنه امتداد طبيعي لـ agent trace auditing لكن للـ physical/action domain.

## 3. World Model Utility Profiler

عميق جدًا، لكنه أصعب وأبعد.

---

# علاقة هذا بباقي المحاور

## مع Evaluation

Embodied Task Generator هو Ground-Truth Eval Generator للروبوتات.

## مع Agent Reliability

Robot Action Trace Auditor امتداد لـ Agent Reliability Monitor.

## مع Cheap Genius

Edge constraints تجعل cost-aware routing ضروريًا.

## مع AI for Science

Self-driving labs تحتاج embodied/action workflows وتقييم traces.

---

# الخلاصة العميقة

هذا المحور يقول:

> المستقبل ليس language-only. لكن الدخول العملي ليس ببناء روبوت، بل ببناء أدوات تقييم/trace/simulation للذكاء المتجسد.

أي أن نقطة الدخول المناسبة لنا ليست:

- build VLA model
- build robot

بل:

- evaluate embodied agents
- generate tasks
- audit traces
- measure world model utility

---

# القرار

نضيف إلى Top Candidates:

1. Embodied Task Generator & Validator
2. Robot Action Trace Auditor
3. World Model Utility Profiler

ولا نقرر بعد.
