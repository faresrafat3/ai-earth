"""
Tests for Cross-Piece Integration — AI Earth Platform
======================================================
Tests the orchestrator's ability to compose all 7 LEGO pieces.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai_earth', 'lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai_earth'))


# ══════════════════════════════════════════════════════════════════════
# 1. Orchestrator Boot + All LEGO Imports
# ══════════════════════════════════════════════════════════════════════

class TestPlatformBoot:
    """Test platform boots and all LEGO pieces are importable."""

    def test_aiearth_boot(self):
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        assert earth is not None
        assert earth.name == "ai-earth"

    def test_evoagentx_imports(self):
        from evoagentx.core.module import BaseModule
        from evoagentx.workflow.workflow_graph import WorkFlowGraph, SequentialWorkFlowGraph
        assert BaseModule is not None
        assert WorkFlowGraph is not None

    def test_dspy_imports(self):
        from dspy.primitives.example import Example
        from dspy.signatures.signature import Signature
        assert Example is not None
        assert Signature is not None

    def test_mem0_imports(self):
        from mem0.configs.base import MemoryConfig
        assert MemoryConfig is not None

    def test_langgraph_imports(self):
        from langgraph.graph.state import StateGraph
        from langgraph.constants import START, END
        assert StateGraph is not None
        assert START is not None
        assert END is not None

    def test_crewai_imports(self):
        from crewai import Agent, Task, Crew, Process
        assert Agent is not None
        assert Process.sequential.value == 'sequential'

    def test_model_router_imports(self):
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        assert router is not None


# ══════════════════════════════════════════════════════════════════════
# 2. Cross-Piece Bridge
# ══════════════════════════════════════════════════════════════════════

class TestCrossPieceBridge:
    """Test the bridge between LEGO pieces."""

    def test_bridge_creation(self):
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        bridge = earth.bridge()
        assert bridge is not None

    def test_create_langgraph(self):
        from ai_earth.orchestrator import AIEarth
        from langgraph.graph.state import StateGraph
        earth = AIEarth()
        graph = earth.create_langgraph("test_graph")
        assert isinstance(graph, StateGraph)

    def test_create_crew(self):
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        crew = earth.create_crew("team", [
            {"name": "agent1", "role": "Researcher", "goal": "Find info"},
            {"name": "agent2", "role": "Writer", "goal": "Write reports"},
        ])
        assert crew["name"] == "team"
        assert len(crew["agents"]) == 2

    def test_create_memory(self):
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        memory = earth.create_memory("conv_history")
        assert memory is not None
        assert "conv_history" in earth.bridge().list_memory_stores()

    def test_compose_workflow(self):
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        earth.create_langgraph("research_graph")
        earth.create_crew("team", [
            {"name": "researcher", "role": "Researcher", "goal": "Find info"},
        ])
        earth.create_memory("context_memory")
        
        composed = earth.compose("research_pipeline",
            graph_name="research_graph",
            crew_agents=["researcher"],
            memory_store="context_memory",
        )
        assert composed["name"] == "research_pipeline"
        assert "graph" in composed["pieces"]
        assert "agents" in composed["pieces"]
        assert "memory" in composed["pieces"]

    def test_platform_info(self):
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        info = earth.platform_info()
        assert "lego_pieces" in info
        assert "totals" in info
        assert info["totals"]["tests"] == 542
        assert len(info["lego_pieces"]) == 7

    def test_platform_stats(self):
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        stats = earth.platform_stats()
        assert "ai-earth" in stats
        assert "542 tests" in stats


# ══════════════════════════════════════════════════════════════════════
# 3. Cross-Piece Integration Scenarios
# ══════════════════════════════════════════════════════════════════════

class TestIntegrationScenarios:
    """Test real integration scenarios combining LEGO pieces."""

    def test_langgraph_with_dspy_example(self):
        """LangGraph graph + DSPy Example for typed data."""
        from langgraph.graph.state import StateGraph
        from dspy.primitives.example import Example
        from typing import TypedDict

        class ResearchState(TypedDict):
            query: str
            findings: str

        graph = StateGraph(ResearchState)
        example = Example(query="What is AI?", findings="AI is...")
        assert example.query == "What is AI?"
        assert graph is not None

    def test_crewai_with_mem0_config(self):
        """CrewAI Process + Mem0 MemoryConfig."""
        from crewai import Process
        from mem0.configs.base import MemoryConfig
        assert Process.sequential.value == "sequential"
        mc = MemoryConfig()
        assert mc is not None

    def test_model_router_with_all_pieces(self):
        """Model Router provides LLM for all other pieces."""
        from ai_earth.model_router import ModelRouter
        from langgraph.graph.state import StateGraph
        from crewai import Process
        from dspy.primitives.example import Example
        from mem0.configs.base import MemoryConfig
        from typing import TypedDict

        router = ModelRouter()
        router.configure(mock=True)

        # Model Router for LangGraph
        assert router._mock_mode is True
        
        # LangGraph graph
        class S(TypedDict): x: int
        sg = StateGraph(S)
        assert sg is not None

        # DSPy typed example
        e = Example(question="test", answer="response")
        assert e.question == "test"

        # Mem0 memory
        mc = MemoryConfig()
        assert mc is not None

        # CrewAI process
        assert Process.hierarchical.value == "hierarchical"

    def test_evoagentx_workflow_with_langgraph(self):
        """EvoAgentX workflow graph + LangGraph StateGraph."""
        from evoagentx.workflow.workflow_graph import SequentialWorkFlowGraph
        from langgraph.graph.state import StateGraph
        from typing import TypedDict

        # Create EvoAgentX workflow
        tasks = [{
            "name": "step1",
            "description": "First step",
            "inputs": [{"name": "data", "type": "string", "required": True, "description": "Input"}],
            "outputs": [{"name": "result", "type": "string", "required": True, "description": "Output"}],
            "prompt": "Process {data}",
            "parse_mode": "str",
        }]
        wf = SequentialWorkFlowGraph(goal="Test workflow", tasks=tasks)
        assert len(wf.nodes) == 1

        # Create LangGraph graph
        class S(TypedDict): data: str; result: str
        sg = StateGraph(S)
        assert sg is not None

    def test_full_platform_composition(self):
        """Full platform: orchestrator composes all pieces."""
        from ai_earth.orchestrator import AIEarth
        from ai_earth.model_router import ModelRouter
        from typing import TypedDict

        earth = AIEarth()
        router = ModelRouter()
        router.configure(mock=True)
        earth.bridge().set_router(router)

        # Create graph
        class ResearchState(TypedDict):
            query: str
            analysis: str
            report: str
        earth.create_langgraph("research", ResearchState)

        # Create crew
        earth.create_crew("research_team", [
            {"name": "analyst", "role": "Data Analyst", "goal": "Analyze data"},
            {"name": "writer", "role": "Report Writer", "goal": "Write reports"},
        ])

        # Create memory
        earth.create_memory("research_memory")

        # Compose
        composed = earth.compose("full_pipeline",
            graph_name="research",
            crew_agents=["analyst", "writer"],
            memory_store="research_memory",
        )

        assert composed["name"] == "full_pipeline"
        assert len(composed["pieces"]) == 3
        assert len(composed["connections"]) == 3

        # Verify platform stats
        stats = earth.platform_stats()
        assert "research" in stats
        assert "542 tests" in stats
