"""
Tests for AutoGen LEGO Pieces — AI Earth Platform
==================================================
Source: https://github.com/microsoft/autogen (42K+ ⭐)
Version: 0.7.5 — Event-driven Multi-Agent Framework by Microsoft
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))


# ══════════════════════════════════════════════════════════════════════
# 1. Core — Agent Runtime & Models
# ══════════════════════════════════════════════════════════════════════

class TestCoreRuntime:
    """Test autogen_core runtime components."""

    def test_agent_id(self):
        from autogen_core import AgentId, AgentType
        aid = AgentId("test", "key1")
        assert aid is not None
        assert str(aid)

    def test_topic_id(self):
        from autogen_core import TopicId
        tid = TopicId("my_topic", source="test")
        assert tid is not None

    def test_agent_type(self):
        from autogen_core import AgentType
        at = AgentType("assistant")
        assert at is not None

    def test_single_threaded_runtime(self):
        from autogen_core import SingleThreadedAgentRuntime
        assert SingleThreadedAgentRuntime is not None

    def test_cancellation_token(self):
        from autogen_core import CancellationToken
        ct = CancellationToken()
        assert ct is not None

    def test_routed_agent(self):
        from autogen_core import RoutedAgent, message_handler
        assert RoutedAgent is not None
        assert callable(message_handler)


# ══════════════════════════════════════════════════════════════════════
# 2. Core — Models
# ══════════════════════════════════════════════════════════════════════

class TestCoreModels:
    """Test model interfaces."""

    def test_user_message(self):
        from autogen_core.models import UserMessage
        msg = UserMessage(content="Hello", source="user")
        assert msg.content == "Hello"

    def test_assistant_message(self):
        from autogen_core.models import AssistantMessage
        msg = AssistantMessage(content="Hi!", source="assistant")
        assert msg.content == "Hi!"

    def test_system_message(self):
        from autogen_core.models import SystemMessage
        msg = SystemMessage(content="You are helpful")
        assert msg.content == "You are helpful"

    def test_chat_completion_client(self):
        from autogen_core.models import ChatCompletionClient
        assert ChatCompletionClient is not None

    def test_create_result(self):
        from autogen_core.models import CreateResult
        assert CreateResult is not None


# ══════════════════════════════════════════════════════════════════════
# 3. Core — Tools
# ══════════════════════════════════════════════════════════════════════

class TestCoreTools:
    """Test tool system."""

    def test_function_tool(self):
        from autogen_core.tools import FunctionTool
        def my_func(x: str) -> str:
            """Process x."""
            return x.upper()
        tool = FunctionTool(my_func, description="Process input")
        assert tool is not None

    def test_function_tool_properties(self):
        from autogen_core.tools import FunctionTool
        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b
        tool = FunctionTool(add, description="Add numbers")
        assert tool.name == "add"


# ══════════════════════════════════════════════════════════════════════
# 4. Core — Memory
# ══════════════════════════════════════════════════════════════════════

class TestCoreMemory:
    """Test memory system."""

    def test_memory_types(self):
        from autogen_core.memory import Memory, MemoryContent, MemoryQueryResult
        assert Memory is not None
        assert MemoryContent is not None
        assert MemoryQueryResult is not None

    def test_list_memory(self):
        from autogen_core.memory import ListMemory
        lm = ListMemory()
        assert lm is not None

    def test_memory_content(self):
        from autogen_core.memory import MemoryContent, MemoryMimeType
        mc = MemoryContent(content="test data", mime_type=MemoryMimeType.TEXT)
        assert mc.content == "test data"


# ══════════════════════════════════════════════════════════════════════
# 5. Core — Code Executor
# ══════════════════════════════════════════════════════════════════════

class TestCodeExecutor:
    """Test code execution."""

    def test_code_executor_import(self):
        from autogen_core.code_executor import CodeExecutor, CodeBlock
        assert CodeExecutor is not None
        assert CodeBlock is not None


# ══════════════════════════════════════════════════════════════════════
# 6. AgentChat — Agents
# ══════════════════════════════════════════════════════════════════════

class TestAgentChatAgents:
    """Test agent types."""

    def test_assistant_agent(self):
        from autogen_agentchat.agents import AssistantAgent
        assert AssistantAgent is not None

    def test_user_proxy_agent(self):
        from autogen_agentchat.agents import UserProxyAgent
        assert UserProxyAgent is not None

    def test_code_executor_agent(self):
        from autogen_agentchat.agents import CodeExecutorAgent
        assert CodeExecutorAgent is not None


# ══════════════════════════════════════════════════════════════════════
# 7. AgentChat — Teams
# ══════════════════════════════════════════════════════════════════════

class TestAgentChatTeams:
    """Test team orchestration types."""

    def test_round_robin_group_chat(self):
        from autogen_agentchat.teams import RoundRobinGroupChat
        assert RoundRobinGroupChat is not None

    def test_selector_group_chat(self):
        from autogen_agentchat.teams import SelectorGroupChat
        assert SelectorGroupChat is not None

    def test_swarm(self):
        from autogen_agentchat.teams import Swarm
        assert Swarm is not None

    def test_magentic_one_group_chat(self):
        from autogen_agentchat.teams import MagenticOneGroupChat
        assert MagenticOneGroupChat is not None


# ══════════════════════════════════════════════════════════════════════
# 8. AgentChat — Base & Conditions
# ══════════════════════════════════════════════════════════════════════

class TestAgentChatConditions:
    """Test termination conditions and base types."""

    def test_task_result(self):
        from autogen_agentchat.base import TaskResult, Response
        assert TaskResult is not None
        assert Response is not None

    def test_chat_agent(self):
        from autogen_agentchat.base import ChatAgent
        assert ChatAgent is not None

    def test_text_mention_termination(self):
        from autogen_agentchat.conditions import TextMentionTermination
        cond = TextMentionTermination("TERMINATE")
        assert cond is not None

    def test_max_message_termination(self):
        from autogen_agentchat.conditions import MaxMessageTermination
        cond = MaxMessageTermination(10)
        assert cond is not None

    def test_token_usage_termination(self):
        from autogen_agentchat.conditions import TokenUsageTermination
        assert TokenUsageTermination is not None

    def test_source_match_termination(self):
        from autogen_agentchat.conditions import SourceMatchTermination
        assert SourceMatchTermination is not None

    def test_timeout_termination(self):
        from autogen_agentchat.conditions import TimeoutTermination
        assert TimeoutTermination is not None


# ══════════════════════════════════════════════════════════════════════
# 9. AgentChat — Messages
# ══════════════════════════════════════════════════════════════════════

class TestAgentChatMessages:
    """Test message types."""

    def test_chat_message(self):
        from autogen_agentchat.messages import ChatMessage, TextMessage
        msg = TextMessage(content="Hello", source="user")
        assert msg.content == "Hello"

    def test_multi_modal_message(self):
        from autogen_agentchat.messages import MultiModalMessage
        assert MultiModalMessage is not None

    def test_handoff_message(self):
        from autogen_agentchat.messages import HandoffMessage
        assert HandoffMessage is not None

    def test_tool_call_summary(self):
        from autogen_agentchat.messages import ToolCallSummaryMessage
        assert ToolCallSummaryMessage is not None


# ══════════════════════════════════════════════════════════════════════
# 10. AgentChat — UI & State
# ══════════════════════════════════════════════════════════════════════

class TestAgentChatUIState:
    """Test UI and state components."""

    def test_console(self):
        from autogen_agentchat.ui import Console
        assert Console is not None

    def test_assistant_agent_state(self):
        from autogen_agentchat.state import AssistantAgentState
        assert AssistantAgentState is not None

    def test_team_state(self):
        from autogen_agentchat.state import TeamState
        assert TeamState is not None

    def test_round_robin_manager_state(self):
        from autogen_agentchat.state import RoundRobinManagerState
        assert RoundRobinManagerState is not None

    def test_selector_manager_state(self):
        from autogen_agentchat.state import SelectorManagerState
        assert SelectorManagerState is not None

    def test_swarm_manager_state(self):
        from autogen_agentchat.state import SwarmManagerState
        assert SwarmManagerState is not None


# ══════════════════════════════════════════════════════════════════════
# 11. AgentChat — Tools
# ══════════════════════════════════════════════════════════════════════

class TestAgentChatTools:
    """Test agent tools."""

    def test_agent_tool(self):
        from autogen_agentchat.tools import AgentTool
        assert AgentTool is not None

    def test_team_tool(self):
        from autogen_agentchat.tools import TeamTool
        assert TeamTool is not None


# ══════════════════════════════════════════════════════════════════════
# 12. LEGO Files Present
# ══════════════════════════════════════════════════════════════════════

class TestLEGOFiles:
    """Verify extracted AutoGen files exist."""

    def _lego_path(self, *parts):
        base = os.path.join(os.path.dirname(__file__), '..', '..', 'ai_earth', 'lego', 'autogen_src')
        return os.path.join(base, *parts)

    def test_core_files(self):
        for f in ['_agent_id.py', '_routed_agent.py', '_cancellation_token.py']:
            assert os.path.exists(self._lego_path('core', f)), f"Missing core/{f}"

    def test_core_model_files(self):
        for f in ['__init__.py', '_model_client.py']:
            assert os.path.exists(self._lego_path('core', 'models', f)), f"Missing core/models/{f}"

    def test_core_tool_files(self):
        assert os.path.exists(self._lego_path('core', 'tools', '__init__.py')), "Missing core/tools/"

    def test_core_memory_files(self):
        assert os.path.exists(self._lego_path('core', 'memory', '__init__.py')), "Missing core/memory/"

    def test_agentchat_agent_files(self):
        for f in ['__init__.py', '_assistant_agent.py']:
            assert os.path.exists(self._lego_path('agentchat', 'agents', f)), f"Missing agentchat/agents/{f}"

    def test_agentchat_team_files(self):
        for f in ['__init__.py']:
            assert os.path.exists(self._lego_path('agentchat', 'teams', f)), f"Missing agentchat/teams/{f}"

    def test_agentchat_condition_files(self):
        assert os.path.exists(self._lego_path('agentchat', 'conditions', '__init__.py')), "Missing conditions/"


# ══════════════════════════════════════════════════════════════════════
# 13. Integration — AutoGen + All Other LEGO Pieces
# ══════════════════════════════════════════════════════════════════════

class TestAutoGenIntegration:
    """Test AutoGen works alongside all other LEGO pieces."""

    def test_with_model_router(self):
        from ai_earth.model_router import ModelRouter
        from autogen_core.models import UserMessage
        router = ModelRouter()
        router.configure()  # Real LLM
        assert router.info()["real_llm"] is True
        msg = UserMessage(content="test", source="user")
        assert msg.content == "test"

    def test_with_langgraph(self):
        from langgraph.graph.state import StateGraph
        from autogen_core.models import UserMessage
        from typing import TypedDict
        class S(TypedDict): x: int
        sg = StateGraph(S)
        msg = UserMessage(content="hello", source="user")
        assert sg is not None
        assert msg.content == "hello"

    def test_with_dspy(self):
        from dspy.primitives.example import Example
        from autogen_core.tools import FunctionTool
        e = Example(question="test")
        def fn(x: str) -> str: return x
        tool = FunctionTool(fn, description="test")
        assert e.question == "test"
        assert tool is not None

    def test_with_mem0(self):
        from mem0.configs.base import MemoryConfig
        from autogen_core.memory import ListMemory
        mc = MemoryConfig()
        lm = ListMemory()
        assert mc is not None
        assert lm is not None

    def test_with_crewai(self):
        from crewai import Process
        from autogen_agentchat.teams import RoundRobinGroupChat
        assert Process.sequential.value == "sequential"
        assert RoundRobinGroupChat is not None
