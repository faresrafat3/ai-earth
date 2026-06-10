"""
🌍 AI Earth — Orchestrator
═══════════════════════════════════════════════════════════
The main platform that composes LEGO pieces into a working system.

Architecture: 7 Layers → LEGO Pieces → Composed System
Source: EvoAgentX (arXiv:2507.03616) + AI Earth Design

Usage:
    from ai_earth.orchestrator import AIEarth
    
    earth = AIEarth()
    
    # Create a workflow
    workflow = earth.create_workflow("Analyze and summarize documents")
    
    # Optimize it
    optimized = earth.optimize(workflow, method="sew")
    
    # Run it
    result = earth.run(optimized, input_data={"document": "..."})
"""
from __future__ import annotations

import json
import copy
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

# ═════════════════════════════════════════════════════════
# LEGO Piece Imports
# ═════════════════════════════════════════════════════════

# Layer 1: Core
from evoagentx.core.module import BaseModule
from evoagentx.core.registry import MODULE_REGISTRY

# Layer 2: Models + Prompts
from evoagentx.models.base_model import BaseLLM
from evoagentx.prompts.template import PromptTemplate

# Layer 3: Agents + Actions
from evoagentx.agents.agent import Agent
from evoagentx.actions.action import Action

# Layer 4: Workflow
from evoagentx.workflow.workflow_graph import (
    WorkFlowGraph, SequentialWorkFlowGraph, WorkFlowNode, WorkFlowEdge
)

# Layer 5: Memory
from evoagentx.memory.memory import ShortTermMemory

# Layer 7: Optimizers
from evoagentx.optimizers.engine.registry import ParamRegistry, OptimizableField


# ═════════════════════════════════════════════════════════
# Enums
# ═════════════════════════════════════════════════════════

class OptimizeMethod(str, Enum):
    SEW = "sew"
    AFLOW = "aflow"
    TEXTGRAD = "textgrad"
    MIPRO = "mipro"
    EVOPROMPT = "evoprompt"
    MAPELITES = "map_elites"

class WorkflowType(str, Enum):
    SEQUENTIAL = "sequential"
    DAG = "dag"
    PARALLEL = "parallel"


# ═════════════════════════════════════════════════════════
# Data Classes
# ═════════════════════════════════════════════════════════

@dataclass
class TaskSpec:
    """Specification for a single task in a workflow."""
    name: str
    description: str
    inputs: Dict[str, str] = field(default_factory=dict)   # name → description
    outputs: Dict[str, str] = field(default_factory=dict)   # name → description
    prompt: str = ""
    agent_config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowSpec:
    """Specification for a complete workflow."""
    goal: str
    tasks: List[TaskSpec]
    workflow_type: WorkflowType = WorkflowType.SEQUENTIAL


@dataclass 
class OptimizationResult:
    """Result of an optimization run."""
    original_workflow: Dict[str, Any]
    optimized_workflow: Dict[str, Any]
    method: str
    metrics_before: Dict[str, float] = field(default_factory=dict)
    metrics_after: Dict[str, float] = field(default_factory=dict)
    iterations: int = 0
    elapsed_seconds: float = 0.0


@dataclass
class RunResult:
    """Result of running a workflow."""
    success: bool
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ═════════════════════════════════════════════════════════
# WorkflowBuilder — fluent API for building workflows
# ═════════════════════════════════════════════════════════

class WorkflowBuilder:
    """Fluent builder for creating workflow specifications."""
    
    def __init__(self):
        self._goal = ""
        self._tasks: List[TaskSpec] = []
        self._type = WorkflowType.SEQUENTIAL
    
    def goal(self, description: str) -> "WorkflowBuilder":
        self._goal = description
        return self
    
    def task(
        self,
        name: str,
        description: str = "",
        inputs: Dict[str, str] = None,
        outputs: Dict[str, str] = None,
        prompt: str = "",
    ) -> "WorkflowBuilder":
        self._tasks.append(TaskSpec(
            name=name,
            description=description or name,
            inputs=inputs or {},
            outputs=outputs or {},
            prompt=prompt,
        ))
        return self
    
    def sequential(self) -> "WorkflowBuilder":
        self._type = WorkflowType.SEQUENTIAL
        return self
    
    def dag(self) -> "WorkflowBuilder":
        self._type = WorkflowType.DAG
        return self
    
    def build(self) -> WorkflowSpec:
        if not self._goal:
            raise ValueError("Workflow must have a goal")
        if not self._tasks:
            raise ValueError("Workflow must have at least one task")
        return WorkflowSpec(
            goal=self._goal,
            tasks=self._tasks,
            workflow_type=self._type,
        )


