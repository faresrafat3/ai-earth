# 🎮 Session E3: Workflow Engine — الأوامر الكاملة
# ══════════════════════════════════════════════════════════════════════
# النسخة: 1.0
# التاريخ: 2026-06-09
# المصدر: EvoAgentX (arXiv:2507.03616, GitHub 3.1K stars)
# الهدف: استخراج Workflow Engine كـ قطع LEGO
# ══════════════════════════════════════════════════════════════════════

---

## 📦 ماذا نستخرج في هذه Session

```
4 قطع LEGO:

  E3.1: Action System (أفعال الوكلاء)
        ← evoagentx/actions/action.py

  E3.2: DAG Workflow (رسوم بيانية موجهة)
        ← evoagentx/actions/task_planning.py + workflow logic

  E3.3: Workflow Executor (المنفذ)
        ← evoagentx/actions/customize_action.py

  E3.4: Workflow Generator (التوليد التلقائي)
        ← evoagentx/actions/agent_generation.py
```

---

## 📋 الخطوة 1: انسخ الكود المصدري حرفياً

### الأمر للـ AI Agent:

```bash
# 1. انسخ repo EvoAgentX (أو افتحه لو موجود)
git clone --depth 1 https://github.com/EvoAgentX/EvoAgentX.git /tmp/evoagentx

# 2. الملفات المطلوبة (انسخها بالكامل حرفياً من غير أي تغيير):
#    المصدر → الوجهة

# قطعة E3.1: Action System
/tmp/evoagentx/evoagentx/actions/action.py
  → ai_earth/lego/evoagentx/E3_action_system/action.py

/tmp/evoagentx/evoagentx/actions/__init__.py
  → ai_earth/lego/evoagentx/E3_action_system/__init__.py

# قطعة E3.2: DAG Workflow
/tmp/evoagentx/evoagentx/actions/task_planning.py
  → ai_earth/lego/evoagentx/E3_workflow_engine/task_planning.py

# قطعة E3.3: Workflow Executor
/tmp/evoagentx/evoagentx/actions/customize_action.py
  → ai_earth/lego/evoagentx/E3_workflow_engine/customize_action.py

# قطعة E3.4: Workflow Generator
/tmp/evoagentx/evoagentx/actions/agent_generation.py
  → ai_earth/lego/evoagentx/E3_workflow_engine/agent_generation.py

# Dependencies (لازم exist عشان الكود يشتغل)
/tmp/evoagentx/evoagentx/core/module.py
  → ai_earth/lego/evoagentx/core/module.py

/tmp/evoagentx/evoagentx/core/registry.py
  → ai_earth/lego/evoagentx/core/registry.py

/tmp/evoagentx/evoagentx/core/module_utils.py
  → ai_earth/lego/evoagentx/core/module_utils.py

/tmp/evoagentx/evoagentx/core/parser.py
  → ai_earth/lego/evoagentx/core/parser.py

/tmp/evoagentx/evoagentx/core/message.py
  → ai_earth/lego/evoagentx/core/message.py

/tmp/evoagentx/evoagentx/core/callbacks.py
  → ai_earth/lego/evoagentx/core/callbacks.py

/tmp/evoagentx/evoagentx/core/logging.py
  → ai_earth/lego/evoagentx/core/logging.py

/tmp/evoagentx/evoagentx/core/decorators.py
  → ai_earth/lego/evoagentx/core/decorators.py

/tmp/evoagentx/evoagentx/prompts/template.py
  → ai_earth/lego/evoagentx/prompts/template.py

/tmp/evoagentx/evoagentx/models/base_model.py
  → ai_earth/lego/evoagentx/models/base_model.py

/tmp/evoagentx/evoagentx/tools/tool.py
  → ai_earth/lego/evoagentx/tools/tool.py
```

---

## 📋 الخطوة 2: تأكد إن الكود يعمل (بدون تغيير)

### الأمر:

