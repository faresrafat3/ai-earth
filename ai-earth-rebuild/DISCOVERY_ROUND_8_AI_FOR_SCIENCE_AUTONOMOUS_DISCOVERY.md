# Discovery Round 8 — AI for Science / Autonomous Discovery

## الهدف

استكشاف مجال AI for Science بعمق، دون الوقوع في hype “AI Scientist يستبدل العلماء”.

نبحث عن:

- hypothesis generation
- literature-grounded science agents
- autonomous discovery systems
- self-driving labs
- experiment design
- evidence validation
- reproducibility
- where a small team can realistically enter

---

# Online Round — مصادر واتجاهات

## 1. Google DeepMind Co-Scientist

مصادر:

- C&EN summary: https://cen.acs.org/articles/104/web/2026/05/ai-companies-introduce-agent-based-research-tools.html
- Nature coverage / references: https://techxplore.com/news/2026-05-ai-scientific-discoveries.html

Co-Scientist هو multi-agent AI system لتوليد hypotheses، مراجعتها، ترتيبها، وتحسينها. تم توثيقه في Nature 2026 مع تطبيقات في biomedicine/drug repurposing.

**المهم:** ليس autonomous discovery كاملًا. هو hypothesis engine مع lab validation بشرية.

---

## 2. FutureHouse Robin

مصادر:

- Nature paper: https://www.nature.com/articles/s41586-026-10652-y
- C&EN: https://cen.acs.org/articles/104/web/2026/05/ai-companies-introduce-agent-based-research-tools.html

Robin نظام multi-agent للبيولوجيا التجريبية: literature agents + data analysis agents. طبّق على drug repurposing لـ dry AMD واقترح/حلل فرضيات.

**المهم:** يعمل في loop مع تجارب بشرية/مختبرية. قوته ليست اللغة فقط، بل اتصال literature + data + experiment analysis.

---

## 3. FutureHouse Platform / PaperQA2 / Agents

مصادر:

- FutureHouse platform guide: https://intuitionlabs.ai/articles/futurehouse-ai-agents-platform
- PaperQA2 announcement: https://www.linkedin.com/posts/andrewdwhite_today-futurehouse-has-released-paperqa2-activity-7239691606931488774-N9Lj

Agents:

- Crow: concise literature Q&A
- Falcon: deep literature review
- Owl: prior-work check
- Phoenix: chemistry design
- Finch: biology data analysis

**المهم:** هذه ليست مجرد chatbots. هي agents مدمجة مع scientific corpora, tools, APIs, full-text PDFs, citation graph.

---

## 4. AI Scientist v2

مصادر:

- GitHub: https://github.com/sakanaai/ai-scientist-v2
- Paper page: https://huggingface.co/papers/2504.08066

نظام end-to-end يولد hypotheses، يشغل experiments، يحلل، ويكتب paper. v2 يستخدم agentic tree search ويتخلص جزئيًا من templates.

**المهم:** قوي كمؤشر اتجاه، لكن جودة المخرجات وتكلفة التشغيل وتعميمه خارج ML domains تحتاج حذر.

---

## 5. AutoDiscovery / Asta

مصادر:

- https://allenai.org/blog/autodiscovery
- Asta coverage: https://thelettertwo.com/2025/08/26/ai2-asta-open-science-ai-framework/

AutoDiscovery يبدأ من dataset ويولد hypotheses ويكتب code لتحليلها. Asta من Ai2 يوفر agents/resources/benchmarks للبحث العلمي.

**المهم:** نقطة دخول قوية ليست “اسأل سؤالًا”، بل “اعثر على أسئلة داخل البيانات”.

---

## 6. Agentic AI for Scientific Discovery Survey

الرابط: https://arxiv.org/html/2503.08979v1

يصنف systems في literature review, experimentation, report writing, chemistry, biology, materials. يؤكد مشاكل:

- reliability
- reproducibility
- evaluation metrics
- ethical governance

---

## 7. Survey of AI Scientists

الرابط: https://arxiv.org/html/2510.23045v3

يركز على AI scientists كأنظمة تنفذ مراحل من scientific method. يوضح أن chemistry/materials أكثر نضجًا بسبب:

- structured representations
- clear experimental procedures
- self-driving labs

---

## 8. Self-Driving Laboratory 2.0

الرابط: https://pubs.rsc.org/en/content/articlehtml/2026/mh/d5mh01984b

يرسم رؤية SDL 2.0:

- interoperable
- collaborative
- generalizable
- orchestrated
- safe
- creative

يتناول Bayesian optimization, computer vision, LLMs, orchestration software.

**المهم:** autonomous discovery الحقيقي يحتاج hardware + data + optimization + safety، لا LLM وحده.

