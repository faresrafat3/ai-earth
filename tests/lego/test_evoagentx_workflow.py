"""
Tests for LEGO E3: EvoAgentX Workflow Engine
Source: arXiv:2507.03616 (EMNLP 2025, 3.1K stars)
Code: copied verbatim from EvoAgentX/EvoAgentX

These tests verify the workflow engine LEGO pieces work correctly:
- WorkFlowNode: task representation with inputs/outputs/state
- WorkFlowEdge: directed connections between tasks
- WorkFlowGraph: full DAG workflow with NetworkX
- Action: base action class
- ActionGraph: action composition
"""

import sys
import pytest

sys.path.insert(0, 'ai_earth/lego')

from evoagentx.workflow.workflow_graph import (
    WorkFlowGraph, WorkFlowNode, WorkFlowEdge, WorkFlowNodeState,
    SequentialWorkFlowGraph
)
from evoagentx.actions.action import Action, ActionInput, ActionOutput
from evoagentx.core.base_config import Parameter
from evoagentx.core.module import BaseModule


# ═══════════════════════════════════════════
# WorkFlowNode Tests
# ═══════════════════════════════════════════

class TestWorkFlowNode:
    """Test workflow node — the fundamental task unit."""

    def test_create_node(self):
        node = WorkFlowNode(
            name="test_task",
            description="A test task",
            inputs=[Parameter(name="x", type="int", required=True, description="input")],
            outputs=[Parameter(name="y", type="int", required=True, description="output")]
        )
        assert node.name == "test_task"
        assert node.description == "A test task"
        assert len(node.inputs) == 1
        assert len(node.outputs) == 1

    def test_node_default_status_is_pending(self):
        node = WorkFlowNode(
            name="t", description="t",
            inputs=[], outputs=[]
        )
        assert node.status == WorkFlowNodeState.PENDING

    def test_node_state_transitions(self):
        node = WorkFlowNode(name="t", description="t", inputs=[], outputs=[])
        
        node.set_status(WorkFlowNodeState.RUNNING)
        assert node.status == WorkFlowNodeState.RUNNING
        assert not node.is_complete
        
        node.set_status(WorkFlowNodeState.COMPLETED)
        assert node.status == WorkFlowNodeState.COMPLETED
        assert node.is_complete

    def test_node_state_failed(self):
        node = WorkFlowNode(name="t", description="t", inputs=[], outputs=[])
        node.set_status(WorkFlowNodeState.FAILED)
        assert node.status == WorkFlowNodeState.FAILED
        assert not node.is_complete

    def test_node_get_input_names(self):
        node = WorkFlowNode(
            name="t", description="t",
            inputs=[
                Parameter(name="a", type="str", required=True, description="a"),
                Parameter(name="b", type="str", required=False, description="b")
            ],
            outputs=[]
        )
        assert node.get_input_names() == ["a", "b"]
        assert node.get_input_names(required=True) == ["a"]

    def test_node_get_output_names(self):
        node = WorkFlowNode(
            name="t", description="t", inputs=[],
            outputs=[
                Parameter(name="result", type="str", required=True, description="result")
            ]
        )
        assert node.get_output_names() == ["result"]

    def test_node_get_task_info(self):
        node = WorkFlowNode(
            name="search", description="Search papers",
            inputs=[Parameter(name="query", type="str", required=True, description="q")],
            outputs=[Parameter(name="papers", type="list", required=True, description="p")]
        )
        info = node.get_task_info()
        assert "search" in info
        assert "query" in info
        assert "papers" in info

    def test_node_get_agents_empty(self):
        node = WorkFlowNode(name="t", description="t", inputs=[], outputs=[])
        assert node.get_agents() == []

    def test_node_set_agents(self):
        node = WorkFlowNode(name="t", description="t", inputs=[], outputs=[])
        node.set_agents(["research_agent"])
        assert node.get_agents() == ["research_agent"]

    def test_node_is_basemodule(self):
        node = WorkFlowNode(name="t", description="t", inputs=[], outputs=[])
        assert isinstance(node, BaseModule)

    def test_node_serializable(self):
        node = WorkFlowNode(name="t", description="t", inputs=[], outputs=[])
        d = node.to_dict()
        assert isinstance(d, dict)
        assert d["name"] == "t"


# ═══════════════════════════════════════════
# WorkFlowEdge Tests
# ═══════════════════════════════════════════

class TestWorkFlowEdge:
    """Test workflow edges — connections between tasks."""

    def test_create_edge_from_tuple(self):
        edge = WorkFlowEdge(edge_tuple=("a", "b"))
        assert edge.source == "a"
        assert edge.target == "b"
        assert edge.priority == 0

    def test_edge_with_priority(self):
        edge = WorkFlowEdge(edge_tuple=("a", "b"), priority=5)
        assert edge.priority == 5

    def test_edge_from_kwargs(self):
        edge = WorkFlowEdge(source="x", target="y")
        assert edge.source == "x"
        assert edge.target == "y"

    def test_edge_is_basemodule(self):
        edge = WorkFlowEdge(edge_tuple=("a", "b"))
        assert isinstance(edge, BaseModule)


# ═══════════════════════════════════════════
# WorkFlowGraph Tests (DAG)
# ═══════════════════════════════════════════

