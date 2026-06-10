"""
Tests for CrewAI LEGO Pieces — AI Earth Platform
=================================================
Source: https://github.com/crewAIInc/crewAI (22K+ ⭐)
Version: 1.14.6 — Multi-Agent Orchestration Framework
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))


# ══════════════════════════════════════════════════════════════════════
# 1. Core Classes — Agent, Task, Crew, Process
# ══════════════════════════════════════════════════════════════════════

class TestCore:
    """Test CrewAI core classes."""

    def test_agent_import(self):
        from crewai import Agent
        assert Agent is not None

    def test_task_import(self):
        from crewai import Task
        assert Task is not None

    def test_crew_import(self):
        from crewai import Crew
        assert Crew is not None

    def test_process_enum(self):
        from crewai import Process
        assert hasattr(Process, 'sequential')
        assert hasattr(Process, 'hierarchical')
        assert Process.sequential.value == 'sequential'
        assert Process.hierarchical.value == 'hierarchical'

    def test_llm_import(self):
        from crewai import LLM
        assert LLM is not None

    def test_flow_import(self):
        from crewai import Flow
        assert Flow is not None

    def test_knowledge_import(self):
        from crewai import Knowledge
        assert Knowledge is not None


# ══════════════════════════════════════════════════════════════════════
# 2. Task System
# ══════════════════════════════════════════════════════════════════════

class TestTaskSystem:
    """Test Task types and outputs."""

    def test_conditional_task(self):
        from crewai.tasks.conditional_task import ConditionalTask
        assert ConditionalTask is not None

    def test_task_output(self):
        from crewai.tasks.task_output import TaskOutput
        assert TaskOutput is not None

    def test_llm_guardrail(self):
        from crewai.tasks.llm_guardrail import LLMGuardrail
        assert LLMGuardrail is not None

    def test_hallucination_guardrail(self):
        from crewai.tasks.hallucination_guardrail import HallucinationGuardrail
        assert HallucinationGuardrail is not None

    def test_output_format(self):
        from crewai.tasks.output_format import OutputFormat
        assert OutputFormat is not None


# ══════════════════════════════════════════════════════════════════════
# 3. Crew Output
# ══════════════════════════════════════════════════════════════════════

class TestCrewOutput:
    """Test Crew output handling."""

    def test_crew_output(self):
        from crewai.crews.crew_output import CrewOutput
        assert CrewOutput is not None


# ══════════════════════════════════════════════════════════════════════
# 4. Tools System
# ══════════════════════════════════════════════════════════════════════

class TestTools:
    """Test CrewAI tool system."""

    def test_base_tool(self):
        from crewai.tools.base_tool import BaseTool
        assert BaseTool is not None

    def test_structured_tool(self):
        from crewai.tools.structured_tool import CrewStructuredTool
        assert CrewStructuredTool is not None


# ══════════════════════════════════════════════════════════════════════
# 5. Memory System
# ══════════════════════════════════════════════════════════════════════

class TestMemory:
    """Test CrewAI memory components."""

    def test_memory_types(self):
        from crewai.memory.types import MemoryConfig, MemoryMatch, MemoryRecord
        assert MemoryConfig is not None
        assert MemoryMatch is not None
        assert MemoryRecord is not None

    def test_memory_scope(self):
        from crewai.memory.memory_scope import MemoryScope
        assert MemoryScope is not None

    def test_unified_memory(self):
        from crewai.memory.unified_memory import Memory
        assert Memory is not None


# ══════════════════════════════════════════════════════════════════════
# 6. State Management
# ══════════════════════════════════════════════════════════════════════

class TestState:
    """Test state management and checkpoints."""

    def test_runtime_state(self):
        from crewai.state.runtime import RuntimeState
        assert RuntimeState is not None

    def test_checkpoint_config(self):
        from crewai.state.checkpoint_config import CheckpointConfig
        assert CheckpointConfig is not None


# ══════════════════════════════════════════════════════════════════════
# 7. Hooks System
# ══════════════════════════════════════════════════════════════════════

class TestHooks:
    """Test LLM and tool hooks."""

    def test_llm_hooks(self):
        from crewai.hooks.llm_hooks import (
            register_before_llm_call_hook,
            register_after_llm_call_hook,
            LLMCallHookContext,
        )
        assert callable(register_before_llm_call_hook)
        assert callable(register_after_llm_call_hook)
        assert LLMCallHookContext is not None

    def test_tool_hooks(self):
        from crewai.hooks.tool_hooks import (
            register_before_tool_call_hook,
            register_after_tool_call_hook,
            ToolCallHookContext,
        )
        assert callable(register_before_tool_call_hook)
        assert callable(register_after_tool_call_hook)
        assert ToolCallHookContext is not None


# ══════════════════════════════════════════════════════════════════════
# 8. Lite Agent
# ══════════════════════════════════════════════════════════════════════

class TestLiteAgent:
    """Test lightweight agent."""

    def test_lite_agent_import(self):
        from crewai.lite_agent import LiteAgent
        assert LiteAgent is not None

    def test_lite_agent_output(self):
        from crewai.lite_agent_output import LiteAgentOutput
        assert LiteAgentOutput is not None


# ══════════════════════════════════════════════════════════════════════
# 9. Agent Builder & Executor
# ══════════════════════════════════════════════════════════════════════

class TestAgentBuilder:
    """Test agent building blocks."""

    def test_base_agent(self):
        from crewai.agents.agent_builder.base_agent import BaseAgent
        assert BaseAgent is not None

    def test_crew_agent_executor(self):
        from crewai.agents.crew_agent_executor import CrewAgentExecutor
        assert CrewAgentExecutor is not None

    def test_cache_handler(self):
        from crewai.agents.cache.cache_handler import CacheHandler
        assert CacheHandler is not None

    def test_tools_handler(self):
        from crewai.agents.tools_handler import ToolsHandler
        assert ToolsHandler is not None

    def test_step_executor(self):
        from crewai.agents.step_executor import StepExecutor
        assert StepExecutor is not None

    def test_parser_types(self):
        from crewai.agents.parser import AgentAction, AgentFinish, OutputParserError
        assert AgentAction is not None
        assert AgentFinish is not None
        assert OutputParserError is not None


# ══════════════════════════════════════════════════════════════════════
# 10. Constants & Context
# ══════════════════════════════════════════════════════════════════════

class TestConstantsContext:
    """Test constants and execution context."""

    def test_constants(self):
        from crewai.constants import DEFAULT_LLM_MODEL, PROVIDERS
        assert DEFAULT_LLM_MODEL is not None
        assert PROVIDERS is not None

    def test_execution_context(self):
        from crewai.context import ExecutionContext, capture_execution_context
        assert ExecutionContext is not None
        assert callable(capture_execution_context)

    def test_version(self):
        from crewai.version import get_crewai_version
        version = get_crewai_version()
        assert version is not None
        assert isinstance(version, str)


# ══════════════════════════════════════════════════════════════════════
# 11. Flow System
# ══════════════════════════════════════════════════════════════════════

class TestFlowSystem:
    """Test Flow orchestration."""

    def test_flow_config(self):
        from crewai.flow.flow_config import FlowConfig
        assert FlowConfig is not None

    def test_flow_trackable(self):
        from crewai.flow.flow_trackable import FlowTrackable
        assert FlowTrackable is not None


# ══════════════════════════════════════════════════════════════════════
# 12. Security
# ══════════════════════════════════════════════════════════════════════

class TestSecurity:
    """Test security configuration."""

    def test_security_config(self):
        from crewai.security.security_config import SecurityConfig
        assert SecurityConfig is not None


# ══════════════════════════════════════════════════════════════════════
# 13. Types
# ══════════════════════════════════════════════════════════════════════

class TestTypes:
    """Test type definitions."""

    def test_usage_metrics(self):
        from crewai.types.usage_metrics import UsageMetrics
        assert UsageMetrics is not None

    def test_serializable_callable(self):
        from crewai.types.callback import SerializableCallable
        assert SerializableCallable is not None


# ══════════════════════════════════════════════════════════════════════
# 14. LEGO Files Present
# ══════════════════════════════════════════════════════════════════════

class TestLEGOFiles:
    """Verify all extracted CrewAI files exist."""

    def _lego_path(self, *parts):
        base = os.path.join(os.path.dirname(__file__), '..', '..', 'ai_earth', 'lego', 'crewai_src')
        return os.path.join(base, *parts)

    def test_core_files(self):
        for f in ['constants.py', 'context.py', 'settings.py', 'version.py',
                   'process.py', 'task.py', 'crew.py', 'lite_agent.py']:
            assert os.path.exists(self._lego_path(f)), f"Missing {f}"

    def test_agent_files(self):
        for f in ['core.py', 'utils.py', 'planning_config.py']:
            assert os.path.exists(self._lego_path('agent', f)), f"Missing agent/{f}"

    def test_task_files(self):
        for f in ['conditional_task.py', 'task_output.py', 'llm_guardrail.py',
                   'hallucination_guardrail.py', 'output_format.py']:
            assert os.path.exists(self._lego_path('tasks', f)), f"Missing tasks/{f}"

    def test_flow_files(self):
        for f in ['flow.py', 'flow_config.py', 'flow_trackable.py', 'flow_wrappers.py']:
            assert os.path.exists(self._lego_path('flow', f)), f"Missing flow/{f}"

    def test_memory_files(self):
        for f in ['unified_memory.py', 'types.py', 'memory_scope.py', 'encoding_flow.py']:
            assert os.path.exists(self._lego_path('memory', f)), f"Missing memory/{f}"

    def test_tools_files(self):
        for f in ['base_tool.py', 'structured_tool.py', 'tool_usage.py']:
            assert os.path.exists(self._lego_path('tools', f)), f"Missing tools/{f}"

    def test_state_files(self):
        for f in ['runtime.py', 'checkpoint_config.py', 'event_record.py']:
            assert os.path.exists(self._lego_path('state', f)), f"Missing state/{f}"


# ══════════════════════════════════════════════════════════════════════
# 15. Integration — CrewAI + All Other LEGO Pieces
# ══════════════════════════════════════════════════════════════════════

class TestCrewAIIntegration:
    """Test CrewAI works alongside all other LEGO pieces."""

    def test_with_model_router(self):
        from ai_earth.model_router import ModelRouter
        from crewai import Agent, Process
        router = ModelRouter()
        router.configure(mock=True)
        assert router._mock_mode is True
        assert Process.sequential.value == 'sequential'

    def test_with_langgraph(self):
        from crewai import Agent
        from langgraph.graph.state import StateGraph
        from typing import TypedDict
        class S(TypedDict): x: int
        sg = StateGraph(S)
        assert sg is not None

    def test_with_dspy(self):
        from crewai import Agent
        from dspy.primitives.example import Example
        e = Example(question="test")
        assert e.question == "test"

    def test_with_mem0(self):
        from crewai import Agent
        from mem0.configs.base import MemoryConfig
        mc = MemoryConfig()
        assert mc is not None