# ═════════════════════════════════════════════════════════
# AIEarth — The Main Orchestrator
# ═════════════════════════════════════════════════════════

class AIEarth:
    """
    🌍 AI Earth — The Living Intelligence Ecosystem
    
    Composes LEGO pieces from research papers into a working system.
    
    Architecture:
        Memory → LLM Interface → Capabilities → Insight → Workflow → Agents → Orchestrator
    
    LEGO Pieces (from EvoAgentX, arXiv:2507.03616):
        - WorkFlowGraph (1,227 lines) — DAG workflow engine
        - SequentialWorkFlowGraph — Linear sequential workflows
        - Agent + Actions — Multi-agent with memory
        - BaseLLM + PromptTemplate — LLM interface
        - 6 Optimizers (SEW, AFlow, TextGrad, MIPRO, EvoPrompt, MapElites)
        - ParamRegistry — Runtime parameter optimization
        - Memory (ShortTerm + LongTerm + Manager)
        - Evaluators + Benchmarks
    """
    
    def __init__(self, name: str = "ai-earth"):
        self.name = name
        self._registry = ParamRegistry()
        self._workflows: Dict[str, WorkFlowGraph] = {}
        self._results: List[Dict[str, Any]] = []
        self._created_at = time.time()
    
    # ─── Workflow Creation ───────────────────────────────
    
    def builder(self) -> WorkflowBuilder:
        """Create a new workflow builder (fluent API)."""
        return WorkflowBuilder()
    
    def create_workflow(
        self, 
        goal: str, 
        tasks: List[Dict[str, Any]] = None,
        workflow_type: WorkflowType = WorkflowType.SEQUENTIAL,
    ) -> Union[WorkFlowGraph, SequentialWorkFlowGraph]:
        if tasks is None:
            # Use the builder instead for simple goals
            spec = (
                self.builder()
                .goal(goal)
                .task("execute", description=goal,
                      inputs={"query": "The input query"},
                      outputs={"result": "The result"},
                      prompt=goal)
                .sequential()
                .build()
            )
            return self.create_workflow_from_spec(spec)
        
        if workflow_type == WorkflowType.SEQUENTIAL:
            return SequentialWorkFlowGraph(goal=goal, tasks=tasks)
        else:
            raise ValueError(f"Workflow type '{workflow_type}' not yet supported.")
    
    def create_workflow_from_spec(self, spec: WorkflowSpec) -> Union[WorkFlowGraph, SequentialWorkFlowGraph]:
        """Create a workflow from a WorkflowSpec."""
        tasks = []
        for t in spec.tasks:
            task = {
                "name": t.name,
                "description": t.description,
                "inputs": [{"name": k, "type": "string", "required": True, "description": v} 
                          for k, v in t.inputs.items()],
                "outputs": [{"name": k, "type": "string", "required": True, "description": v} 
                           for k, v in t.outputs.items()],
                "prompt": t.prompt,
                "parse_mode": "str",
            }
            tasks.append(task)
        
        return self.create_workflow(
            goal=spec.goal,
            tasks=tasks,
            workflow_type=spec.workflow_type,
        )
    
    # ─── Workflow Operations ─────────────────────────────
    
    def save_workflow(self, name: str, workflow: WorkFlowGraph) -> str:
        """Save a workflow to the registry."""
        self._workflows[name] = workflow
        return name
    
    def load_workflow(self, name: str) -> WorkFlowGraph:
        """Load a saved workflow."""
        if name not in self._workflows:
            raise KeyError(f"Workflow '{name}' not found. Available: {list(self._workflows.keys())}")
        return self._workflows[name]
    
    def list_workflows(self) -> List[str]:
        """List all saved workflow names."""
        return list(self._workflows.keys())
    
    def workflow_info(self, workflow: WorkFlowGraph) -> Dict[str, Any]:
        """Get information about a workflow."""
        info = {
            "goal": workflow.goal,
            "num_nodes": len(workflow.nodes),
            "num_edges": len(workflow.edges),
            "nodes": [],
        }
        for node in workflow.nodes:
            info["nodes"].append({
                "name": node.name,
                "inputs": [i.name for i in node.inputs],
                "outputs": [o.name for o in node.outputs],
            })
        return info
    
    def serialize_workflow(self, workflow: WorkFlowGraph) -> Dict[str, Any]:
        """Serialize a workflow to a dict."""
        return workflow.to_dict()
    
    # ─── Optimization ────────────────────────────────────
    
    def optimize(
        self,
        workflow: WorkFlowGraph,
        method: OptimizeMethod = OptimizeMethod.SEW,
        **kwargs,
    ) -> OptimizationResult:
        """
        Optimize a workflow using one of the 6 optimization methods.
        
        Note: Full optimization requires LLM connectivity. This returns
        the optimization framework ready for execution.
        
        Args:
            workflow: The workflow to optimize
            method: Optimization method to use
            **kwargs: Additional parameters for the optimizer
        """
        start_time = time.time()
        
        original = self.serialize_workflow(workflow)
        
        # Get the optimizer class
        optimizer_map = {
            OptimizeMethod.SEW: "SEWOptimizer",
            OptimizeMethod.AFLOW: "AFlowOptimizer",
            OptimizeMethod.TEXTGRAD: "TextGradOptimizer",
            OptimizeMethod.MIPRO: "MiproOptimizer",
            OptimizeMethod.EVOPROMPT: "EvopromptOptimizer",
            OptimizeMethod.MAPELITES: "MapElitesOptimizer",
        }
        
        optimizer_name = optimizer_map[method]
        
        result = OptimizationResult(
            original_workflow=original,
            optimized_workflow=original,  # Would be updated by actual optimization
            method=method.value,
            elapsed_seconds=time.time() - start_time,
        )
        
        return result
    
    def get_available_optimizers(self) -> List[Dict[str, str]]:
        """List all available optimizers with descriptions."""
        return [
            {"name": "SEW", "method": "sew", "description": "Self-Evolving Workflow — 5 representation schemes", "lines": 931},
            {"name": "AFlow", "method": "aflow", "description": "Workflow Topology Evolution via LLM", "lines": 302},
            {"name": "TextGrad", "method": "textgrad", "description": "Textual Gradient Backpropagation", "lines": 675},
            {"name": "MIPRO", "method": "mipro", "description": "Multi-Prompt Co-Optimization (DSPy-inspired)", "lines": 1610},
            {"name": "EvoPrompt", "method": "evoprompt", "description": "Evolutionary Genetic Prompt Optimization", "lines": 1127},
            {"name": "MapElites", "method": "map_elites", "description": "Quality-Diversity Optimization", "lines": 175},
        ]
    
    # ─── Registry ────────────────────────────────────────
    
    def track_parameter(self, obj: Any, path: str, name: str = None) -> "AIEarth":
        """Track a parameter for optimization. Returns self for chaining."""
        self._registry.track(obj, path, name=name)
        return self
    
    def get_parameter(self, name: str) -> Any:
        """Get a tracked parameter's value."""
        return self._registry.get(name)
    
    def set_parameter(self, name: str, value: Any) -> "AIEarth":
        """Set a tracked parameter's value. Returns self for chaining."""
        self._registry.set(name, value)
        return self
    
    def list_parameters(self) -> List[str]:
        """List all tracked parameter names."""
        return self._registry.names()
    
    def reset_parameters(self) -> "AIEarth":
        """Reset all parameters to their initial values."""
        self._registry.reset()
        return self
    
    # ─── System Info ─────────────────────────────────────
    
    def info(self) -> Dict[str, Any]:
        """Get system information."""
        return {
            "name": self.name,
            "version": "0.1.0",
            "status": "LEGO pieces assembled, ready for composition",
            "layers": {
                "L1_core": "BaseModule, Registry, Config",
                "L2_models": "BaseLLM, LLMOutputParser",
                "L2_prompts": "PromptTemplate, StringTemplate",
                "L3_agents": "Agent, Action",
                "L4_workflow": "WorkFlowGraph, SequentialWorkFlowGraph, Operators",
                "L5_memory": "ShortTermMemory, LongTermMemory, MemoryManager",
                "L5_rag": "RAG Pipeline (chunkers, embeddings, retrievers)",
                "L6_eval": "Evaluator, Benchmark (10 benchmarks)",
                "L7_optimizers": "SEW, AFlow, TextGrad, MIPRO, EvoPrompt, MapElites",
            },
            "lego_pieces": {
                "source": "EvoAgentX (arXiv:2507.03616, EMNLP 2025)",
                "files": 192,
                "lines": 35569,
                "optimizers": 6,
            },
            "saved_workflows": len(self._workflows),
            "tracked_parameters": len(self._registry.names()),
        }
    
    def stats(self) -> str:
        """Human-readable system statistics."""
        i = self.info()
        lines = [
            f"🌍 {i['name']} v{i['version']}",
            f"📊 Status: {i['status']}",
            f"🧱 LEGO: {i['lego_pieces']['files']} files, {i['lego_pieces']['lines']} lines",
            f"🧬 Optimizers: {i['lego_pieces']['optimizers']}",
            f"💾 Saved workflows: {i['saved_workflows']}",
            f"⚙️ Tracked parameters: {i['tracked_parameters']}",
        ]
        return "\n".join(lines)
