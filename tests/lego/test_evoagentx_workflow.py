"""
Tests for LEGO E3: EvoAgentX Workflow Engine
Source: arXiv:2507.03616 (EMNLP 2025, 3.1K stars)
Code: copied verbatim from EvoAgentX/EvoAgentX

These tests verify the workflow engine LEGO pieces work correctly.
Note: evoagentx has complex dependencies (tkinter, tree-sitter) so
tests are xfail in environments without GUI support.
"""
import sys
import pytest

sys.path.insert(0, 'ai_earth/lego')

# Mark all tests as xfail if tkinter/tree-sitter not available
pytestmark = pytest.mark.xfail(
    reason="evoagentx needs tkinter/tree-sitter — GUI dep not in server env",
    raises=(ImportError, ModuleNotFoundError),
)

class TestEvoAgentXImports:
    def test_workflow_graph_imports(self):
        try:
            from evoagentx.workflow.workflow_graph import (
                WorkFlowGraph, WorkFlowNode, WorkFlowEdge, WorkFlowNodeState,
                SequentialWorkFlowGraph
            )
            assert WorkFlowGraph is not None
        except (ImportError, ModuleNotFoundError) as e:
            pytest.skip(f"evoagentx not available: {e}")

    def test_action_imports(self):
        try:
            from evoagentx.actions.action import Action, ActionInput, ActionOutput
            assert Action is not None
        except (ImportError, ModuleNotFoundError) as e:
            pytest.skip(f"evoagentx not available: {e}")

    def test_core_imports(self):
        try:
            from evoagentx.core.base_config import Parameter
            from evoagentx.core.module import BaseModule
            assert Parameter is not None
        except (ImportError, ModuleNotFoundError) as e:
            pytest.skip(f"evoagentx not available: {e}")

    def test_workflow_node_creation(self):
        try:
            from evoagentx.workflow.workflow_graph import WorkFlowNode, WorkFlowNodeState
            node = WorkFlowNode(
                name="test_node",
                description="Test",
                inputs=[],
                outputs=[],
                prompt="test",
                parse_mode="str",
            )
            assert node.name == "test_node"
            assert node.status == WorkFlowNodeState.PENDING
        except (ImportError, ModuleNotFoundError) as e:
            pytest.skip(f"evoagentx not available: {e}")

    def test_sequential_graph_creation(self):
        try:
            from evoagentx.workflow.workflow_graph import SequentialWorkFlowGraph
            tasks = [{
                "name": "step1",
                "description": "First step",
                "inputs": [{"name": "data", "type": "string", "required": True, "description": "Input"}],
                "outputs": [{"name": "result", "type": "string", "required": True, "description": "Output"}],
                "prompt": "Process {data}",
                "parse_mode": "str",
            }]
            wf = SequentialWorkFlowGraph(goal="Test", tasks=tasks)
            assert len(wf.nodes) == 1
        except (ImportError, ModuleNotFoundError) as e:
            pytest.skip(f"evoagentx not available: {e}")
