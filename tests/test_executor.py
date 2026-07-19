"""
Tests for Real Execution Engine — AI Earth Platform
====================================================
Tests actual LEGO piece routing and execution.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth'))


class TestExecutorInit:
    """Test executor initialization."""

    def test_default_init(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        assert engine.info()["real_llm"] is True

    def test_init_with_router(self):
        from ai_earth.executor import ExecutionEngine
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        engine = ExecutionEngine(model_router=router, llm=False)
        assert engine._router is router

    def test_info(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        info = engine.info()
        assert "strategies" in info
        assert "langgraph" in info["available_pieces"]
        assert len(info["strategies"]) == 6


class TestLangGraphExecution:
    """Test LangGraph execution path."""

    def test_basic_execution(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Build a data pipeline", strategy="langgraph")
        assert result.success
        assert result.strategy == "langgraph"
        assert "result" in result.output

    def test_state_graph_compiled(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Process data through graph", strategy="langgraph")
        assert result.success
        assert "nodes" in result.metadata
        assert "process" in result.metadata["nodes"]

    def test_graph_output(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Test task", strategy="langgraph")
        assert result.output["result"] is not None
        assert len(result.output["steps"]) > 0


class TestCrewAIExecution:
    """Test CrewAI execution path."""

    def test_basic_execution(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Research AI agents", strategy="crewai")
        assert result.success
        assert result.strategy == "crewai"
        assert "agents_used" in result.output

    def test_agent_count(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Build crew for analysis", strategy="crewai")
        assert result.metadata["agent_count"] == 3


class TestAutoGenExecution:
    """Test AutoGen execution path."""

    def test_basic_execution(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Chat about AI", strategy="autogen")
        assert result.success
        assert result.strategy == "autogen"
        assert "message_created" in result.output

    def test_team_type(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Team discussion", strategy="autogen")
        assert result.output["team_type"] == "RoundRobinGroupChat"


class TestDSPyExecution:
    """Test DSPy execution path."""

    def test_basic_execution(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Predict outcome", strategy="dspy")
        assert result.success
        assert result.strategy == "dspy"
        assert "signature" in result.output

    def test_example_creation(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Classify text", strategy="dspy")
        assert "example_keys" in result.output
        assert "task" in result.output["example_keys"]


class TestHybridExecution:
    """Test hybrid multi-piece execution."""

    def test_basic_execution(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Complex multi-step task", strategy="hybrid")
        assert result.success
        assert result.strategy == "hybrid"
        assert len(result.output["pieces_used"]) >= 2

    def test_all_pieces_used(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Full pipeline", strategy="hybrid")
        pieces = result.output["pieces_used"]
        assert "langgraph" in pieces
        assert "dspy" in pieces


class TestAutoStrategy:
    """Test auto strategy selection."""

    def test_graph_task(self):
        from ai_earth.executor import ExecutionEngine, ExecStrategy
        engine = ExecutionEngine(llm=False)
        strategy = engine._classify_strategy("Build a graph pipeline")
        assert strategy == ExecStrategy.LANGGRAPH

    def test_crew_task(self):
        from ai_earth.executor import ExecutionEngine, ExecStrategy
        engine = ExecutionEngine(llm=False)
        strategy = engine._classify_strategy("Assemble a team of agents")
        assert strategy == ExecStrategy.CREWAI

    def test_chat_task(self):
        from ai_earth.executor import ExecutionEngine, ExecStrategy
        engine = ExecutionEngine(llm=False)
        strategy = engine._classify_strategy("Have a chat conversation")
        assert strategy == ExecStrategy.AUTOGEN

    def test_predict_task(self):
        from ai_earth.executor import ExecutionEngine, ExecStrategy
        engine = ExecutionEngine(llm=False)
        strategy = engine._classify_strategy("Predict the classification")
        assert strategy == ExecStrategy.DSPY

    def test_default_task(self):
        from ai_earth.executor import ExecutionEngine, ExecStrategy
        engine = ExecutionEngine(llm=False)
        strategy = engine._classify_strategy("Do something general")
        assert strategy == ExecStrategy.LANGGRAPH  # Default

    def test_auto_execution(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        result = engine.run("Build a graph workflow", strategy="auto")
        assert result.success
        assert result.strategy == "langgraph"


class TestExecResult:
    """Test ExecResult data model."""

    def test_result_to_dict(self):
        from ai_earth.executor import ExecResult
        r = ExecResult(success=True, strategy="test", output={"key": "val"})
        d = r.to_dict()
        assert d["success"]
        assert d["strategy"] == "test"
        assert d["output"]["key"] == "val"

    def test_failed_result(self):
        from ai_earth.executor import ExecResult
        r = ExecResult(success=False, strategy="test", error="something failed")
        d = r.to_dict()
        assert not d["success"]
        assert d["error"] == "something failed"


class TestExecutorHistory:
    """Test execution history tracking."""

    def test_empty_history(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        assert engine.num_executions() == 0
        assert engine.history() == []

    def test_history_after_runs(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        engine.run("Task 1", strategy="langgraph")
        engine.run("Task 2", strategy="crewai")
        assert engine.num_executions() == 2
        h = engine.history()
        assert h[0]["strategy"] == "langgraph"
        assert h[1]["strategy"] == "crewai"


class TestExecutorIntegration:
    """Test executor with all LEGO pieces."""

    def test_all_strategies_succeed(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm=False)
        
        for strat in ["langgraph", "crewai", "autogen", "dspy", "hybrid"]:
            result = engine.run(f"Test {strat}", strategy=strat)
            assert result.success, f"{strat} failed: {result.error}"

    def test_with_model_router(self):
        from ai_earth.executor import ExecutionEngine
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        router.configure()  # Real LLM
        engine = ExecutionEngine(model_router=router, llm=False)
        result = engine.run("Test with router", strategy="langgraph")
        assert result.success

    def test_cross_piece_composition(self):
        """Test that execution works with cross-piece bridge."""
        from ai_earth.executor import ExecutionEngine
        from ai_earth.orchestrator import AIEarth
        
        earth = AIEarth()
        engine = ExecutionEngine(llm=False)
        
        # Execute through engine
        result = engine.run("Multi-agent analysis", strategy="hybrid")
        assert result.success
        
        # Verify platform still works
        info = earth.platform_info()
        assert len(info["lego_pieces"]) >= 7


# ═════════════════════════════════════════════════════════
# Real LLM Execution (e2e) — marked llm, excluded from fast suite
# ═════════════════════════════════════════════════════════

@pytest.mark.llm
class TestRealLLMExecution:
    """Real intelligence flowing through each LEGO paradigm."""

    def test_langgraph_real_plan_and_execute(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm_budget_per_run=2, llm_max_tokens=200)
        result = engine.run("List two benefits of caching LLM responses", strategy="langgraph")
        assert result.success
        assert result.llm_calls >= 1
        assert result.metadata["intelligence"] == "llm"
        assert not result.output["result"].startswith("[structural]")
        assert any("[llm]" in s for s in result.output["steps"])

    def test_crewai_real_handoffs(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm_budget_per_run=3, llm_max_tokens=200)
        result = engine.run("Write a one-line tagline for an AI research platform", strategy="crewai")
        assert result.success
        assert result.llm_calls >= 1
        llm_handoffs = [h for h in result.output["handoffs"] if h["source"] == "llm"]
        assert len(llm_handoffs) >= 1
        # sequential handoff: writer received analyst output (chain is real)
        assert result.output["result"]

    def test_autogen_real_roundrobin(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm_budget_per_run=2, llm_max_tokens=200)
        result = engine.run("What is 17 + 25? Answer with the number.", strategy="autogen")
        assert result.success
        assert result.llm_calls >= 1
        assert result.output["turns"] >= 1
        assert "42" in str(result.output["conversation"])

    def test_dspy_real_signature_fill(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm_budget_per_run=1, llm_max_tokens=150)
        result = engine.run("Classify the sentiment of 'I love this platform': positive or negative?", strategy="dspy")
        assert result.success
        assert result.llm_calls == 1
        assert "positive" in result.output["result"].lower()

    def test_hybrid_budget_never_exceeded(self):
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine(llm_budget_per_run=3, llm_max_tokens=150)
        result = engine.run("Summarize what a key pool does in one sentence", strategy="hybrid")
        assert result.success
        # hybrid runs 3 pieces but budget guard caps total calls
        assert result.llm_calls <= 3
        assert result.llm_cost_usd < 0.01
