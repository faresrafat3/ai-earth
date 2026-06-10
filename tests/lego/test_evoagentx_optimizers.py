"""
🧪 Tests for EvoAgentX Optimizers — Session E4+E5+E6
═════════════════════════════════════════════════════════
Tests the complete optimizer layer extracted from EvoAgentX:
  - Engine (BaseOptimizer, ParamRegistry, OptimizableField, Decorators)
  - SEW Optimizer (Self-Evolving Workflow)
  - AFlow Optimizer
  - TextGrad Optimizer
  - MapElites Optimizer
  - MIPRO Optimizer (stub-based)
  - EvoPrompt Optimizer

All code extracted VERBATIM from EvoAgentX (arXiv:2507.03616).
"""
import sys
import os
import pytest

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ai_earth', 'lego'))


def _make_sequential_graph():
    """Helper to create a SequentialWorkFlowGraph with tasks format."""
    from evoagentx.workflow.workflow_graph import SequentialWorkFlowGraph
    return SequentialWorkFlowGraph(
        goal="Test workflow",
        tasks=[
            {
                "name": "analyze",
                "description": "Analyze input text",
                "inputs": [{"name": "text", "type": "string", "required": True, "description": "input text"}],
                "outputs": [{"name": "analysis", "type": "string", "required": True, "description": "analysis result"}],
                "prompt": "{text}",
                "parse_mode": "str",
            },
            {
                "name": "summarize",
                "description": "Summarize the analysis",
                "inputs": [{"name": "analysis", "type": "string", "required": True, "description": "analysis"}],
                "outputs": [{"name": "summary", "type": "string", "required": True, "description": "summary"}],
                "prompt": "{analysis}",
                "parse_mode": "str",
            }
        ]
    )


# ═════════════════════════════════════════════════════════
# PART 1: OptimizableField Tests
# ═════════════════════════════════════════════════════════

class TestOptimizableFieldEngine:
    """Tests for OptimizableField from engine/registry.py"""

    def test_field_create(self):
        from evoagentx.optimizers.engine.registry import OptimizableField
        field = OptimizableField("test", lambda: "test_value", lambda v: None)
        assert field.name == "test"
        assert field.get() == "test_value"

    def test_field_get_set(self):
        from evoagentx.optimizers.engine.registry import OptimizableField
        storage = {"val": 42}
        field = OptimizableField("num", lambda: storage["val"], lambda v: storage.update({"val": v}))
        assert field.get() == 42
        field.set(100)
        assert field.get() == 100

    def test_field_init_snapshot_and_reset(self):
        from evoagentx.optimizers.engine.registry import OptimizableField
        storage = {"val": "original"}
        field = OptimizableField("snap_test", lambda: storage["val"], lambda v: storage.update({"val": v}))
        field.init_snapshot()
        assert field.get() == "original"
        field.set("modified")
        assert field.get() == "modified"
        field.reset()
        assert field.get() == "original"


class TestOptimizableFieldCore:
    """Tests for OptimizableField from optimizer_core.py"""

    def test_core_field_create(self):
        from evoagentx.optimizers.optimizer_core import OptimizableField
        field = OptimizableField("test", lambda: "hello", lambda v: None)
        assert field.name == "test"
        assert field.get() == "hello"

    def test_core_field_set(self):
        from evoagentx.optimizers.optimizer_core import OptimizableField
        state = {"x": 10}
        field = OptimizableField("x", lambda: state["x"], lambda v: state.update({"x": v}))
        field.set(20)
        assert state["x"] == 20