---

## 9. Low-Cost / Frugal Self-Driving Lab

الرابط: https://arxiv.org/html/2509.05351v1

يعرض “frugal twin” self-driving lab منخفض التكلفة لتحسين LCST للبوليمرات باستخدام robotic fluid handling + sensors + Bayesian optimization.

**المهم:** هناك مسار “cheap science automation”، وليس فقط مختبرات ضخمة.

---

## 10. AI Materials Discovery / SDLs

مصادر:

- https://www.oaepublish.com/articles/cs.2025.66
- https://www.sciencedaily.com/releases/2025/07/250714052105.htm
- https://www.emergentmind.com/topics/self-driving-laboratories

الاتجاه: active learning / Bayesian optimization / robotics / high-throughput characterization.

---

# Offline Audit

## ما الحقيقي؟

1. AI for Science يتقدم فعلاً في biology, chemistry, materials, simulation.
2. أكثر المناطق نضجًا هي التي لديها:
   - structured data
   - simulators أو experiments قابلة للتقييم
   - clear objective functions
   - tools/APIs
3. LLMs وحدها لا تكفي؛ القيمة في workflow + tools + validation.
4. Hypothesis generation مفيد، لكنه لا يساوي discovery إلا مع validation.
5. Self-driving labs قوية لكنها hardware-heavy.
6. Literature grounding وprior-work checking عنق زجاجة متكرر.
7. Reproducibility/provenance أساسي.

## ما الـ hype؟

1. “AI Scientist fully autonomous” في أغلب الحالات مبالغ فيه.
2. AI-generated paper acceptance لا يعني science قوي.
3. Drug repurposing hits ليست clinical success.
4. Hypothesis plausible لا يعني novel أو true.
5. Autonomous labs ليست accessible لمعظم الأفراد بدون hardware.

---

# التحليل العميق

## 1. AI for Science ينقسم إلى 3 مستويات

### Level 1 — Knowledge/Literature Intelligence

- search
- prior work
- citation/evidence
- claim maps
- hypothesis context

مناسب جدًا لفرد/فريق صغير.

### Level 2 — Computational Research Agents

- code generation
- simulation
- dataset analysis
- hypothesis testing in silico
- report generation

ممكن لفرد/فريق صغير إذا المجال computational.

### Level 3 — Wet/Physical Autonomous Discovery

- robotics
- self-driving labs
- experimental execution
- sensors
- Bayesian optimization

قوي جدًا لكنه يحتاج capital/lab partnerships.

## 2. فرصة الفرد ليست بناء Co-Scientist كامل

Google/FutureHouse لديهم:

- corpora
- infrastructure
- domain experts
- labs
- compute
- funding

الفرد لا ينافسهم في “AI scientist كامل”.

لكن يمكنه بناء:

- evidence layer
- prior-work checker
- hypothesis evaluator
- reproducibility checker
- data hypothesis miner
- local computational agent for narrow domains

## 3. Hypothesis generation وحدها ضعيفة

المشكلة ليست توليد 100 فرضية.

المشكلة:

- هل جديدة؟
- هل قابلة للاختبار؟
- هل plausible؟
- هل supported by evidence؟
- هل تخالف known constraints؟
- هل هناك cheap validation path؟

إذن candidate أقوى:

> Hypothesis Triage Engine

لا يولد فقط، بل يفلتر ويصنف ويحدد مسار تحقق.

## 4. AI for Science يحتاج Value of Experiment

في self-driving labs، القرار الحقيقي:

> أي تجربة تالية تعطي أعلى information gain مقابل cost؟

هذا يعيدنا إلى Value of Information وBayesian optimization.

قد نستورد هذا لمجالات غير مختبرية:

- أي source أقرأ؟
- أي تجربة كود أشغل؟
- أي نموذج أقارن؟
- أي hypothesis تستحق وقتي؟

---

# Candidate Theses

## Thesis A — Hypothesis Triage Engine

### المشكلة

AI يستطيع توليد فرضيات كثيرة، لكن الباحث يحتاج ترتيبها حسب:

- novelty
- plausibility
- evidence support
- testability
- cost of validation
- risk

### الأطروحة

> أداة لا تولد فرضيات فقط، بل تفرزها إلى: worth testing / weak / already known / unsupported / too expensive.

### MVP

Input:

- research question
- candidate hypotheses

Output:

- novelty check
- evidence map
- contradictions
- validation path
- cost estimate

### لماذا قوي؟

يقف بين Evidence Engine وAI Scientist.

---

## Thesis B — Prior-Work / Novelty Checker

### المشكلة

قبل أي فكرة علمية أو startup idea، السؤال:

