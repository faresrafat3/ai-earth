# 🧠 منهجية تنظيم الذاكرة والمعرفة — Memory Organization Rules
# ══════════════════════════════════════════════════════════════════════
# النسخة: 1.0
# التاريخ: 2026-06-09
# الجمهور: AI Agent المكلف بتنظيم الذاكرة والمعرفة
# الغرض: كيف ننظم ونخزن ونربط ونسترجع المعرفة في AI Earth
# ══════════════════════════════════════════════════════════════════════

---

## 0. الفلسفة

> "عايز Database تسجل كل حاجة وتنظمها"
> "وما اجبر المدنفسير فواءد" — التفسير لازم يكون كامل ومفصل

الذاكرة ليست تخزين — إنها **نظام معرفي حي** يربط:
- الأوراق العلمية (Papers)
- التطوير (Dev) — ما بُني وكيف ولماذا
- التجارب (Memory) — ما حدث في كل run
- المنتج (Product) — ما نريد بناءه

---

## 1. البنية رباعية المستويات (4-Tier Memory Architecture)

### Tier 1: Working Memory (ذاكرة العمل)
```
المدة: خلال الجلسة الحالية فقط
الحجم: محدود (context window)
المحتوى: السياق الفوري — task, prompt, current generation
التخزين: in-memory (Python dict)
الآلية: MemGPT paging — عند overflow → انقل لـ Episodic
```

### Tier 2: Episodic Memory (الذاكرة الحلقية)
```
المدة: per-run + grace period
الحجم: متوسط
المحتوى: أحداث مرتبطة بزمن — runs, generations, scores, errors
التخزين: SQLite + JSON files (runs/run_N/)
الآلية: timestamp + expiry + surprise-weighted retention
```

### Tier 3: Semantic Memory (الذاكرة الدلالية)
```
المدة: دائمة
الحجم: كبير
المحتوى: حقائق — facts, concepts, relationships, paper findings
التخزين: Knowledge Graph + Vector DB
الآلية: atemporal — لا تنتهي صلاحيتها
```

### Tier 4: Procedural Memory (الذاكرة الإجرائية)
```
المدة: دائمة + متطورة
الحجم: متوسط
المحتوى: كيف نفعل الأشياء — skills, strategies, heuristics
التخزين: SKILL_ENGINE (filesystem skills/)
الآلية: performance-score + usage-count + LRU eviction
```

### تدفق البيانات بين المستويات:

```
Working (Tier 1)
    │
    │ overflow / session end
    ▼
Episodic (Tier 2)
    │
    │ consolidation (pattern extraction)
    ▼
Semantic (Tier 3) ──── Knowledge Graph
    │
    │ skill extraction from successful patterns
    ▼
Procedural (Tier 4) ──── Skill Library
```

---

## 2. Knowledge Graph Schema

### 2.1 أنواع العقد (Node Types)

```yaml
Concept:
  id: string (UUID)
  name: string
  type: "concept" | "paper" | "skill" | "tool" | "agent" | "pattern" | "anomaly"
  properties: dict
  source: string (من أين أتى — ورقة/تجربة/ملاحظة)
  created: datetime
  last_accessed: datetime
  access_count: int
  confidence: float (0-1)

Paper:
  extends: Concept
  arxiv_id: string
  score: int (0-100 per scientific_research_rules.md)
  what_we_stole: list[string]
  what_we_missed: list[string]
  integration_point: string (Layer + Component)

Skill:
  extends: Concept
  performance_score: float
  usage_count: int
  domain: string
  contract: {P, O, A, V, F}

Pattern:
  extends: Concept
  pattern_type: "winning" | "losing" | "anomaly" | "regime"
  evidence_runs: list[int]
  confidence: float
```

### 2.2 أنواع الحواف (Edge Types)

```yaml
REFERENCES:
  from: Concept → Concept
  meaning: "A يشير لـ B"
  weight: 1.0

CONTRADICTS:
  from: Concept → Concept
  meaning: "A يتناقض مع B"
  weight: 1.0
  notes: "مهم — يحتاج تحليل"

SUPERSEDES:
  from: Concept → Concept
  meaning: "A يحل محل B"
  weight: 1.0

ELABORATES:
  from: Concept → Concept
  meaning: "A يوضح B أكثر"
  weight: 0.5

DEPENDS_ON:
  from: Skill → Skill
  meaning: "A يحتاج B للعمل"
  weight: 1.0

COMPLEMENTS:
  from: Skill → Skill
  meaning: "A و B يعملان معاً بشكل أفضل"
  weight: 0.7

REDUNDANT_WITH:
  from: Skill → Skill
  meaning: "A و B يفعلان نفس الشيء — واحد يمكن إزالته"
  weight: 0.8

DERIVED_FROM:
  from: Concept → Paper
  meaning: "A مشتق من الورقة B"
  weight: 1.0
```

