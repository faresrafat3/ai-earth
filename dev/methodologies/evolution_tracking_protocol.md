# 📊 بروتوكول تتبع التطور — Evolution Tracking Protocol
# ══════════════════════════════════════════════════════════════════════
# النسخة: 1.0
# التاريخ: 2026-06-09
# الجمهور: AI Agent المكلف بتتبع وتحليل التطور
# الغرض: كيف نقيس ونراقب ونحلل تطور النظام عبر الزمن
# ══════════════════════════════════════════════════════════════════════

---

## 0. الفلسفة

> "منحنيات وإبعاد ومحاور تطور الفكره بالكامل"

التطور ليس رقم واحد — إنه **منحنى متعدد الأبعاد** عبر **محاور متعددة**.

```
┌─────────────────────────────────────────────────┐
│           EVOLUTION SPACE                        │
│                                                  │
│  Axis 1: Task Complexity (بسيط ← مركب)          │
│  Axis 2: Output Quality (ضعيف ← ممتاز)          │
│  Axis 3: System Capability (محدود ← شامل)       │
│  Axis 4: Cost Efficiency (مكلف ← اقتصادي)       │
│  Axis 5: Autonomy Level ( supervised ← autonomous)│
│  Axis 6: Knowledge Depth ( سطحي ← عميق)         │
│                                                  │
│  كل run = نقطة في هذا الفضاء                     │
│  التطور = حركة النقاط عبر الزمن                  │
└─────────────────────────────────────────────────┘
```

---

## 1. المحاور الثلاثة الرئيسية (The 3 Evolution Axes)

### 1.1 Task Evolution (تطور المهام)

كيف تتغير طبيعة المهام التي يتعامل معها النظام مع الوقت؟

```yaml
metrics:
  - name: task_complexity_score
    type: float (0-100)
    source: INTENT_ENGINE (goal_spec.json → num_sub_goals × avg_depth)
    direction: INCREASING (نريد تعقيد أكبر)
    frequency: per run

  - name: task_scope_breadth
    type: categorical [narrow, medium, broad, open-ended]
    source: INTENT_ENGINE (scope field)
    direction: BROADENING
    frequency: per run

  - name: task_domain_diversity
    type: int (unique domains)
    source: goal_spec.json (domain fields)
    direction: INCREASING
    frequency: per run

  - name: task_success_rate_by_complexity
    type: float (0-1)
    source: CRITIC_ENGINE (overall_score > 70 = success)
    direction: STABLE_OR_INCREASING
    frequency: per run

signals:
  GRADUATION: "when task_success_rate > 80% for 5 consecutive runs at current complexity → system ready for harder tasks"
  PLATEAU: "when task_success_rate flat for 10 runs → need new capabilities"
  REGRESSION: "when task_success_rate drops 15%+ → investigate (regime change)"
```

### 1.2 Output Evolution (تطور المخرجات)

كيف يتحسن جودة المخرجات مع الوقت؟

```yaml
metrics:
  - name: overall_score_trajectory
    type: list[float]
    source: CRITIC_ENGINE (overall_score per gen)
    direction: INCREASING (أحادي الاتجاه أو متدرج)
    frequency: per generation

  - name: hallucination_rate_trajectory
    type: list[float]
    source: WEB_SEARCH_TOOL (evidence_log.json)
    direction: DECREASING
    frequency: per generation

  - name: evidence_score_trajectory
    type: list[float]
    source: CRITIC_ENGINE (evidence_score)
    direction: INCREASING
    frequency: per generation

  - name: generation_convergence_speed
    type: int (gen number where score > threshold)
    source: orchestrator (first gen achieving target)
    direction: DECREASING (أقل أجيال = أسرع)
    frequency: per run

  - name: feedback_effectiveness
    type: float (score_delta / gen_delta)
    source: orchestrator (score[N+1] - score[N])
    direction: INCREASING
    frequency: per generation

signals:
  BREAKTHROUGH: "when overall_score jumps > 20 points in one gen"
  CONVERGENCE: "when score delta < 2 for 3 consecutive gens → plateau"
  DEGRADATION: "when score drops > 15 points → regime signal"
```

### 1.3 System Evolution (التطور الشامل)

كيف يتطور النظام ككل — بنيوياً وقدراتياً؟

```yaml
metrics:
  - name: skill_count
    type: int
    source: SKILL_ENGINE (library count)
    direction: INCREASING
    frequency: per run

  - name: skill_quality_avg
    type: float
    source: SKILL_ENGINE (avg performance_score across skills)
    direction: INCREASING
    frequency: per run

  - name: tool_usage_diversity
    type: int (unique tools used)
    source: TELEMETRY
    direction: INCREASING then STABILIZING
    frequency: per run

  - name: regime_stability
    type: int (runs since last regime transition)
    source: EVOLUTION_ENGINE (regime_transition_report.json)
    direction: INCREASING (استقرار أكبر)
    frequency: per run

  - name: meta_gradient_magnitude
    type: float
    source: META_ENGINE (gradient magnitude)
    direction: DECREASING (تقل → النظام يتعلم)
    frequency: per generation

  - name: knowledge_graph_nodes
    type: int
    source: KNOWLEDGE_GRAPH
    direction: INCREASING
    frequency: per run

  - name: knowledge_graph_edges
    type: int
    source: KNOWLEDGE_GRAPH
    direction: INCREASING
    frequency: per run

  - name: memory_utilization
    type: float (0-1)
    source: MEMORY_ENGINE
    direction: STABILIZING around 0.7
    frequency: per run

signals:
  CAPABILITY_GAIN: "when new skill extracted with score > 80"
  ARCHITECTURE_SHIFT: "when regime transition occurs"
  MATURITY: "when regime_stability > 10 and meta_gradient < 0.1"
  DIVERGENCE: "when knowledge_graph edges grow but scores drop"
```