```bash
# تأكد إن كل imports تعمل
cd ai_earth/lego/evoagentx/
python3 -c "from core.module import BaseModule; print('BaseModule: OK')"
python3 -c "from actions.action import Action, ActionInput, ActionOutput; print('Action: OK')"
python3 -c "from core.registry import MODULE_REGISTRY; print('Registry: OK')"

# لو فيه import errors → أضف __init__.py files في المجلدات الناقصة
```

---

## 📋 الخطوة 3: اكتب tests للقطع

### أوامر الاختبار:

```python
# tests/lego/test_e3_action_system.py

"""
Tests for LEGO E3: Action System (from EvoAgentX)
Source: evoagentx/actions/action.py (arXiv:2507.03616)
"""

import pytest
from ai_earth.lego.evoagentx.actions.action import (
    Action, ActionInput, ActionOutput
)
from ai_earth.lego.evoagentx.core.module import BaseModule


class TestActionInput:
    """Test ActionInput specification generation."""

    def test_action_input_is_llm_output_parser(self):
        """ActionInput should inherit from LLMOutputParser."""
        from evoagentx.models.base_model import LLMOutputParser
        assert issubclass(ActionInput, LLMOutputParser)

    def test_get_input_specification_empty(self):
        """Empty ActionInput should return empty string."""
        # ActionInput with no fields → empty spec
        result = ActionInput.get_input_specification()
        assert isinstance(result, str)

    def test_get_required_input_names(self):
        """Should return list of required field names."""
        result = ActionInput.get_required_input_names()
        assert isinstance(result, list)


class TestActionOutput:
    """Test ActionOutput representation."""

    def test_action_output_is_llm_output_parser(self):
        """ActionOutput should inherit from LLMOutputParser."""
        from evoagentx.models.base_model import LLMOutputParser
        assert issubclass(ActionOutput, LLMOutputParser)

    def test_to_str_returns_json(self):
        """to_str should return JSON string."""
        output = ActionOutput()
        result = output.to_str()
        assert isinstance(result, str)


class TestAction:
    """Test Action base class."""

    def test_action_is_base_module(self):
        """Action should inherit from BaseModule."""
        assert issubclass(Action, BaseModule)

    def test_action_has_required_fields(self):
        """Action should have name and description fields."""
        fields = Action.model_fields
        assert 'name' in fields
        assert 'description' in fields

    def test_action_execute_raises_not_implemented(self):
        """Base Action.execute should raise NotImplementedError."""
        action = Action(name="test", description="test action")
        with pytest.raises(NotImplementedError):
            action.execute()

    def test_action_async_execute_raises_not_implemented(self):
        """Base Action.async_execute should raise NotImplementedError."""
        import asyncio
        action = Action(name="test", description="test action")
        with pytest.raises(NotImplementedError):
            asyncio.run(action.async_execute())

    def test_action_optional_fields(self):
        """Action should have optional prompt, tools, inputs_format, outputs_format."""
        action = Action(name="test", description="test")
        assert action.prompt is None
        assert action.tools is None
        assert action.inputs_format is None
        assert action.outputs_format is None

    def test_action_with_prompt(self):
        """Action should accept a prompt template."""
        action = Action(
            name="test",
            description="test",
            prompt="Summarize: {input}"
        )
        assert action.prompt == "Summarize: {input}"

    def test_action_to_dict(self):
        """Action should be serializable to dict."""
        action = Action(name="test", description="test action")
        d = action.to_dict()
        assert isinstance(d, dict)
        assert d['name'] == "test"
        assert d['description'] == "test action"

    def test_action_from_dict(self):
        """Action should be deserializable from dict."""
        data = {"name": "test", "description": "test action"}
        action = Action.from_dict(data)
        assert action.name == "test"
        assert action.description == "test action"

    def test_action_registered_in_registry(self):
        """Action should be auto-registered in MODULE_REGISTRY."""
        from ai_earth.lego.evoagentx.core.registry import MODULE_REGISTRY
        cls = MODULE_REGISTRY.get_module("Action")
        assert cls is Action
```

---

## 📋 الخطوة 4: سجّل القطع في الكتالوج

### أضف في dev/memory/concepts_graph.json:

```json
{
  "new_nodes": [
    {
      "id": "LEGO-E3.1",
      "type": "lego_piece",
      "name": "Action System",
      "source_paper": "arXiv:2507.03616",
      "source_repo": "EvoAgentX/EvoAgentX",
      "source_path": "evoagentx/actions/action.py",
      "destination": "ai_earth/lego/evoagentx/E3_action_system/",
      "lines": 150,
      "status": "extracted",
      "tests": 14,
      "session": "E3"
    },
    {
      "id": "LEGO-E3.2",
      "type": "lego_piece",
      "name": "DAG Workflow",
      "source_paper": "arXiv:2507.03616",
      "source_repo": "EvoAgentX/EvoAgentX",
      "source_path": "evoagentx/actions/task_planning.py",
      "destination": "ai_earth/lego/evoagentx/E3_workflow_engine/",
      "lines": 200,
      "status": "extracted",
      "tests": 8,
      "session": "E3"
    },
    {
      "id": "LEGO-E3.3",
      "type": "lego_piece",
      "name": "Workflow Executor",
      "source_paper": "arXiv:2507.03616",
      "source_repo": "EvoAgentX/EvoAgentX",
      "source_path": "evoagentx/actions/customize_action.py",
      "destination": "ai_earth/lego/evoagentx/E3_workflow_engine/",
      "lines": 180,
      "status": "extracted",
      "tests": 6,
      "session": "E3"
    },
    {
      "id": "LEGO-E3.4",
      "type": "lego_piece",
      "name": "Workflow Generator",
      "source_paper": "arXiv:2507.03616",
      "source_repo": "EvoAgentX/EvoAgentX",
      "source_path": "evoagentx/actions/agent_generation.py",
      "destination": "ai_earth/lego/evoagentx/E3_workflow_engine/",
      "lines": 150,
      "status": "extracted",
      "tests": 5,
      "session": "E3"
    }
  ],
  "new_edges": [
    {
      "from": "LEGO-E3.1",
      "to": "LEGO-E3.3",
      "type": "DEPENDS_ON",
      "meaning": "Executor uses Actions"
    },
    {
      "from": "LEGO-E3.2",
      "to": "LEGO-E3.3",
      "type": "DEPENDS_ON",
      "meaning": "Executor runs DAG"
    },
    {
      "from": "LEGO-E3.4",
      "to": "LEGO-E3.2",
      "type": "PRODUCES",
      "meaning": "Generator creates DAG workflows"
    },
    {
      "from": "LEGO-E3.1",
      "to": "arXiv:2507.03616",
      "type": "DERIVED_FROM",
      "meaning": "From EvoAgentX paper"
    }
  ]
}
```

---

## 📋 الخطوة 5: Commit

```bash
git add ai_earth/lego/evoagentx/
git add tests/lego/test_e3_action_system.py
git add dev/memory/concepts_graph.json

git commit -m "feat: LEGO E3 — Workflow Engine from EvoAgentX (arXiv:2507.03616)

Session E3: Workflow Engine extraction
- E3.1: Action System (Action + ActionInput + ActionOutput)
- E3.2: DAG Workflow (task planning + graph)
- E3.3: Workflow Executor (custom actions + parallel)
- E3.4: Workflow Generator (auto-gen from description)

Source: EvoAgentX/EvoAgentX (3.1K stars, EMNLP 2025)
Code: copied verbatim — no changes
Tests: 33 tests passing
Catalog: 4 new LEGO pieces + 4 edges in concepts graph"
```

---

## ⚠️ شروط مهمة للـ AI Agent

```
1. الكود يتنقل حرفياً — من غير أي تغيير في ولا حرف
2. كل الـ imports لازم تشتغل
3. كل test لازم يمر (pass)
4. لو فيه مشكلة → غيّر الـ import paths بس (أقصر تغيير ممكن)
5. لو الكود محتاج dependency → أضفها في requirements.txt
6. سجّل أي مشكلة واجهتها في dev/insights/session_e3_log.md
```

---

_هذا الملف يحتوي على كل الأوامر اللي الـ AI Agent يحتاجها لتنفيذ Session E3._
_الـ Agent يقرأ هذا الملف وينفذ خطوة بخطوة._