> هل هذا اتعمل قبل كده؟

### الأطروحة

> agent يبحث في الأدبيات والبراءات وGitHub ويخرج: known / partially known / novel angle.

### MVP

Query → search papers/patents/repos → novelty report.

### قوي لأنه

- واضح.
- مفيد للباحثين والمؤسسين.
- يمكن بناؤه فوق Serper/Firecrawl/Semantic Scholar.

---

## Thesis C — Reproducibility & Experiment Auditor

### المشكلة

أوراق كثيرة لا يمكن إعادة إنتاجها، وAI-generated research يزيد المشكلة.

### الأطروحة

> أداة تفحص paper/repo وتحدد: هل التجربة قابلة للتكرار؟ ما missing details؟ هل الكود/البيانات/الإعدادات موجودة؟

### MVP

Input: paper + repo.  
Output: reproducibility checklist + risk score.

### لماذا قوي؟

يتصل بالـ peer review والـ AI scientist outputs.

---

## Thesis D — Dataset-to-Hypotheses Miner

### المشكلة

البيانات تحتوي أسئلة لم يسألها الباحث.

### الأطروحة

> أداة تبدأ من dataset، تولد hypotheses، تشغل تحليلات، وتنتج ranked findings.

### قريب من AutoDiscovery.

### MVP

CSV dataset → auto EDA → hypotheses → tests → report.

### المخاطر

منافسة Asta/AutoDiscovery، وصعوبة ضمان عدم p-hacking.

---

## Thesis E — Computational Micro-Scientist for Narrow Domains

### المشكلة

بعض المجالات computational يمكن أتمتتها بدون lab.

### الأطروحة

> agent متخصص في مجال ضيق جدًا، يشغل simulations/experiments code ويبحث عن improvements.

أمثلة:

- prompt optimization research
- small ML experiments
- algorithm benchmarks
- trading strategy research
- materials simulation toy domains

### المخاطر

قد يتحول إلى AI Scientist مصغر ومكلف.

---

## Thesis F — Experiment Value Optimizer

### المشكلة

الباحث لا يعرف أي تجربة أو قراءة أو تحليل التالي يستحق الوقت.

### الأطروحة

> يستخدم Value of Information لترتيب التجارب/المصادر/التحليلات حسب expected knowledge gain per cost.

### هذا أعمق وأكثر فلسفية، لكنه قد يكون صعب MVP.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| Hypothesis Triage Engine | 5 | 4 | 4 | 5 | 4 | 22 |
| Prior-Work / Novelty Checker | 4 | 4 | 5 | 5 | 3 | 21 |
| Reproducibility Auditor | 4 | 4 | 4 | 4 | 4 | 20 |
| Dataset-to-Hypotheses Miner | 5 | 4 | 3 | 4 | 4 | 20 |
| Computational Micro-Scientist | 5 | 3 | 2 | 3 | 4 | 17 |
| Experiment Value Optimizer | 5 | 5 | 2 | 3 | 5 | 20 |

---

# أقوى Candidates من هذا المحور

## 1. Hypothesis Triage Engine

أقوى من hypothesis generator.

الفكرة:

> لا نولّد أفكارًا فقط؛ نقرر أيها يستحق الاختبار.

## 2. Prior-Work / Novelty Checker

Wedge قوي جدًا، قريب من FutureHouse Owl.

## 3. Reproducibility Auditor

مهم جدًا في عالم AI-generated science.

---

# علاقة هذا بباقي المحاور

## مع Citation Integrity

Hypothesis triage يحتاج citation/evidence integrity.

## مع Evidence Grounding

كل hypothesis يجب أن تربط بأدلة وموانع.

## مع Cost Routing

اختيار hypothesis هو routing معرفي:

> أي فكرة تستحق تكلفة التحقق؟

## مع Personal Research Memory

Research memory يحفظ hypotheses والقرارات وسبب رفضها.

---

# الخلاصة العميقة

AI for Science يقول لنا:

> القيمة ليست في توليد مزيد من الأفكار، بل في اختيار الأفكار القابلة للتحقق ذات أعلى قيمة معلوماتية.

وهذا يعيدنا إلى مبدأ عام:

# Intelligence = Search + Triage + Validation under Cost

أي ذكاء عملي ليس توليدًا فقط، بل:

1. مساحة احتمالات.
2. فلترة.
3. ترتيب حسب قيمة.
4. تحقق.
5. تحديث معرفة.

---

# Candidate مضاف

نضيف إلى Top Candidates:

1. Hypothesis Triage Engine
2. Prior-Work / Novelty Checker
3. Reproducibility Auditor

ولا نقرر بعد.
