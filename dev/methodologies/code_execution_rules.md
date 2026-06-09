# ⚙️ منهجية كتابة الكود والتنفيذ — Code Execution Methodology
# ══════════════════════════════════════════════════════════════════════
# النسخة: 1.0
# التاريخ: 2026-06-09
# الجمهور: AI Agent المكلف بكتابة/تعديل كود AI Earth
# الغرض: قواعد صارمة لضمان جودة الكود والتوافق العكسي
# ══════════════════════════════════════════════════════════════════════

---

## 0. المبادئ الأساسية

```
CODE_PHILOSOPHY:
  1. "مفيش حاجة تعدي من غير test"
  2. "الـ imports القديمة تشتغل — دائماً"
  3. "كل ملف = وحدة مستقلة قابلة للاستبدال"
  4. "القرار يُسجَّل قبل الكود يُكتب"
  5. "كل مكون JSON-serializable من يومه الأول"
```

---

## 1. قبل ما تكتب سطر واحد (Pre-Flight Checklist)

### إلزامي قبل كل مهمة تنفيذ:

```
□ اقرأ dev/architecture/AI_EARTH_MASTER_BLUEPRINT.md (5 دقائق)
□ اقرأ AGENT_DEVELOPMENT_CONTEXT.md للمكون المطلوب (10 دقائق)
□ حدد: أي Layer؟ أي Component؟ أي Phase؟
□ تحقق: هل هناك ورقة بحثية مرتبطة؟ (→ dev/methodologies/scientific_research_rules.md)
□ سجّل القرار في decision_log.py (إذا كان قرار جديد)
□ تأكد: الـ imports القديمة لن تتأثر
```

---

## 2. قالب الملف القياسي (Standard File Template)

كل ملف Python في AI Earth يجب أن يبدأ بهذا الـ header:

```python
"""
[اسم المكون] — [وصف سطر واحد]

Source:
    - [اسم الورقة/المشروع] (arXiv:XXXX.XXXXX)
    - [اسم الورقة/المشروع] (arXiv:XXXX.XXXXX)

Stolen From:
    - ما أخذناه بالضبط من كل مصدر

What Was Missed:
    - ما تركناه ولماذا

GENESIS/AI Earth Adaptation:
    - كيف اختلف تطبيقنا

Usage:
    from ai_earth.capabilities.tool_hub import get_tool
    tool = get_tool("web_search")

Integration:
    - يُستدعى من: [أين]
    - يستدعي: [ماذا]
    - يُنتج: [أي artifacts]

Tests:
    tests/test_[component].py (N tests)

Decision:
    DECISION-NNN: [سبب التصميم]

Last Updated: YYYY-MM-DD
"""
```

---

## 3. قواعد الكود الإلزامية (Mandatory Code Rules)

### Rule C1: Backward Compatibility
```python
# ❌ WRONG — كسر import قديم
# (حذف genesis/tools/web_search.py)

# ✅ CORRECT — wrap القديم
# ai_earth/LEGACY_COMPAT/imports.py:
from ai_earth.capabilities.tool_hub.tools.web_search import *
# أو ai_earth/capabilities/tool_hub/tools/web_search.py يغلف القديم
```

### Rule C2: كل Component له __init__.py بنظيف API
```python
# ai_earth/capabilities/tool_hub/__init__.py

from ai_earth.capabilities.tool_hub.registry import ToolRegistry, ToolSpec
from ai_earth.capabilities.tool_hub.executor import SandboxExecutor
from ai_earth.capabilities.tool_hub.catalog import catalog, get_tool, invoke

__all__ = ['ToolRegistry', 'ToolSpec', 'SandboxExecutor', 'catalog', 'get_tool', 'invoke']
```

### Rule C3: كل Dataclass له to_dict() + from_dict()
```python
from dataclasses import dataclass, asdict

@dataclass
class ToolSpec:
    name: str
    description: str
    # ...

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ToolSpec':
        return cls(**data)
```

### Rule C4: Error Handling بـ typed exceptions
```python
class AIEarthError(Exception):
    """Base exception for AI Earth"""
    pass

class ToolNotFoundError(AIEarthError):
    pass

class BudgetExceededError(AIEarthError):
    pass

class SkillEvaluationError(AIEarthError):
    pass
```

### Rule C5: Logging منظم
```python
import logging

logger = logging.getLogger(f"ai_earth.{__name__}")

# NOT:
# print("tool not found")

# YES:
# logger.warning("Tool %s not found in registry", tool_name)
```

### Rule C6: لا API keys في الكود — أبداً
```python
# ❌ WRONG
API_KEY = "sk-or-v1-..."

# ✅ CORRECT
import os
API_KEY = os.getenv("OPENROUTER_API_KEY")
```

### Rule C7: Type hints على كل function
```python
from typing import List, Optional, Dict, Any

def search_skills(
    query: str,
    top_k: int = 5,
    domain: Optional[str] = None
) -> List[Skill]:
    ...
```

---