class TestParamRegistry:
    """Tests for ParamRegistry from engine/registry.py"""

    def test_registry_create(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry
        reg = ParamRegistry()
        assert len(reg.names()) == 0

    def test_registry_register_and_get(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry, OptimizableField
        reg = ParamRegistry()
        field = OptimizableField("param1", lambda: 42, lambda v: None)
        reg.register_field(field)
        assert "param1" in reg.names()
        assert reg.get("param1") == 42

    def test_registry_set(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry, OptimizableField
        storage = {"x": 1}
        reg = ParamRegistry()
        field = OptimizableField("x", lambda: storage["x"], lambda v: storage.update({"x": v}))
        reg.register_field(field)
        reg.set("x", 99)
        assert reg.get("x") == 99

    def test_registry_track_attribute(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry

        class MyObj:
            temperature = 0.7
            top_p = 0.9

        obj = MyObj()
        reg = ParamRegistry()
        reg.track(obj, "temperature")
        reg.track(obj, "top_p")

        assert set(reg.names()) == {"temperature", "top_p"}
        assert reg.get("temperature") == 0.7
        assert reg.get("top_p") == 0.9

    def test_registry_track_nested_path(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry

        class Inner:
            value = "inner_val"

        class Outer:
            inner = Inner()

        obj = Outer()
        reg = ParamRegistry()
        reg.track(obj, "inner.value", name="inner_val")

        assert "inner_val" in reg.names()
        assert reg.get("inner_val") == "inner_val"

    def test_registry_reset(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry, OptimizableField
        storage = {"x": 10}
        reg = ParamRegistry()
        field = OptimizableField("x", lambda: storage["x"], lambda v: storage.update({"x": v}))
        reg.register_field(field)
        reg.set("x", 99)
        reg.reset()
        assert reg.get("x") == 10

    def test_registry_get_field(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry, OptimizableField
        reg = ParamRegistry()
        field = OptimizableField("f1", lambda: "val", lambda v: None)
        reg.register_field(field)
        got = reg.get_field("f1")
        assert got is field

    def test_registry_get_field_missing(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry
        reg = ParamRegistry()
        with pytest.raises(ValueError):
            reg.get_field("nonexistent")


class TestPromptRegistry:
    """Tests for PromptRegistry from optimizer_core.py"""

    def test_prompt_registry_create(self):
        from evoagentx.optimizers.optimizer_core import PromptRegistry
        reg = PromptRegistry()
        assert len(reg.names()) == 0

    def test_prompt_registry_register_path(self):
        from evoagentx.optimizers.optimizer_core import PromptRegistry

        class Obj:
            system_prompt = "You are helpful"

        obj = Obj()
        reg = PromptRegistry()
        reg.register_path(obj, "system_prompt", name="sys_prompt")

        assert "sys_prompt" in reg.names()
        assert reg.get("sys_prompt") == "You are helpful"

    def test_prompt_registry_register_nested(self):
        from evoagentx.optimizers.optimizer_core import PromptRegistry

        class Inner:
            template = "Hello {name}"

        class Outer:
            prompt = Inner()

        obj = Outer()
        reg = PromptRegistry()
        reg.register_path(obj, "prompt.template", name="tpl")

        assert reg.get("tpl") == "Hello {name}"
        reg.set("tpl", "Hi {name}!")
        assert reg.get("tpl") == "Hi {name}!"


# ═════════════════════════════════════════════════════════
# PART 2: Engine Decorators Tests
# ═════════════════════════════════════════════════════════

class TestEntryPointDecorator:
    """Tests for EntryPoint decorator from engine/decorators.py"""

    def test_entry_point_register(self):
        from evoagentx.optimizers.engine.decorators import EntryPoint
        EntryPoint._entry_func = None

        @EntryPoint()
        def my_entry():
            return "result"

        assert EntryPoint.get_entry() is my_entry
        assert EntryPoint.get_entry()() == "result"
        EntryPoint._entry_func = None

    def test_entry_point_none(self):
        from evoagentx.optimizers.engine.decorators import EntryPoint
        EntryPoint._entry_func = None
        assert EntryPoint.get_entry() is None


class TestOptimizeParamDecorator:
    """Tests for OptimizeParam decorator from engine/decorators.py"""

    def test_optimize_param_call(self):
        from evoagentx.optimizers.engine.decorators import OptimizeParam
        OptimizeParam._targets = []

        @OptimizeParam("temperature")
        def my_func():
            return 42

        assert my_func() == 42
        OptimizeParam._targets = []

    def test_optimize_param_with_on_execute(self):
        from evoagentx.optimizers.engine.decorators import OptimizeParam
        OptimizeParam._targets = []

        called = []

        def on_exec_cb(func, *args, **kwargs):
            called.append(func.__name__)

        @OptimizeParam("temperature", on_execute=on_exec_cb)
        def my_func():
            return 99

        result = my_func()
        assert result == 99
        assert len(called) == 1
        OptimizeParam._targets = []

    def test_optimize_param_decorator_creates_instance(self):
        from evoagentx.optimizers.engine.decorators import OptimizeParam
        op = OptimizeParam("temperature", "top_p")
        assert op.param_names == ["temperature", "top_p"]

    def test_optimize_param_with_on_execute(self):
        from evoagentx.optimizers.engine.decorators import OptimizeParam
        OptimizeParam._targets = []

        called = []

        def on_exec_cb(func, *args, **kwargs):
            called.append(func.__name__)

        @OptimizeParam("temperature", on_execute=on_exec_cb)
        def my_func():
            return 99

        result = my_func()
        assert result == 99
        assert len(called) == 1
        OptimizeParam._targets = []

    def test_optimize_param_stores_wrapped_func(self):
        from evoagentx.optimizers.engine.decorators import OptimizeParam
        op = OptimizeParam("x", "y")

        @op
        def my_func():
            return 42

        # The decorator wraps the function and stores it
        assert my_func() == 42
        # Check that _targets has entries on the instance
        assert len(op._targets) >= 1

    def test_get_params_for_func(self):
        from evoagentx.optimizers.engine.decorators import OptimizeParam
        op = OptimizeParam("alpha", "beta")

        @op
        def my_func():
            pass

        # The params are stored in op._targets as (wrapped_func, param_names, callback)
        last_entry = op._targets[-1]
        assert last_entry[1] == ["alpha", "beta"]


# ═════════════════════════════════════════════════════════
# PART 3: CodeBlock Tests
# ═════════════════════════════════════════════════════════

class TestCodeBlock:
    """Tests for CodeBlock from optimizer_core.py"""

    def test_codeblock_create(self):
        from evoagentx.optimizers.optimizer_core import CodeBlock
        block = CodeBlock("test_block", lambda cfg: cfg["x"] * 2)
        assert block.name == "test_block"

    def test_codeblock_run(self):
        from evoagentx.optimizers.optimizer_core import CodeBlock
        block = CodeBlock("double", lambda cfg: cfg["x"] * 2)
        result = block.run({"x": 5})
        assert result == 10

    def test_codeblock_callable(self):
        from evoagentx.optimizers.optimizer_core import CodeBlock
        block = CodeBlock("triple", lambda cfg: cfg["x"] * 3)
        assert block({"x": 4}) == 12

    def test_codeblock_repr(self):
        from evoagentx.optimizers.optimizer_core import CodeBlock
        block = CodeBlock("my_block", lambda cfg: None)
        assert "my_block" in repr(block)


# ═════════════════════════════════════════════════════════
# PART 4: Optimizer Base Class Tests
# ═════════════════════════════════════════════════════════

class TestOptimizerBase:
    """Tests for Optimizer base class from optimizer.py"""

    def test_optimizer_is_basemodule(self):
        from evoagentx.optimizers.optimizer import Optimizer
        from evoagentx.core.module import BaseModule
        assert issubclass(Optimizer, BaseModule)

    def test_optimizer_has_methods(self):
        from evoagentx.optimizers.optimizer import Optimizer
        assert hasattr(Optimizer, 'optimize')
        assert hasattr(Optimizer, 'step')
        assert hasattr(Optimizer, 'evaluate')
        assert hasattr(Optimizer, 'convergence_check')

    def test_optimizer_fields(self):
        from evoagentx.optimizers.optimizer import Optimizer
        fields = Optimizer.model_fields
        assert 'graph' in fields
        assert 'evaluator' in fields
        assert 'max_steps' in fields
        assert 'convergence_threshold' in fields

    def test_base_optimizer_is_abstract(self):
        from evoagentx.optimizers.engine.base import BaseOptimizer
        assert hasattr(BaseOptimizer, 'optimize')


# ═════════════════════════════════════════════════════════
# PART 5: SEW Optimizer Tests
# ═════════════════════════════════════════════════════════

class TestSEWOptimizer:
    """Tests for SEWOptimizer (Self-Evolving Workflow)"""

    def test_sew_is_importable(self):
        from evoagentx.optimizers.sew_optimizer import SEWOptimizer
        assert SEWOptimizer is not None

    def test_sew_is_optimizer(self):
        from evoagentx.optimizers.sew_optimizer import SEWOptimizer
        from evoagentx.optimizers.optimizer import Optimizer
        assert issubclass(SEWOptimizer, Optimizer)

    def test_sew_workflow_scheme_class(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        assert SEWWorkFlowScheme is not None

    def test_sew_valid_schemes(self):
        from evoagentx.optimizers.sew_optimizer import VALID_SCHEMES
        assert "python" in VALID_SCHEMES
        assert "yaml" in VALID_SCHEMES
        assert "code" in VALID_SCHEMES
        assert "core" in VALID_SCHEMES
        assert "bpmn" in VALID_SCHEMES

    def test_sew_scheme_python_repr(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        graph = _make_sequential_graph()
        scheme = SEWWorkFlowScheme(graph=graph)
        python_repr = scheme.convert_to_scheme("python")
        assert "analyze" in python_repr
        assert "summarize" in python_repr

    def test_sew_scheme_yaml_repr(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        from evoagentx.workflow.workflow_graph import SequentialWorkFlowGraph
        graph = SequentialWorkFlowGraph(
            goal="YAML test",
            tasks=[{
                "name": "task_a",
                "description": "Task A",
                "inputs": [{"name": "data", "type": "string", "required": True, "description": "input"}],
                "outputs": [{"name": "output", "type": "string", "required": True, "description": "result"}],
                "prompt": "{data}",
                "parse_mode": "str",
            }]
        )
        scheme = SEWWorkFlowScheme(graph=graph)
        yaml_repr = scheme.convert_to_scheme("yaml")
        assert "task_a" in yaml_repr

    def test_sew_scheme_code_repr(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        graph = _make_sequential_graph()
        scheme = SEWWorkFlowScheme(graph=graph)
        code_repr = scheme.convert_to_scheme("code")
        assert "analyze" in code_repr
        assert "summarize" in code_repr
        assert "->" in code_repr

    def test_sew_scheme_bpmn_repr(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        from evoagentx.workflow.workflow_graph import SequentialWorkFlowGraph
        graph = SequentialWorkFlowGraph(
            goal="BPMN test",
            tasks=[{
                "name": "start_process",
                "description": "Start process",
                "inputs": [],
                "outputs": [{"name": "out", "type": "string", "required": True, "description": "output"}],
                "prompt": "process",
                "parse_mode": "str",
            }]
        )
        scheme = SEWWorkFlowScheme(graph=graph)
        bpmn_repr = scheme.convert_to_scheme("bpmn")
        assert "definitions" in bpmn_repr
        assert "start_process" in bpmn_repr

    def test_sew_scheme_invalid_raises(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        from evoagentx.workflow.workflow_graph import SequentialWorkFlowGraph
        graph = SequentialWorkFlowGraph(
            goal="invalid",
            tasks=[{
                "name": "t1",
                "description": "task",
                "inputs": [],
                "outputs": [],
                "prompt": "x",
                "parse_mode": "str",
            }]
        )
        scheme = SEWWorkFlowScheme(graph=graph)
        with pytest.raises(ValueError):
            scheme.convert_to_scheme("invalid_scheme")

    def test_sew_scheme_func_name_conversion(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        from evoagentx.workflow.workflow_graph import SequentialWorkFlowGraph
        graph = SequentialWorkFlowGraph(
            goal="test",
            tasks=[{
                "name": "My Fancy Task-Name",
                "description": "fancy task",
                "inputs": [{"name": "x", "type": "string", "required": True, "description": "x"}],
                "outputs": [{"name": "y", "type": "string", "required": True, "description": "y"}],
                "prompt": "{x}",
                "parse_mode": "str",
            }]
        )
        scheme = SEWWorkFlowScheme(graph=graph)
        func_name = scheme._convert_to_func_name("My Fancy Task-Name")
        assert func_name == "my_fancy_task_name"

    def test_sew_scheme_core_repr(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        graph = _make_sequential_graph()
        scheme = SEWWorkFlowScheme(graph=graph)
        core_repr = scheme.convert_to_scheme("core")
        assert "Step" in core_repr
        assert "Analyze" in core_repr


# ═════════════════════════════════════════════════════════
# PART 6: AFlow Optimizer Tests
# ═════════════════════════════════════════════════════════

class TestAFlowOptimizer:
    """Tests for AFlowOptimizer"""

    def test_aflow_is_importable(self):
        from evoagentx.optimizers.aflow_optimizer import AFlowOptimizer
        assert AFlowOptimizer is not None

    def test_aflow_is_basemodule(self):
        from evoagentx.optimizers.aflow_optimizer import AFlowOptimizer
        from evoagentx.core.module import BaseModule
        assert issubclass(AFlowOptimizer, BaseModule)

    def test_aflow_has_fields(self):
        from evoagentx.optimizers.aflow_optimizer import AFlowOptimizer
        fields = AFlowOptimizer.model_fields
        assert 'question_type' in fields
        assert 'graph_path' in fields
        assert 'max_rounds' in fields
        assert 'operators' in fields

    def test_aflow_graph_optimize_output(self):
        from evoagentx.optimizers.aflow_optimizer import GraphOptimizeOutput
        out = GraphOptimizeOutput()
        assert out.modification == ""
        assert out.graph == ""
        assert out.prompt == ""

    def test_aflow_parse_output(self):
        from evoagentx.optimizers.aflow_optimizer import AFlowOptimizer
        content = """<modification>Added review step</modification>
```python
class Workflow:
    pass
```
"""
        result = AFlowOptimizer._parse_optimizer_llm_output(None, content, orig_graph="orig", orig_prompt="orig_prompt")
        assert "Added review step" in result["modification"]

    def test_aflow_parse_output_no_blocks(self):
        from evoagentx.optimizers.aflow_optimizer import AFlowOptimizer
        content = "No useful output"
        result = AFlowOptimizer._parse_optimizer_llm_output(None, content, orig_graph="orig_g", orig_prompt="orig_p")
        assert result["graph"] == "orig_g"
        assert result["prompt"] == "orig_p"


# ═════════════════════════════════════════════════════════
# PART 7: TextGrad Optimizer Tests
# ═════════════════════════════════════════════════════════

class TestTextGradOptimizer:
    """Tests for TextGradOptimizer"""

    def test_textgrad_is_importable(self):
        from evoagentx.optimizers.textgrad_optimizer import TextGradOptimizer
        assert TextGradOptimizer is not None

    def test_textgrad_is_basemodule(self):
        from evoagentx.optimizers.textgrad_optimizer import TextGradOptimizer
        from evoagentx.core.module import BaseModule
        assert issubclass(TextGradOptimizer, BaseModule)

    def test_textgrad_has_fields(self):
        from evoagentx.optimizers.textgrad_optimizer import TextGradOptimizer
        fields = TextGradOptimizer.model_fields
        assert 'graph' in fields
        assert 'optimize_mode' in fields
        assert 'max_steps' in fields
        assert 'batch_size' in fields

    def test_textgrad_engine_class(self):
        from evoagentx.optimizers.textgrad_optimizer import TextGradEngine
        assert TextGradEngine is not None

    def test_textgrad_agent_class(self):
        from evoagentx.optimizers.textgrad_optimizer import TextGradAgent
        assert TextGradAgent is not None

    def test_textgrad_custom_agent_call(self):
        from evoagentx.optimizers.textgrad_optimizer import CustomAgentCall
        assert CustomAgentCall is not None

    def test_textgrad_optimize_modes(self):
        from evoagentx.optimizers.textgrad_optimizer import TextGradOptimizer
        fields = TextGradOptimizer.model_fields
        assert fields['optimize_mode'].default == "all"


# ═════════════════════════════════════════════════════════
# PART 8: MapElites Optimizer Tests
# ═════════════════════════════════════════════════════════

class TestMapElitesOptimizer:
    """Tests for MapElitesOptimizer"""

    def test_mapelites_is_importable(self):
        from evoagentx.optimizers.map_elites_optimizer import MapElitesOptimizer
        assert MapElitesOptimizer is not None

    def test_mapelites_is_base_optimizer(self):
        from evoagentx.optimizers.map_elites_optimizer import MapElitesOptimizer
        from evoagentx.optimizers.engine.base import BaseOptimizer
        assert issubclass(MapElitesOptimizer, BaseOptimizer)


# ═════════════════════════════════════════════════════════
# PART 9: MIPRO Optimizer Tests
# ═════════════════════════════════════════════════════════

class TestMiproOptimizer:
    """Tests for MiproOptimizer"""

    def test_mipro_is_importable(self):
        from evoagentx.optimizers.mipro_optimizer import MiproOptimizer
        assert MiproOptimizer is not None

    def test_mipro_lm_wrapper_class(self):
        from evoagentx.optimizers.mipro_optimizer import MiproLMWrapper
        assert MiproLMWrapper is not None


# ═════════════════════════════════════════════════════════
# PART 10: EvoPrompt Optimizer Tests
# ═════════════════════════════════════════════════════════

class TestEvopromptOptimizer:
    """Tests for EvopromptOptimizer"""

    def test_evoprompt_is_importable(self):
        from evoagentx.optimizers.evoprompt_optimizer import EvopromptOptimizer
        assert EvopromptOptimizer is not None

    def test_evoprompt_is_base_optimizer(self):
        from evoagentx.optimizers.evoprompt_optimizer import EvopromptOptimizer
        from evoagentx.optimizers.engine.base import BaseOptimizer
        assert issubclass(EvopromptOptimizer, BaseOptimizer)


# ═════════════════════════════════════════════════════════
# PART 11: Prompts Tests
# ═════════════════════════════════════════════════════════

class TestTextGradPrompts:
    """Tests for TextGrad optimizer prompts"""

    def test_loss_prompts_exist(self):
        from evoagentx.prompts.optimizers.textgrad_optimizer import (
            GENERAL_LOSS_PROMPT, CODE_LOSS_PROMPT, NO_ANSWER_LOSS_PROMPT,
        )
        assert len(GENERAL_LOSS_PROMPT) > 0
        assert len(CODE_LOSS_PROMPT) > 0
        assert len(NO_ANSWER_LOSS_PROMPT) > 0

    def test_system_prompt_exists(self):
        from evoagentx.prompts.optimizers.textgrad_optimizer import OPTIMIZER_SYSTEM_PROMPT
        assert "optimization" in OPTIMIZER_SYSTEM_PROMPT.lower()

    def test_examples_exist(self):
        from evoagentx.prompts.optimizers.textgrad_optimizer import (
            PERSONAL_FINANCE_ADVISOR_EXAMPLE,
            FITNESS_COACH_EXAMPLE,
            CODE_REVIEW_EXAMPLE,
        )
        assert len(PERSONAL_FINANCE_ADVISOR_EXAMPLE) > 0
        assert len(FITNESS_COACH_EXAMPLE) > 0
        assert len(CODE_REVIEW_EXAMPLE) > 0

    def test_constraints_exist(self):
        from evoagentx.prompts.optimizers.textgrad_optimizer import OPTIMIZER_CONSTRAINTS
        assert len(OPTIMIZER_CONSTRAINTS) > 0


class TestAFlowPrompts:
    """Tests for AFlow optimizer prompts"""

    def test_workflow_optimize_prompt_exists(self):
        from evoagentx.prompts.optimizers.aflow_optimizer import WORKFLOW_OPTIMIZE_PROMPT
        assert len(WORKFLOW_OPTIMIZE_PROMPT) > 0

    def test_workflow_input_exists(self):
        from evoagentx.prompts.optimizers.aflow_optimizer import WORKFLOW_INPUT
        assert "graph" in WORKFLOW_INPUT.lower()

    def test_workflow_template_exists(self):
        from evoagentx.prompts.optimizers.aflow_optimizer import WORKFLOW_TEMPLATE
        assert "operator" in WORKFLOW_TEMPLATE.lower()


class TestSEWPrompts:
    """Tests for SEW optimizer prompts"""

    def test_mutation_prompts_exist(self):
        from evoagentx.prompts.workflow.sew_optimizer import mutation_prompts
        assert len(mutation_prompts) > 10

    def test_thinking_styles_exist(self):
        from evoagentx.prompts.workflow.sew_optimizer import thinking_styles
        assert len(thinking_styles) > 0


# ═════════════════════════════════════════════════════════
# PART 12: Integration Tests
# ═════════════════════════════════════════════════════════

class TestOptimizerIntegration:
    """Integration tests for the optimizer layer"""

    def test_full_registry_workflow(self):
        from evoagentx.optimizers.engine.registry import ParamRegistry

        class WorkflowConfig:
            temperature = 0.7
            model_name = "gpt-4"
            max_tokens = 1000

        config = WorkflowConfig()
        reg = ParamRegistry()
        reg.track(config, "temperature")
        reg.track(config, "model_name", name="model")
        reg.track(config, "max_tokens")

        assert set(reg.names()) == {"temperature", "model", "max_tokens"}
        reg.set("temperature", 1.2)
        reg.set("model", "gpt-4o")
        reg.set("max_tokens", 2000)
        assert config.temperature == 1.2
        assert config.model_name == "gpt-4o"
        assert config.max_tokens == 2000

    def test_codeblock_with_registry(self):
        from evoagentx.optimizers.optimizer_core import CodeBlock, PromptRegistry

        class MyWorkflow:
            prompt = "Answer: "
            def run(self):
                return {"output": self.prompt + "42"}

        wf = MyWorkflow()
        reg = PromptRegistry()
        reg.register_path(wf, "prompt", name="main_prompt")

        block = CodeBlock("run_wf", lambda cfg: wf.run())
        result = block.run({})
        assert result["output"] == "Answer: 42"

        reg.set("main_prompt", "Result: ")
        result = block.run({})
        assert result["output"] == "Result: 42"

    def test_sew_scheme_roundtrip(self):
        from evoagentx.optimizers.sew_optimizer import SEWWorkFlowScheme
        graph = _make_sequential_graph()
        scheme = SEWWorkFlowScheme(graph=graph)

        for scheme_name in ["python", "yaml", "code", "bpmn"]:
            repr_str = scheme.convert_to_scheme(scheme_name)
            assert len(repr_str) > 0, f"Empty representation for {scheme_name}"
            assert "analyze" in repr_str.lower(), f"Missing 'analyze' in {scheme_name}: {repr_str}"

        # core uses title case "Analyze" 
        core_repr = scheme.convert_to_scheme("core")
        assert len(core_repr) > 0
        assert "Analyze" in core_repr


# ═════════════════════════════════════════════════════════
# PART 13: safe_deepcopy Tests
# ═════════════════════════════════════════════════════════

class TestSafeDeepCopy:
    """Tests for safe_deepcopy utility"""

    def test_safe_deepcopy_simple(self):
        from evoagentx.optimizers.engine.registry import safe_deepcopy
        obj = {"a": [1, 2, 3], "b": "hello"}
        copied = safe_deepcopy(obj)
        assert copied == obj
        assert copied is not obj

    def test_safe_deepcopy_nested(self):
        from evoagentx.optimizers.engine.registry import safe_deepcopy
        obj = {"nested": {"deep": [1, 2, {"x": 42}]}}
        copied = safe_deepcopy(obj)
        copied["nested"]["deep"][2]["x"] = 99
        assert obj["nested"]["deep"][2]["x"] == 42

    def test_safe_deepcopy_uncopyable(self):
        import warnings
        from evoagentx.optimizers.engine.registry import safe_deepcopy

        class Uncopyable:
            def __init__(self):
                self.value = 42
            def __deepcopy__(self, memo):
                raise RuntimeError("Can't deepcopy me!")

        obj = Uncopyable()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            copied = safe_deepcopy(obj)
        assert copied is not None
