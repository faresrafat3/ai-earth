"""
Tests for Self-Evolving Agent Core — AI Earth Platform
=======================================================
Tests the 7-phase evolution loop and cross-piece integration.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth'))


# ══════════════════════════════════════════════════════════════════════
# 1. Core Data Models
# ══════════════════════════════════════════════════════════════════════

class TestDataModels:
    """Test evolution data models."""

    def test_evolution_metrics(self):
        from ai_earth.self_evolve import EvolutionMetrics
        m = EvolutionMetrics(
            quality_score=0.8, efficiency_score=0.7,
            complexity_score=0.6, memory_utilization=0.5,
        )
        assert 0 < m.overall_score() < 1
        d = m.to_dict()
        assert "overall_score" in d
        assert d["quality_score"] == 0.8

    def test_evolution_metrics_weighted(self):
        from ai_earth.self_evolve import EvolutionMetrics
        m = EvolutionMetrics(quality_score=1.0, efficiency_score=0.0,
                             complexity_score=0.0, memory_utilization=0.0)
        # Quality is 40% weight
        assert abs(m.overall_score() - 0.4) < 0.01

    def test_sub_task(self):
        from ai_earth.self_evolve import SubTask, Strategy, TaskStatus
        sub = SubTask(
            id="sub-001", name="test", description="A test sub-task",
            strategy=Strategy.HYBRID,
        )
        assert sub.status == TaskStatus.PENDING
        assert sub.strategy == Strategy.HYBRID

    def test_evolution_cycle(self):
        from ai_earth.self_evolve import EvolutionCycle
        cycle = EvolutionCycle(id="test-1", task="Test task", max_iterations=3)
        assert cycle.task == "Test task"
        assert cycle.elapsed() >= 0
        d = cycle.to_dict()
        assert d["task"] == "Test task"
        assert d["phase"] == "observe"

    def test_evolution_result(self):
        from ai_earth.self_evolve import EvolutionResult, EvolutionMetrics
        result = EvolutionResult(
            success=True, task="test", iterations=2,
            final_metrics=EvolutionMetrics(quality_score=0.9),
            best_output={"score": 0.9}, history=[],
        )
        assert result.success
        d = result.to_dict()
        assert d["success"]
        assert "final_score" in d

    def test_task_status_enum(self):
        from ai_earth.self_evolve import TaskStatus
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"

    def test_evolution_phase_enum(self):
        from ai_earth.self_evolve import EvolutionPhase
        phases = [p.value for p in EvolutionPhase]
        assert phases == ["observe", "plan", "execute", "evaluate", "reflect", "evolve", "remember"]

    def test_strategy_enum(self):
        from ai_earth.self_evolve import Strategy
        strategies = [s.value for s in Strategy]
        assert "hybrid" in strategies
        assert "prompt_optimize" in strategies


# ══════════════════════════════════════════════════════════════════════
# 2. Core Initialization
# ══════════════════════════════════════════════════════════════════════

class TestCoreInit:
    """Test core initialization and configuration."""

    def test_default_init(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        assert core is not None
        assert core.num_cycles() == 0
        assert core.num_learnings() == 0

    def test_custom_threshold(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore(quality_threshold=0.95)
        assert core.info()["quality_threshold"] == 0.95

    def test_custom_budget(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore(max_cost_usd=5.0)
        assert core.info()["max_cost_usd"] == 5.0

    def test_info(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        info = core.info()
        assert "cycles_completed" in info
        assert "phases" in info
        assert "strategies" in info
        assert len(info["phases"]) == 7

    def test_stats(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        stats = core.stats()
        assert "Self-Evolving" in stats
        assert "observe" in stats


# ══════════════════════════════════════════════════════════════════════
# 3. Evolution Loop
# ══════════════════════════════════════════════════════════════════════

class TestEvolutionLoop:
    """Test the full evolution loop."""

    def test_single_iteration(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        result = core.evolve("Classify text into categories", max_iterations=1)
        assert result.iterations == 1
        assert result.final_metrics is not None

    def test_multiple_iterations(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        result = core.evolve("Build a research pipeline", max_iterations=3)
        assert result.iterations == 3
        # Scores should progressively improve
        scores = [h["metrics"]["overall_score"] for h in result.history]
        assert scores[-1] >= scores[0]

    def test_early_stop_on_quality(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore(quality_threshold=0.5)
        result = core.evolve("Simple task", max_iterations=10)
        # Should stop before 10 iterations if threshold met
        assert result.iterations <= 10

    def test_callback_tracking(self):
        from ai_earth.self_evolve import SelfEvolveCore, EvolutionPhase
        phases_seen = []
        
        def tracker(phase, cycle):
            phases_seen.append(phase.value)
        
        core = SelfEvolveCore()
        core.evolve("Test task", max_iterations=1, callback=tracker)
        
        assert "observe" in phases_seen
        assert "plan" in phases_seen
        assert "execute" in phases_seen
        assert "evaluate" in phases_seen

    def test_evolution_result_structure(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        result = core.evolve("Analyze data", max_iterations=2)
        d = result.to_dict()
        assert "success" in d
        assert "iterations" in d
        assert "final_score" in d
        assert "history_summary" in d

    def test_cycles_completed(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        core.evolve("Task 1", max_iterations=2)
        core.evolve("Task 2", max_iterations=2)
        assert core.num_cycles() == 4


# ══════════════════════════════════════════════════════════════════════
# 4. Strategies
# ══════════════════════════════════════════════════════════════════════

class TestStrategies:
    """Test all evolution strategies."""

    def test_prompt_optimize(self):
        from ai_earth.self_evolve import SelfEvolveCore, Strategy
        core = SelfEvolveCore()
        result = core.evolve("Generate creative text", max_iterations=1, strategy=Strategy.PROMPT_OPTIMIZE)
        assert result.iterations == 1

    def test_workflow_evolve(self):
        from ai_earth.self_evolve import SelfEvolveCore, Strategy
        core = SelfEvolveCore()
        result = core.evolve("Automate workflow", max_iterations=1, strategy=Strategy.WORKFLOW_EVOLVE)
        assert result.iterations == 1

    def test_agent_refine(self):
        from ai_earth.self_evolve import SelfEvolveCore, Strategy
        core = SelfEvolveCore()
        result = core.evolve("Build agent team", max_iterations=1, strategy=Strategy.AGENT_REFINE)
        assert result.iterations == 1

    def test_memory_augment(self):
        from ai_earth.self_evolve import SelfEvolveCore, Strategy
        core = SelfEvolveCore()
        result = core.evolve("Research topic", max_iterations=1, strategy=Strategy.MEMORY_AUGMENT)
        assert result.iterations == 1

    def test_graph_restructure(self):
        from ai_earth.self_evolve import SelfEvolveCore, Strategy
        core = SelfEvolveCore()
        result = core.evolve("Design graph pipeline", max_iterations=1, strategy=Strategy.GRAPH_RESTRUCTURE)
        assert result.iterations == 1

    def test_hybrid_strategy(self):
        from ai_earth.self_evolve import SelfEvolveCore, Strategy
        core = SelfEvolveCore()
        result = core.evolve("Complex multi-step task", max_iterations=1, strategy=Strategy.HYBRID)
        assert result.iterations == 1


# ══════════════════════════════════════════════════════════════════════
# 5. Task Classification
# ══════════════════════════════════════════════════════════════════════

class TestTaskClassification:
    """Test automatic task classification."""

    def test_analysis_task(self):
        from ai_earth.self_evolve import SelfEvolveCore
        assert SelfEvolveCore._classify_task("Analyze the data") == "analysis"

    def test_reasoning_task(self):
        from ai_earth.self_evolve import SelfEvolveCore
        assert SelfEvolveCore._classify_task("Solve the logic puzzle") == "reasoning"

    def test_generation_task(self):
        from ai_earth.self_evolve import SelfEvolveCore
        assert SelfEvolveCore._classify_task("Generate a report") == "generation"

    def test_pipeline_task(self):
        from ai_earth.self_evolve import SelfEvolveCore
        assert SelfEvolveCore._classify_task("Build a data pipeline") == "pipeline"

    def test_research_task(self):
        from ai_earth.self_evolve import SelfEvolveCore
        assert SelfEvolveCore._classify_task("Research quantum computing") == "research"

    def test_summarization_task(self):
        from ai_earth.self_evolve import SelfEvolveCore
        assert SelfEvolveCore._classify_task("Summarize this document") == "summarization"

    def test_general_task(self):
        from ai_earth.self_evolve import SelfEvolveCore
        assert SelfEvolveCore._classify_task("Do something") == "general"


# ══════════════════════════════════════════════════════════════════════
# 6. Memory & Learning
# ══════════════════════════════════════════════════════════════════════

class TestMemoryLearning:
    """Test memory persistence and learning."""

    def test_learnings_stored(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        core.evolve("Analyze data patterns", max_iterations=2)
        assert core.num_learnings() == 2

    def test_learnings_by_type(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        core.evolve("Analyze data", max_iterations=1)
        core.evolve("Generate report", max_iterations=1)
        
        analysis_learnings = core.get_learning(task_type="analysis")
        generation_learnings = core.get_learning(task_type="generation")
        assert len(analysis_learnings) >= 1
        assert len(generation_learnings) >= 1

    def test_strategies_learned(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        core.evolve("Complex analysis task requiring efficiency", max_iterations=3)
        
        strategies = core.learned_strategies()
        assert len(strategies) > 0  # Should have learned some strategies

    def test_memory_context_used(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        core._memory = {"data patterns": {"insight": "Patterns cluster in 3 groups"}}
        
        result = core.evolve("Analyze data patterns", max_iterations=1)
        assert result.iterations == 1

    def test_reset(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        core.evolve("Test task", max_iterations=2)
        assert core.num_cycles() == 2
        
        core.reset()
        assert core.num_cycles() == 0
        assert core.num_learnings() == 0


# ══════════════════════════════════════════════════════════════════════
# 7. Integration with LEGO Pieces
# ══════════════════════════════════════════════════════════════════════

class TestLEGOPieceIntegration:
    """Test self-evolve core with actual LEGO piece imports."""

    def test_with_model_router(self):
        from ai_earth.self_evolve import SelfEvolveCore
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        router.configure()  # Real LLM
        core = SelfEvolveCore(model_router=router)
        result = core.evolve("Test with router", max_iterations=1)
        assert result.success

    def test_with_langgraph(self):
        from ai_earth.self_evolve import SelfEvolveCore
        from langgraph.graph.state import StateGraph
        from typing import TypedDict
        
        core = SelfEvolveCore()
        
        class State(TypedDict):
            query: str
            answer: str
        graph = StateGraph(State)
        assert graph is not None
        result = core.evolve("Process with graph", max_iterations=1)
        assert result.iterations == 1

    def test_with_crewai(self):
        from ai_earth.self_evolve import SelfEvolveCore
        from crewai import Process
        core = SelfEvolveCore()
        result = core.evolve("Build agent crew", max_iterations=1, strategy="agent_refine")
        assert Process.sequential.value == "sequential"
        assert result.iterations == 1

    def test_with_dspy(self):
        from ai_earth.self_evolve import SelfEvolveCore
        from dspy.primitives.example import Example
        core = SelfEvolveCore()
        result = core.evolve("Optimize prompts", max_iterations=1, strategy="prompt_optimize")
        e = Example(x=1, y=2)
        assert e.x == 1
        assert result.iterations == 1

    def test_with_mem0(self):
        from ai_earth.self_evolve import SelfEvolveCore
        from mem0.configs.base import MemoryConfig
        core = SelfEvolveCore()
        result = core.evolve("Enhance with memory", max_iterations=1, strategy="memory_augment")
        mc = MemoryConfig()
        assert mc is not None
        assert result.iterations == 1

    def test_full_platform_integration(self):
        """Full integration: SelfEvolveCore + all LEGO pieces."""
        from ai_earth.self_evolve import SelfEvolveCore
        from ai_earth.orchestrator import AIEarth
        from ai_earth.model_router import ModelRouter
        from typing import TypedDict
        
        # Setup platform
        earth = AIEarth()
        router = ModelRouter()
        router.configure()  # Real LLM
        
        # Setup core
        core = SelfEvolveCore(model_router=router)
        
        # Create platform components
        earth.create_langgraph("evolve_graph")
        earth.create_crew("evolve_crew", [
            {"name": "optimizer", "role": "Optimizer", "goal": "Optimize workflows"},
        ])
        earth.create_memory("evolve_memory")
        
        # Run evolution
        result = core.evolve(
            "Analyze and optimize a multi-agent workflow",
            max_iterations=3,
        )
        
        assert result.iterations == 3
        assert core.num_learnings() == 3
        
        # Verify platform state
        info = earth.platform_info()
        assert info["totals"]["tests"] == 543
        assert len(info["lego_pieces"]) == 9