---

## 3. بنية مجلدات الذاكرة

```
dev/memory/
├── concepts_graph.json          ← Knowledge Graph (عقد + حواف)
├── experiences_log.json         ← سجل التجارب
├── papers_index.json            ← فهرس الأوراق
├── patterns/
│   ├── winning_patterns.json    ← ما نجح
│   ├── losing_patterns.json     ← ما فشل
│   ├── anomalies.json           ← الشذوذات
│   └── regime_transitions.json  ← تحولات النظام
├── insights/
│   ├── cross_run_insights.json  ← استنتاجات عبر الـ runs
│   ├── domain_knowledge.json    ← معرفة المجال
│   └── meta_insights.json       ← استنتاجات عن النظام نفسه
└── evolution/
    ├── learning_curve.json
    ├── cost_curve.json
    └── trajectory.json
```

---

## 4. قواعد إضافة معرفة جديدة

### Rule M1: لا معرفة بدون مصدر
```
كل concept لازم له:
  - source: "paper:arXiv:XXXX" أو "run:NN" أو "observation:F."
  - confidence: 0-1 (كم نحن متأكدون)
  - بدون المصدر = لا تُضاف
```

### Rule M2: لا تناقض بدون توثيق
```
إذا مفهوم جديد يتناقض مع مفهوم موجود:
  1. لا تحذف القديم
  2. أضف CONFLICTS_WITH edge
  3. سجّل كلاهما مع confidence
  4. سجّل التحليل في insights/
```

### Rule M3: كل pattern يُربط بأدلة
```
إذا اكتشفت pattern:
  - minimum 3 runs كدليل
  - أو ورقة بحثية تدعمه
  - أضف evidence_runs أو evidence_paper
  - بدون دليل = insight مرشح (وليس pattern مؤكد)
```

### Rule M4: التحديث دوري
```
كل N runs:
  - راجع concepts ذات access_count = 0 (قد تكون قديمة)
  - راجع edges ذات confidence < 0.5
  - ادمج concepts مكررة
  - حدّث last_accessed لكل concept مُستخدم
```

---

## 5. بروتوكول الاسترجاع (Retrieval Protocol)

### كيف نسترجع المعرفة المناسبة في الوقت المناسب؟

```yaml
intent_guided_retrieval:
  description: "لا نسترجع بالتشابه فقط — بل بالنية"
  
  steps:
    1. تحليل النية (task → what kind of knowledge needed?)
    2. تحديد النطاق (which tiers? which node types?)
    3. استرجاع أولي (BM25 + semantic hybrid)
    4. ترشيح بالرتبة (relevance + confidence + recency)
    5. تضمين السياق (walk graph for related concepts)
    6. تجميع (assemble into prompt section)

  retrieval_formula: >
    score = λ₁·relevance + λ₂·confidence + λ₃·recency + λ₄·access_count
    
    WHERE:
      λ₁ = 0.4 (التطابق أهم شيء)
      λ₂ = 0.3 (الثقة)
      λ₃ = 0.2 (الحداثة)
      λ₄ = 0.1 (الاستخدام المتكرر = مفيد)
```

---

## 6. تكامل الذاكرة مع باقي النظام

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Papers Engine  │────▶│  Semantic Mem   │────▶│  Knowledge      │
│   (Layer 6)      │     │  (Tier 3)       │     │  Graph          │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   INTENT_ENGINE │     │  Working Mem    │     │  Concept Engine │
│   (Layer 2)     │     │  (Tier 1)       │     │  (Layer 2)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Skill Engine  │◀────│  Procedural Mem │◀────│  Meta Engine    │
│   (Layer 2)     │     │  (Tier 4)       │     │  (Layer 2)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

_هذا الملف يُقرأ من أي AI Agent مكلف بتنظيم أو تخزين أو استرجاع المعرفة._
