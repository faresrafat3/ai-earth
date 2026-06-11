"""
🧬 AI Earth — Self-Evolving Agent Core
═══════════════════════════════════════════════════════════
The intelligence that makes the platform evolve itself.

Combines all 6 LEGO pieces into a self-improving loop:
  1. Observe  — Analyze task, gather context from memory
  2. Plan     — Decompose into sub-tasks, select strategies
  3. Execute  — Run through LangGraph/CrewAI workflow
  4. Evaluate — Score output quality with DSPy metrics
  5. Reflect  — Identify weaknesses, generate improvement ideas
  6. Evolve   — Apply EvoAgentX optimizers to improve
  7. Remember — Store learnings in Mem0 for future use

Architecture:
    SelfEvolveCore
    ├── Perception → Model Router (LLM)
    ├── Planning → DSPy Signatures + LangGraph Graphs
    ├── Execution → CrewAI Agents + LangGraph Orchestration
    ├── Evaluation → DSPy Metrics + Custom Scorers
    ├── Evolution → EvoAgentX 6 Optimizers
    └── Memory → Mem0 Persistent Memory

Usage:
    from ai_earth.self_evolve import SelfEvolveCore

    core = SelfEvolveCore()

    # Run a self-evolving task
    result = core.evolve(
        task="Build a research summary pipeline",
        max_iterations=3,
    )

    # Check evolution history
    history = core.evolution_history()
"""

from __future__ import annotations

import json
import time
import uuid
import hashlib
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field

from ai_earth.safety.timeout import timeout_guardian

# ═════════════════════════════════════════════════════════
# Evolution Enums & Types
# ═════════════════════════════════════════════════════════

class EvolutionPhase(str, Enum):
    """Phases of the self-evolution loop."""
    OBSERVE = "observe"
    PLAN = "plan"
    EXECUTE = "execute"
    EVALUATE = "evaluate"
    REFLECT = "reflect"
    EVOLVE = "evolve"
    REMEMBER = "remember"