---

## 2. منحنيات التطور (Evolution Curves)

### 2.1 منحنى التعلم (Learning Curve)
```
Score
  ↑
  │         ╭────────────── Maturity
  │       ╱
  │     ╱
  │   ╱      Rapid Growth
  │  ╱
  │╱ Initial Learning
  └──────────────────────────→ Runs
```

### 2.2 منحنى التكلفة (Cost Curve)
```
Cost per task
  ↑
  │╲
  │ ╲
  │  ╲
  │   ╲────── Economic Efficiency
  │
  └──────────────────────────→ Runs
```

### 2.3 منحنى التعقيد (Complexity Curve)
```
Task Complexity
  ↑
  │                    ╭──── Capability Ceiling
  │               ╭───╯
  │          ╭───╯
  │     ╭───╯
  │╭───╯
  │
  └──────────────────────────→ Runs
```

### 2.4 المنحنى متعدد الأبعاد (Multi-Dimensional)
```
كل run = نقطة في فضاء 6D:
  (task_complexity, output_quality, system_capability, 
   cost_efficiency, autonomy_level, knowledge_depth)
   
التتبع = سلسلة من النقاط عبر الزمن
الهدف = الحركة نحو الركن (100, 100, 100, 100, 100, 100)
```

---

## 3. بروتوكول التقرير (Reporting Protocol)

### 3.1 تقرير لكل Run

```markdown
# Evolution Report — Run N

## Summary
- Date: YYYY-MM-DD
- Task: [task_name]
- Complexity: [score]
- Final Score: [score] (Gen [N])
- Skills Used: [count]
- Cost: $[amount]

## Task Evolution
- Complexity vs previous run: [+/-/=]
- New domain explored: [yes/no]

## Output Evolution
- Score trajectory: [start] → [end] ([delta])
- Hallucination: [start] → [end]
- Convergence: Gen [N] (vs avg Gen [M])
- Feedback effectiveness: [ratio]

## System Evolution
- Skills: [count] total, [N] new
- Regime: [stable/transition]
- Meta gradient: [magnitude]
- Knowledge: [nodes] nodes, [edges] edges

## Predictions
- Next run estimated score: [range]
- Regime transition risk: [low/medium/high]
- Recommended next task type: [type]
```

### 3.2 تقرير أسبوعي (Weekly Summary)

```markdown
# Weekly Evolution Summary — Week [N]

## The Big Picture
- Runs completed: [N]
- Average score: [avg] (vs last week: [delta])
- New skills: [N]
- Regime transitions: [N]
- Total knowledge nodes: [N]

## Trends
- [Trend 1]: description
- [Trend 2]: description

## Gaps Identified
- [Gap 1]: description + recommendation
- [Gap 2]: description + recommendation

## Predictions
- Score next week: [range]
- Capability milestone: [which + when]
- Risk areas: [what + why]

## Action Items
- [ ] [Action 1]
- [ ] [Action 2]
```

---

## 4. أين تُحفظ التقارير

```
dev/insights/
├── evolution_reports/
│   ├── run_054_evolution.md          ← تقرير لكل run
│   ├── run_055_evolution.md
│   ├── week_01_summary.md            ← تقرير أسبوعي
│   ├── week_02_summary.md
│   └── curves/                       ← بيانات المنحنيات
│       ├── learning_curve.json
│       ├── cost_curve.json
│       ├── complexity_curve.json
│       └── multi_dim_trajectory.json
```

---

## 5. التنبؤ (Forecasting)

### نموذج التنبؤ البسيط (Linear Extrapolation):

```python
def predict_next_score(score_history: list[float]) -> tuple[float, float]:
    """
    Predict score range for next run.
    Uses last 5 runs for trend.
    Returns: (lower_bound, upper_bound)
    """
    if len(score_history) < 5:
        return (0.0, 100.0)  # لا بيانات كافية
    
    recent = score_history[-5:]
    trend = (recent[-1] - recent[0]) / len(recent)
    
    predicted = recent[-1] + trend
    variance = sum((s - sum(recent)/len(recent))**2 for s in recent) / len(recent)
    
    return (
        max(0, predicted - variance),
        min(100, predicted + variance)
    )
```

### إشارات التنبؤ (Prediction Signals):

| الإشارة | المعنى | الإجراء |
|---------|--------|---------|
| trend > 0 AND variance < 5 | نمو مستقر | استمر في المهام الحالية |
| trend > 0 AND variance > 15 | نمو متذبذب | حقق في الأسباب |
| trend ≈ 0 AND variance < 5 | ثبات (plateau) | جرب مهام أصعب أو مهارات جديدة |
| trend < 0 | تراجع | STOP — تحقق فوراً |
| regime_transition pending | تحول وشيك | استعد لضبط المعلمات |

---

_هذا الملف يُقرأ من أي AI Agent مكلف بتتبع أو تحليل التطور._