class TestWorkFlowGraph:
    """Test the DAG workflow graph — the heart of the engine."""

    def _make_node(self, name, in_names=None, out_names=None):
        return WorkFlowNode(
            name=name,
            description=f"Task: {name}",
            inputs=[Parameter(name=n, type="str", required=True, description=n)
                    for n in (in_names or [])],
            outputs=[Parameter(name=n, type="str", required=True, description=n)
                     for n in (out_names or [])]
        )

    def test_create_simple_graph(self):
        n1 = self._make_node("search", out_names=["results"])
        n2 = self._make_node("analyze", in_names=["results"], out_names=["insights"])
        edge = WorkFlowEdge(edge_tuple=("search", "analyze"))
        
        graph = WorkFlowGraph(
            goal="Research pipeline",
            nodes=[n1, n2],
            edges=[edge]
        )
        
        assert graph.goal == "Research pipeline"
        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
        assert graph.graph.number_of_nodes() == 2
        assert graph.graph.number_of_edges() == 1

    def test_graph_with_branching(self):
        """A → B, A → C (fan-out)"""
        a = self._make_node("fetch", out_names=["data"])
        b = self._make_node("analyze", in_names=["data"], out_names=["stats"])
        c = self._make_node("visualize", in_names=["data"], out_names=["chart"])
        
        graph = WorkFlowGraph(
            goal="Data pipeline",
            nodes=[a, b, c],
            edges=[
                WorkFlowEdge(edge_tuple=("fetch", "analyze")),
                WorkFlowEdge(edge_tuple=("fetch", "visualize"))
            ]
        )
        
        assert graph.graph.number_of_nodes() == 3
        assert graph.graph.number_of_edges() == 2

    def test_graph_with_merge(self):
        """A → C, B → C (fan-in)"""
        a = self._make_node("web_search", out_names=["web_results"])
        b = self._make_node("db_search", out_names=["db_results"])
        c = self._make_node("merge", in_names=["web_results", "db_results"], out_names=["combined"])
        
        graph = WorkFlowGraph(
            goal="Multi-source search",
            nodes=[a, b, c],
            edges=[
                WorkFlowEdge(edge_tuple=("web_search", "merge")),
                WorkFlowEdge(edge_tuple=("db_search", "merge"))
            ]
        )
        
        assert graph.graph.number_of_nodes() == 3

    def test_graph_serialization(self):
        n1 = self._make_node("a", out_names=["x"])
        n2 = self._make_node("b", in_names=["x"], out_names=["y"])
        
        graph = WorkFlowGraph(
            goal="test",
            nodes=[n1, n2],
            edges=[WorkFlowEdge(edge_tuple=("a", "b"))]
        )
        
        config = graph.get_config()
        assert isinstance(config, dict)
        assert "goal" in config or "class_name" in config

    def test_graph_add_node(self):
        n1 = self._make_node("a")
        graph = WorkFlowGraph(goal="test", nodes=[n1], edges=[])
        
        n2 = self._make_node("b")
        graph.add_node(n2)
        
        assert len(graph.nodes) == 2

    def test_graph_infer_edges(self):
        """Edges auto-inferred from matching output→input names"""
        a = self._make_node("extract", out_names=["raw_data"])
        b = self._make_node("transform", in_names=["raw_data"], out_names=["clean_data"])
        
        graph = WorkFlowGraph(goal="ETL", nodes=[a, b])
        edges = graph._infer_edges_from_nodes([a, b])
        
        edge_names = [(e.source, e.target) for e in edges]
        assert ("extract", "transform") in edge_names

    def test_graph_get_description(self):
        n1 = self._make_node("step1", out_names=["x"])
        graph = WorkFlowGraph(goal="test", nodes=[n1], edges=[])
        
        desc = graph.get_workflow_description()
        assert "step1" in desc


# ═══════════════════════════════════════════
# Action Tests
# ═══════════════════════════════════════════

class TestAction:
    """Test the base Action class."""

    def test_action_fields(self):
        assert 'name' in Action.model_fields
        assert 'description' in Action.model_fields
        assert 'prompt' in Action.model_fields
        assert 'tools' in Action.model_fields

    def test_action_create(self):
        a = Action(name="search", description="Search the web")
        assert a.name == "search"
        assert a.prompt is None
        assert a.tools is None

    def test_action_with_prompt(self):
        a = Action(name="t", description="t", prompt="Find: {query}")
        assert a.prompt == "Find: {query}"

    def test_action_execute_raises(self):
        a = Action(name="t", description="t")
        with pytest.raises(NotImplementedError):
            a.execute()

    def test_action_async_execute_raises(self):
        import asyncio
        a = Action(name="t", description="t")
        with pytest.raises(NotImplementedError):
            asyncio.run(a.async_execute())

    def test_action_serialization(self):
        a = Action(name="t", description="test action")
        d = a.to_dict()
        assert d["name"] == "t"

    def test_action_deserialization(self):
        a = Action.from_dict({"name": "t", "description": "test"})
        assert a.name == "t"


# ═══════════════════════════════════════════
# WorkFlowNodeState Tests
# ═══════════════════════════════════════════

class TestWorkFlowNodeState:
    """Test node states."""

    def test_all_states_exist(self):
        assert WorkFlowNodeState.PENDING.value == "pending"
        assert WorkFlowNodeState.RUNNING.value == "running"
        assert WorkFlowNodeState.COMPLETED.value == "completed"
        assert WorkFlowNodeState.FAILED.value == "failed"

    def test_four_states_only(self):
        assert len(WorkFlowNodeState) == 4