## 4. قواعد الاختبار (Testing Rules)

### Test Coverage Requirements

| Component | الحد الأدنى للاختبارات | النوع |
|-----------|----------------------|-------|
| Tool Hub | 35+ | Unit + Integration |
| Skill Engine | 60+ | Unit + Integration + E2E |
| Meta Engine | 40+ | Unit + Integration |
| Agent Hub | 50+ | Unit + Integration |
| Safety Engine | 25+ | Unit |
| Telemetry | 20+ | Unit |
| كل component جديد | 25+ minimum | Unit + Integration |

### Test Template

```python
"""
Tests for [Component Name]

Reference: AGENT_DEVELOPMENT_CONTEXT.md §[section]
"""

import pytest
from ai_earth.capabilities.tool_hub import get_tool, invoke, catalog


class TestToolRegistry:
    """Test tool registration and discovery"""

    def test_register_new_tool(self):
        """Test registering a new tool"""
        ...

    def test_discover_tools_by_domain(self):
        """Test discovering tools filtered by domain"""
        ...

    def test_catalog_format(self):
        """Test catalog YAML output format"""
        ...

    def test_invoke_tool(self):
        """Test invoking a registered tool"""
        ...

    def test_tool_not_found_raises(self):
        """Test that invoking non-existent tool raises"""
        ...


class TestSandboxExecutor:
    """Test sandbox code execution"""

    def test_execute_simple_code(self):
        ...

    def test_execute_with_timeout(self):
        ...

    def test_execute_with_error_returns_traceback(self):
        ...
```

### قبل كل commit:

```bash
# 1. كل الـ tests القديمة تمر
python3 -m pytest tests/ -q
# EXPECTED: 937+ passed

# 2. الـ tests الجديدة
python3 -m pytest tests/test_[new_component].py -v

# 3. Backward compatibility
python3 -c "from genesis.tools.web_search import web_search; print('OK')"
python3 -c "from genesis.goal_specification import run_goal_specification; print('OK')"

# 4. Security scan
git diff HEAD | grep -E "sk-or-v1-|sk-proj-|gsk_|AIzaSy|github_pat_|ghp_"
# EXPECTED: empty
```

---

## 5. Git Workflow

### Commit Message Format
```
feat: [Component] — [description], [N] new tests, [M] total

مثال:
feat: Tool Hub — registry + executor + web_search wrapper, 38 tests, 975 total
fix: Skill Engine — extractor edge case for empty agents, 3 tests fixed
docs: Meta Engine — add header documentation + integration points
refactor: Agent Hub — extract soul system to separate module
```

### Branch Strategy
```
main ← مستقر وكل الـ tests تمر
  │
  ├── ai_earth ← فرع التطوير الرئيسي
  │     │
  │     ├── feat/tool-hub
  │     ├── feat/skill-engine
  │     ├── feat/meta-engine
  │     └── feat/agent-hub
  │
  └── genesis-legacy ← snapshot قبل الهجرة
```

### Git Add — إلزامي explicit
```bash
# ❌ NEVER
git add -A
git add .

# ✅ ALWAYS
git add ai_earth/capabilities/tool_hub/registry.py
git add ai_earth/capabilities/tool_hub/__init__.py
git add tests/test_tool_hub.py
git commit -m "feat: Tool Hub — registry + init, 20 tests"
```

---

## 6. ترتيب التنفيذ لكل Component

```
لكل component جديد، اتبع هذا الترتيب بالضبط:

Step 1: اكتب الـ Schema (schemas/xxx.v1.json)
Step 2: اكتب الـ Dataclasses (to_dict + from_dict)
Step 3: اكتب الـ Tests أولاً (TDD — Red)
Step 4: اكتب الـ Implementation (TDD — Green)
Step 5: اكتب الـ __init__.py (clean public API)
Step 6: اكتب الـ Integration Point (أين يُدمج)
Step 7: حدّث LEGACY_COMPAT (لو فيه imports قديمة تتأثر)
Step 8: حدّث AGENT_DEVELOPMENT_CONTEXT.md
Step 9: حدّث decision_log.py (لو فيه قرارات جديدة)
Step 10: Run all tests → commit → report to F.
```

---

## 7. ما لا تفعله أبداً (Never Do List)

```
❌ لا تعدّل orchestrator.py core logic — فقط أضف injections
❌ لا تحذف أي test قديم — أبداً
❌ لا تستخدم print() — استخدم logging
❌ لا تكتب API key في أي ملف — env vars فقط
❌ لا تكسر backward compatibility — الـ imports القديمة تشتغل
❌ لا تضيف dependency جديدة بدون موافقة F.
❌ لا تعمل git add . أو git add -A — explicit فقط
❌ لا تضيف ملف بدون header documentation
❌ لا تتخطى Step 3 (الـ Tests أولاً)
❌ لا تدمج فرع بدون كل الـ tests تمر
```

---

_هذا الملف يُقرأ من أي AI Agent مكلف بكتابة أو تعديل كود AI Earth._