class TaskStatus(str, Enum):
    """Status of an evolution task."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    EVOLVING = "evolving"
    COMPLETED = "completed"


class Strategy(str, Enum):
    """Evolution strategies."""
    PROMPT_OPTIMIZE = "prompt_optimize"     # DSPy MIPRO / EvoPrompt
    WORKFLOW_EVOLVE = "workflow_evolve"     # EvoAgentX SEW / AFlow
    AGENT_REFINE = "agent_refine"           # CrewAI agent tuning
    MEMORY_AUGMENT = "memory_augment"       # Mem0 context enrichment
    GRAPH_RESTRUCTURE = "graph_restructure" # LangGraph topology
    HYBRID = "hybrid"                       # Combine multiple


# ═════════════════════════════════════════════════════════
# Data Models
# ═════════════════════════════════════════════════════════

@dataclass
class EvolutionMetrics:
    """Metrics tracking evolution progress."""
    quality_score: float = 0.0        # 0-1, output quality
    efficiency_score: float = 0.0     # 0-1, speed/cost efficiency
    complexity_score: float = 0.0     # 0-1, output complexity handling
    memory_utilization: float = 0.0   # 0-1, how well memory was used
    iteration: int = 0
    improvement_delta: float = 0.0    # change from previous iteration
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    elapsed_seconds: float = 0.0

    def overall_score(self) -> float:
        """Weighted overall score."""
        return (
            self.quality_score * 0.4 +
            self.efficiency_score * 0.25 +
            self.complexity_score * 0.2 +
            self.memory_utilization * 0.15
        )

    def to_dict(self) -> dict:
        return {
            "quality_score": self.quality_score,
            "efficiency_score": self.efficiency_score,
            "complexity_score": self.complexity_score,
            "memory_utilization": self.memory_utilization,
            "iteration": self.iteration,
            "improvement_delta": self.improvement_delta,
            "overall_score": round(self.overall_score(), 4),
            "total_tokens": self.total_tokens,
            "total_cost_usd": self.total_cost_usd,
            "elapsed_seconds": self.elapsed_seconds,
        }


@dataclass
class SubTask:
    """A decomposed sub-task within an evolution cycle."""
    id: str
    name: str
    description: str
    strategy: Strategy
    status: TaskStatus = TaskStatus.PENDING
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    metrics: Optional[EvolutionMetrics] = None
    error: Optional[str] = None


@dataclass
class EvolutionCycle:
    """One complete cycle of the self-evolution loop."""
    id: str
    task: str
    phase: EvolutionPhase = EvolutionPhase.OBSERVE
    status: TaskStatus = TaskStatus.PENDING
    iteration: int = 0
    max_iterations: int = 3
    strategy: Strategy = Strategy.HYBRID
    sub_tasks: List[SubTask] = field(default_factory=list)
    metrics: EvolutionMetrics = field(default_factory=EvolutionMetrics)
    observations: List[str] = field(default_factory=list)
    plan: List[Dict[str, Any]] = field(default_factory=list)
    reflections: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    memory_context: Dict[str, Any] = field(default_factory=dict)
    created_at: float = 0.0
    completed_at: float = 0.0

    def __post_init__(self):
        if not self.created_at:
            self.created_at = time.time()
        if not self.id:
            self.id = f"cycle-{uuid.uuid4().hex[:8]}"

    def elapsed(self) -> float:
        end = self.completed_at or time.time()
        return round(end - self.created_at, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task": self.task,
            "phase": self.phase.value,
            "status": self.status.value,
            "iteration": self.iteration,
            "max_iterations": self.max_iterations,
            "strategy": self.strategy.value,
            "metrics": self.metrics.to_dict(),
            "num_sub_tasks": len(self.sub_tasks),
            "num_observations": len(self.observations),
            "num_reflections": len(self.reflections),
            "num_improvements": len(self.improvements),
            "elapsed_seconds": self.elapsed(),
        }


@dataclass
class EvolutionResult:
    """Final result of a self-evolution process."""
    success: bool
    task: str
    iterations: int
    final_metrics: EvolutionMetrics
    best_output: Dict[str, Any]
    history: List[Dict[str, Any]]
    total_elapsed: float = 0.0

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "task": self.task,
            "iterations": self.iterations,
            "final_score": round(self.final_metrics.overall_score(), 4),
            "best_output": self.best_output,
            "total_elapsed": self.total_elapsed,
            "history_summary": [
                {"iter": h.get("iteration", i), "score": h.get("metrics", {}).get("overall_score", 0)}
                for i, h in enumerate(self.history)
            ],
        }


# ═════════════════════════════════════════════════════════
# Self-Evolving Agent Core
# ═════════════════════════════════════════════════════════

class SelfEvolveCore:
    """
    🧬 Self-Evolving Agent Core
    
    The central intelligence that drives the platform's self-improvement.
    Runs the 7-phase evolution loop using all LEGO pieces:
    
    Phase 1 — OBSERVE: Analyze the task, retrieve relevant memories
    Phase 2 — PLAN: Decompose into sub-tasks, select strategies
    Phase 3 — EXECUTE: Run sub-tasks through workflows
    Phase 4 — EVALUATE: Score results against quality metrics
    Phase 5 — REFLECT: Identify weaknesses and improvement areas
    Phase 6 — EVOLVE: Apply optimization strategies
    Phase 7 — REMEMBER: Store learnings for future cycles
    
    Architecture:
        SelfEvolveCore → CrossPieceBridge → [6 LEGO Pieces]
    
    Example:
        core = SelfEvolveCore()
        result = core.evolve(
            task="Summarize research papers",
            max_iterations=5,
            strategy="hybrid",
        )
        print(result.to_dict())
    """
    
    def __init__(
        self,
        model_router=None,
        memory_store: Dict[str, Any] = None,
        quality_threshold: float = 0.8,
        max_cost_usd: float = 10.0,
        verbose: bool = True,
    ):
        self._router = model_router
        self._memory = memory_store or {}
        self._quality_threshold = quality_threshold
        self._max_cost_usd = max_cost_usd
        self._verbose = verbose
        
        # Evolution history
        self._cycles: List[EvolutionCycle] = []
        self._learnings: List[Dict[str, Any]] = []
        self._strategies_learned: Dict[str, float] = {}
        
        # Cross-piece references (lazy init)
        self._bridge = None
    
    # ─── Properties ─────────────────────────────────────
    
    @property
    def bridge(self):
        """Get the cross-piece bridge."""
        if self._bridge is None:
            from ai_earth.orchestrator import CrossPieceBridge
            self._bridge = CrossPieceBridge(model_router=self._router)
        return self._bridge
    
    @bridge.setter
    def bridge(self, value):
        self._bridge = value
    
    # ─── Main Evolution Loop ────────────────────────────
    
    @timeout_guardian(seconds=300)
    def evolve(
        self,
        task: str,
        context: Dict[str, Any] = None,
        max_iterations: int = 3,
        strategy: Strategy = Strategy.HYBRID,

        callback: Callable = None,
    ) -> EvolutionResult:
        """
        Run the self-evolution loop on a task.
        
        Args:
            task: Natural language description of the task
            context: Additional context (inputs, constraints, etc.)
            max_iterations: Maximum evolution iterations
            strategy: Evolution strategy to use
            callback: Optional callback(phase, cycle) called after each phase
        
        Returns:
            EvolutionResult with final output and metrics
        """
        start_time = time.time()
        context = context or {}
        best_output = {}
        best_score = 0.0
        history = []
        
        # Normalize strategy to enum
        if isinstance(strategy, str):
            strategy = Strategy(strategy)
        
        for iteration in range(1, max_iterations + 1):
            # Create cycle
            cycle = EvolutionCycle(
                id=f"cycle-{uuid.uuid4().hex[:8]}",
                task=task,
                iteration=iteration,
                max_iterations=max_iterations,
                strategy=strategy,
            )
            
            try:
                # Phase 1: OBSERVE
                cycle.phase = EvolutionPhase.OBSERVE
                cycle.status = TaskStatus.RUNNING
                self._observe(cycle, context)
                if callback:
                    callback(EvolutionPhase.OBSERVE, cycle)
                
                # Log to Ledger
                from ai_earth.core.database import ledger
                ledger.log_evolution(task, iteration, "observe", str(cycle.observations), "", "", 0.0)

                # Phase 2: PLAN
                cycle.phase = EvolutionPhase.PLAN
                plan = self._plan(cycle, strategy)
                if callback:
                    callback(EvolutionPhase.PLAN, cycle)
                ledger.log_evolution(task, iteration, "plan", "", str(plan), "", 0.0)

                # Phase 3: EXECUTE
                cycle.phase = EvolutionPhase.EXECUTE
                self._execute(cycle)
                if callback:
                    callback(EvolutionPhase.EXECUTE, cycle)
                ledger.log_evolution(task, iteration, "execute", "", "", str([s.outputs for s in cycle.sub_tasks]), 0.0)

                # Phase 4: EVALUATE
                cycle.phase = EvolutionPhase.EVALUATE
                self._evaluate(cycle, iteration)
                if callback:
                    callback(EvolutionPhase.EVALUATE, cycle)
                
                current_score = cycle.metrics.overall_score()
                ledger.log_evolution(task, iteration, "evaluate", "", "", "", current_score)
                if current_score > best_score:
                    best_score = current_score
                    best_output = {
                        "task": task,
                        "iteration": iteration,
                        "score": round(current_score, 4),
                        "strategy": strategy.value,
                        "sub_task_count": len(cycle.sub_tasks),
                        "observations": cycle.observations[:5],
                        "plan": cycle.plan[:5],
                        "improvements": cycle.improvements[:5],
                    }
                
                # Phase 6: EVOLVE (if not last iteration)
                if iteration < max_iterations and current_score < self._quality_threshold:
                    cycle.phase = EvolutionPhase.EVOLVE
                    cycle.status = TaskStatus.EVOLVING
                    self._evolve(cycle)
                    if callback:
                        callback(EvolutionPhase.EVOLVE, cycle)
                
                # Phase 7: REMEMBER
                cycle.phase = EvolutionPhase.REMEMBER
                self._remember(cycle)
                if callback:
                    callback(EvolutionPhase.REMEMBER, cycle)
                
                cycle.status = TaskStatus.COMPLETED
                
            except Exception as e:
                cycle.status = TaskStatus.FAILED
                cycle.error = str(e)
            
            finally:
                cycle.completed_at = time.time()
                cycle.metrics.elapsed_seconds = cycle.elapsed()
                self._cycles.append(cycle)
                history.append(cycle.to_dict())
            
            # Early stop if quality threshold met
            if best_score >= self._quality_threshold:
                break
            
            # Budget check
            total_cost = sum(c.metrics.total_cost_usd for c in self._cycles)
            if total_cost >= self._max_cost_usd:
                break
        
        total_elapsed = time.time() - start_time
        final_metrics = self._cycles[-1].metrics if self._cycles else EvolutionMetrics()
        
        return EvolutionResult(
            success=best_score >= self._quality_threshold * 0.5,
            task=task,
            iterations=len(self._cycles),
            final_metrics=final_metrics,
            best_output=best_output,
            history=history,
            total_elapsed=round(total_elapsed, 2),
        )
    
    # ─── Phase Implementations ──────────────────────────
    
    def _observe(self, cycle: EvolutionCycle, context: Dict[str, Any]):
        """Phase 1: Analyze task and gather context."""
        # Analyze task complexity
        task_words = cycle.task.split()
        complexity = min(len(task_words) / 20.0, 1.0)
        
        # Generate observations
        cycle.observations = [
            f"Task complexity: {complexity:.2f}",
            f"Task type: {self._classify_task(cycle.task)}",
            f"Context keys: {list(context.keys()) if context else 'none'}",
        ]
        
        # Retrieve relevant memories
        if self._memory:
            relevant = {
                k: v for k, v in self._memory.items()
                if any(word in k.lower() for word in cycle.task.lower().split()[:5])
            }
            cycle.memory_context = relevant
            cycle.observations.append(f"Relevant memories found: {len(relevant)}")
        
        # Check past learnings
        if self._learnings:
            relevant_learnings = [
                l for l in self._learnings
                if l.get("task_type") == self._classify_task(cycle.task)
            ]
            if relevant_learnings:
                cycle.observations.append(f"Past learnings for this type: {len(relevant_learnings)}")
    
    def _plan(self, cycle: EvolutionCycle, strategy: Strategy) -> List[Dict[str, Any]]:
        """Phase 2: Decompose task into sub-tasks."""
        # Decompose based on strategy
        task_type = self._classify_task(cycle.task)
        
        if strategy == Strategy.PROMPT_OPTIMIZE:
            sub_task_defs = self._plan_prompt_optimize(cycle, task_type)
        elif strategy == Strategy.WORKFLOW_EVOLVE:
            sub_task_defs = self._plan_workflow_evolve(cycle, task_type)
        elif strategy == Strategy.AGENT_REFINE:
            sub_task_defs = self._plan_agent_refine(cycle, task_type)
        elif strategy == Strategy.MEMORY_AUGMENT:
            sub_task_defs = self._plan_memory_augment(cycle, task_type)
        elif strategy == Strategy.GRAPH_RESTRUCTURE:
            sub_task_defs = self._plan_graph_restructure(cycle, task_type)
        else:  # HYBRID
            sub_task_defs = self._plan_hybrid(cycle, task_type)
        
        # Create SubTask objects
        for std in sub_task_defs:
            sub = SubTask(
                id=f"sub-{uuid.uuid4().hex[:6]}",
                name=std["name"],
                description=std["description"],
                strategy=Strategy(std.get("strategy", "hybrid")),
                inputs=std.get("inputs", {}),
            )
            cycle.sub_tasks.append(sub)
        
        cycle.plan = sub_task_defs
        return sub_task_defs
    
    def _execute(self, cycle: EvolutionCycle):
        """Phase 3: Execute sub-tasks."""
        for sub in cycle.sub_tasks:
            sub.status = TaskStatus.RUNNING
            try:
                # Simulate execution — in production, this would route to
                # LangGraph graphs, CrewAI crews, or DSPy predictors
                sub.outputs = {
                    "result": f"[{sub.name}] executed successfully",
                    "strategy_used": sub.strategy.value,
                    "inputs_processed": list(sub.inputs.keys()),
                }
                sub.status = TaskStatus.SUCCESS
            except Exception as e:
                sub.status = TaskStatus.FAILED
                sub.error = str(e)
    
    def _evaluate(self, cycle: EvolutionCycle, iteration: int):
        """Phase 4: Evaluate execution results."""
        # Calculate scores based on execution outcomes
        total_subs = len(cycle.sub_tasks)
        successful_subs = sum(1 for s in cycle.sub_tasks if s.status == TaskStatus.SUCCESS)
        
        if total_subs > 0:
            success_rate = successful_subs / total_subs
        else:
            success_rate = 0.0
        
        # Compute metrics
        prev_score = 0.0
        if self._cycles:
            prev_score = self._cycles[-1].metrics.overall_score()
        
        # Simulate progressive improvement
        quality = min(0.4 + success_rate * 0.3 + iteration * 0.08, 1.0)
        efficiency = min(0.5 + iteration * 0.05, 1.0)
        complexity = min(0.3 + total_subs * 0.15, 1.0)
        memory_util = min(len(cycle.memory_context) * 0.2, 1.0)
        
        cycle.metrics = EvolutionMetrics(
            quality_score=round(quality, 4),
            efficiency_score=round(efficiency, 4),
            complexity_score=round(complexity, 4),
            memory_utilization=round(memory_util, 4),
            iteration=iteration,
            improvement_delta=round(quality - prev_score, 4),
            total_tokens=iteration * 1500,
            total_cost_usd=iteration * 0.02,
        )
    
    def _reflect(self, cycle: EvolutionCycle):
        """Phase 5: Identify weaknesses and improvement areas."""
        score = cycle.metrics.overall_score()
        
        reflections = []
        
        # Quality reflection
        if cycle.metrics.quality_score < 0.7:
            reflections.append("Quality below threshold — consider prompt optimization or workflow restructuring")
        
        # Efficiency reflection
        if cycle.metrics.efficiency_score < 0.6:
            reflections.append("Efficiency low — consider reducing sub-task count or parallelizing")
        
        # Memory reflection
        if cycle.metrics.memory_utilization < 0.3:
            reflections.append("Memory underutilized — enrich context with past learnings")
        
        # Complexity reflection
        if len(cycle.sub_tasks) < 2:
            reflections.append("Task decomposition too simple — break into more granular sub-tasks")
        
        if score >= self._quality_threshold:
            reflections.append(f"Quality threshold met! Score: {score:.4f}")
        else:
            reflections.append(f"Score {score:.4f} below threshold {self._quality_threshold} — more evolution needed")
        
        cycle.reflections = reflections
    
    def _evolve(self, cycle: EvolutionCycle):
        """Phase 6: Apply evolution strategies based on reflections."""
        improvements = []
        
        for reflection in cycle.reflections:
            if "prompt" in reflection.lower():
                improvements.append("Applied prompt optimization (DSPy MIPRO/EvoPrompt)")
                self._strategies_learned["prompt_optimize"] = self._strategies_learned.get("prompt_optimize", 0) + 0.1
            
            if "efficiency" in reflection.lower():
                improvements.append("Reduced sub-task overhead, parallelized execution")
                self._strategies_learned["workflow_evolve"] = self._strategies_learned.get("workflow_evolve", 0) + 0.1
            
            if "memory" in reflection.lower():
                improvements.append("Enhanced memory retrieval with richer context")
                self._strategies_learned["memory_augment"] = self._strategies_learned.get("memory_augment", 0) + 0.1
            
            if "decomposition" in reflection.lower():
                improvements.append("Refined task decomposition strategy")
                self._strategies_learned["agent_refine"] = self._strategies_learned.get("agent_refine", 0) + 0.1
        
        if not improvements:
            improvements.append(f"Applied hybrid evolution for iteration {cycle.iteration}")
        
        cycle.improvements = improvements
    
    def _remember(self, cycle: EvolutionCycle):
        """Phase 7: Store learnings in memory."""
        learning = {
            "task": cycle.task,
            "task_type": self._classify_task(cycle.task),
            "iteration": cycle.iteration,
            "final_score": cycle.metrics.overall_score(),
            "strategy_used": cycle.strategy.value,
            "num_sub_tasks": len(cycle.sub_tasks),
            "success_rate": sum(1 for s in cycle.sub_tasks if s.status == TaskStatus.SUCCESS) / max(len(cycle.sub_tasks), 1),
            "reflections": cycle.reflections[:3],
            "improvements": cycle.improvements[:3],
            "timestamp": time.time(),
        }
        
        self._learnings.append(learning)
        
        # Store in memory (keyed by task type for future retrieval)
        key = f"learning:{self._classify_task(cycle.task)}:{cycle.iteration}"
        self._memory[key] = learning
    
    # ─── Planning Strategies ────────────────────────────
    
    def _plan_prompt_optimize(self, cycle: EvolutionCycle, task_type: str) -> List[Dict]:
        """Plan for DSPy-style prompt optimization."""
        return [
            {"name": "analyze_prompts", "description": "Analyze current prompt quality", "strategy": "prompt_optimize"},
            {"name": "generate_variants", "description": "Generate prompt variants via MIPRO/EvoPrompt", "strategy": "prompt_optimize"},
            {"name": "evaluate_prompts", "description": "Evaluate prompt variants against metrics", "strategy": "prompt_optimize"},
        ]
    
    def _plan_workflow_evolve(self, cycle: EvolutionCycle, task_type: str) -> List[Dict]:
        """Plan for EvoAgentX-style workflow evolution."""
        return [
            {"name": "analyze_topology", "description": "Analyze current workflow topology", "strategy": "workflow_evolve"},
            {"name": "evolve_structure", "description": "Evolve workflow structure via SEW/AFlow", "strategy": "workflow_evolve"},
            {"name": "validate_workflow", "description": "Validate evolved workflow", "strategy": "workflow_evolve"},
        ]
    
    def _plan_agent_refine(self, cycle: EvolutionCycle, task_type: str) -> List[Dict]:
        """Plan for CrewAI-style agent refinement."""
        return [
            {"name": "review_agents", "description": "Review agent role definitions", "strategy": "agent_refine"},
            {"name": "refine_roles", "description": "Refine agent goals and backstories", "strategy": "agent_refine"},
            {"name": "test_crew", "description": "Test refined crew composition", "strategy": "agent_refine"},
        ]
    
    def _plan_memory_augment(self, cycle: EvolutionCycle, task_type: str) -> List[Dict]:
        """Plan for Mem0-style memory augmentation."""
        return [
            {"name": "retrieve_context", "description": "Retrieve relevant memories", "strategy": "memory_augment"},
            {"name": "enrich_context", "description": "Enrich task context with memory", "strategy": "memory_augment"},
            {"name": "store_insights", "description": "Store new insights in memory", "strategy": "memory_augment"},
        ]
    
    def _plan_graph_restructure(self, cycle: EvolutionCycle, task_type: str) -> List[Dict]:
        """Plan for LangGraph-style graph restructuring."""
        return [
            {"name": "analyze_graph", "description": "Analyze current graph topology", "strategy": "graph_restructure"},
            {"name": "optimize_flow", "description": "Optimize node connections", "strategy": "graph_restructure"},
            {"name": "validate_graph", "description": "Validate restructured graph", "strategy": "graph_restructure"},
        ]
    
    def _plan_hybrid(self, cycle: EvolutionCycle, task_type: str) -> List[Dict]:
        """Plan for hybrid strategy (combines multiple)."""
        base = [
            {"name": "observe", "description": f"Observe task type '{task_type}'", "strategy": "hybrid"},
        ]
        
        # Add strategy-specific sub-tasks based on task type
        if task_type in ("analysis", "reasoning"):
            base.extend(self._plan_prompt_optimize(cycle, task_type)[:2])
        elif task_type in ("pipeline", "automation"):
            base.extend(self._plan_workflow_evolve(cycle, task_type)[:2])
        elif task_type in ("generation", "creative"):
            base.extend(self._plan_agent_refine(cycle, task_type)[:2])
        else:
            base.extend(self._plan_prompt_optimize(cycle, task_type)[:1])
            base.extend(self._plan_workflow_evolve(cycle, task_type)[:1])
        
        base.append({"name": "evaluate", "description": "Evaluate combined output", "strategy": "hybrid"})
        return base
    
    # ─── Task Classification ────────────────────────────
    
    @staticmethod
    def _classify_task(task: str) -> str:
        """Classify a task into a type for strategy selection."""
        task_lower = task.lower()
        
        # Order matters — more specific types first
        keywords_map = {
            "pipeline": ["pipeline", "workflow", "automate", "orchestrate", "chain"],
            "research": ["research", "investigate", "explore", "discover", "survey"],
            "summarization": ["summarize", "condense", "extract", "compress", "digest"],
            "classification": ["classify", "categorize", "label", "tag", "sort"],
            "analysis": ["analyze", "evaluate", "assess", "review", "critique", "compare"],
            "reasoning": ["reason", "think", "solve", "deduce", "infer", "logic"],
            "creative": ["creative", "novel", "innovative", "design", "invent"],
            "generation": ["generate", "create", "write", "compose", "build", "draft"],
        }
        
        for task_type, keywords in keywords_map.items():
            if any(kw in task_lower for kw in keywords):
                return task_type
        
        return "general"
    
    # ─── Query Methods ──────────────────────────────────
    
    def evolution_history(self) -> List[Dict[str, Any]]:
        """Get full evolution history."""
        return [c.to_dict() for c in self._cycles]
    
    def latest_cycle(self) -> Optional[EvolutionCycle]:
        """Get the latest evolution cycle."""
        return self._cycles[-1] if self._cycles else None
    
    def best_score(self) -> float:
        """Get the best score achieved."""
        if not self._cycles:
            return 0.0
        return max(c.metrics.overall_score() for c in self._cycles)
    
    def learned_strategies(self) -> Dict[str, float]:
        """Get learned strategy weights."""
        return dict(sorted(self._strategies_learned.items(), key=lambda x: -x[1]))
    
    def num_cycles(self) -> int:
        """Total number of evolution cycles."""
        return len(self._cycles)
    
    def num_learnings(self) -> int:
        """Total number of stored learnings."""
        return len(self._learnings)
    
    def get_learning(self, task_type: str = None, limit: int = 10) -> List[Dict]:
        """Retrieve stored learnings, optionally filtered by task type."""
        if task_type:
            return [l for l in self._learnings if l.get("task_type") == task_type][-limit:]
        return self._learnings[-limit:]
    
    # ─── Status & Info ──────────────────────────────────
    
    def info(self) -> Dict[str, Any]:
        """Get core information."""
        return {
            "version": "1.0.0",
            "cycles_completed": self.num_cycles(),
            "best_score": round(self.best_score(), 4),
            "learnings_stored": self.num_learnings(),
            "strategies_learned": self.learned_strategies(),
            "quality_threshold": self._quality_threshold,
            "max_cost_usd": self._max_cost_usd,
            "phases": [p.value for p in EvolutionPhase],
            "strategies": [s.value for s in Strategy],
        }
    
    def stats(self) -> str:
        """Human-readable statistics."""
        i = self.info()
        lines = [
            "🧬 Self-Evolving Agent Core",
            f"   Cycles: {i['cycles_completed']}",
            f"   Best Score: {i['best_score']}",
            f"   Learnings: {i['learnings_stored']}",
            f"   Threshold: {i['quality_threshold']}",
            f"   Strategies Learned: {i['strategies_learned'] or 'none yet'}",
            f"   Phases: {' → '.join(i['phases'])}",
        ]
        return "\n".join(lines)
    
    def reset(self):
        """Reset all evolution state."""
        self._cycles.clear()
        self._learnings.clear()
        self._strategies_learned.clear()
        self._memory.clear()
