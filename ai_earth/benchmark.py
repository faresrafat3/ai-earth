"""
📊 AI Earth — Benchmark Suite
═══════════════════════════════════════════════════════════
Evaluates platform capabilities across all LEGO pieces.

Benchmarks:
    1. Import Speed — how fast each LEGO piece loads
    2. Execution Latency — time for each strategy
    3. Cross-Piece Composition — multi-piece workflows
    4. Evolution Quality — self-evolving core improvement rate
    5. Platform Health — overall system metrics

Usage:
    from ai_earth.benchmark import BenchmarkSuite

    suite = BenchmarkSuite()
    report = suite.run_all()
    print(suite.format_report(report))
"""

from __future__ import annotations

import time
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class BenchResult:
    """Single benchmark result."""
    name: str
    category: str
    passed: bool
    latency_ms: float = 0.0
    score: float = 0.0  # 0-1
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "passed": self.passed,
            "latency_ms": round(self.latency_ms, 2),
            "score": round(self.score, 4),
            "details": self.details,
            "error": self.error,
        }


@dataclass
class BenchReport:
    """Full benchmark report."""
    results: List[BenchResult] = field(default_factory=list)
    total_time_ms: float = 0.0
    timestamp: float = 0.0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def avg_score(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.score for r in self.results) / len(self.results)

    @property
    def avg_latency(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.latency_ms for r in self.results) / len(self.results)

    def by_category(self) -> Dict[str, List[BenchResult]]:
        cats: Dict[str, List[BenchResult]] = {}
        for r in self.results:
            cats.setdefault(r.category, []).append(r)
        return cats

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "avg_score": round(self.avg_score, 4),
            "avg_latency_ms": round(self.avg_latency, 2),
            "total_time_ms": round(self.total_time_ms, 2),
            "results": [r.to_dict() for r in self.results],
        }


class BenchmarkSuite:
    """
    📊 Benchmark Suite — evaluates platform capabilities.
    
    Runs 5 categories of benchmarks across all LEGO pieces
    and produces a comprehensive report.
    
    Example:
        suite = BenchmarkSuite()
        report = suite.run_all()
        print(f"Score: {report.avg_score:.2f}")
        print(f"Passed: {report.passed}/{report.total}")
    """

    def run_all(self) -> BenchReport:
        """Run all benchmarks."""
        start = time.time()
        results: List[BenchResult] = []
        
        # Category 1: Import Speed
        results.extend(self._bench_imports())
        
        # Category 2: Execution Latency
        results.extend(self._bench_execution())
        
        # Category 3: Cross-Piece
        results.extend(self._bench_cross_piece())
        
        # Category 4: Evolution Quality
        results.extend(self._bench_evolution())
        
        # Category 5: Platform Health
        results.extend(self._bench_health())
        
        total_time = (time.time() - start) * 1000
        
        return BenchReport(
            results=results,
            total_time_ms=total_time,
        )

    # ─── Category 1: Import Speed ──────────────────────

    def _bench_imports(self) -> List[BenchResult]:
        """Benchmark import speed for each LEGO piece."""
        results = []
        
        imports = [
            ("evoagentx", "from evoagentx.core.module import BaseModule"),
            ("dspy", "from dspy.primitives.example import Example"),
            ("mem0", "from mem0.configs.base import MemoryConfig"),
            ("langgraph", "from langgraph.graph.state import StateGraph"),
            ("crewai", "from crewai import Agent, Process"),
            ("autogen_core", "from autogen_core import AgentId"),
            ("autogen_chat", "from autogen_agentchat.agents import AssistantAgent"),
            ("model_router", "from ai_earth.model_router import ModelRouter"),
            ("orchestrator", "from ai_earth.orchestrator import AIEarth"),
            ("self_evolve", "from ai_earth.self_evolve import SelfEvolveCore"),
            ("executor", "from ai_earth.executor import ExecutionEngine"),
        ]
        
        for name, code in imports:
            start = time.time()
            try:
                exec(code)
                latency = (time.time() - start) * 1000
                # Score: faster = better, 100ms = 1.0, 1000ms = 0.5
                score = max(0.1, min(1.0, 100.0 / max(latency, 1)))
                results.append(BenchResult(
                    name=f"import_{name}",
                    category="import_speed",
                    passed=True,
                    latency_ms=latency,
                    score=score,
                    details={"import_time_ms": round(latency, 2)},
                ))
            except Exception as e:
                latency = (time.time() - start) * 1000
                results.append(BenchResult(
                    name=f"import_{name}",
                    category="import_speed",
                    passed=False,
                    latency_ms=latency,
                    score=0.0,
                    error=str(e)[:100],
                ))
        
        return results

    # ─── Category 2: Execution Latency ─────────────────

    def _bench_execution(self) -> List[BenchResult]:
        """Benchmark execution through each strategy."""
        from ai_earth.executor import ExecutionEngine
        engine = ExecutionEngine()
        results = []
        
        strategies = ["langgraph", "crewai", "autogen", "dspy", "hybrid"]
        
        for strategy in strategies:
            start = time.time()
            try:
                result = engine.run(f"Benchmark task for {strategy}", strategy=strategy)
                latency = (time.time() - start) * 1000
                score = 1.0 if result.success else 0.0
                results.append(BenchResult(
                    name=f"exec_{strategy}",
                    category="execution",
                    passed=result.success,
                    latency_ms=latency,
                    score=score,
                    details={"output_keys": list(result.output.keys())},
                ))
            except Exception as e:
                latency = (time.time() - start) * 1000
                results.append(BenchResult(
                    name=f"exec_{strategy}",
                    category="execution",
                    passed=False,
                    latency_ms=latency,
                    score=0.0,
                    error=str(e)[:100],
                ))
        
        return results

    # ─── Category 3: Cross-Piece Composition ───────────

    def _bench_cross_piece(self) -> List[BenchResult]:
        """Benchmark cross-piece composition scenarios."""
        results = []
        
        # Test 1: LangGraph + DSPy
        start = time.time()
        try:
            from langgraph.graph.state import StateGraph, START, END
            from dspy.primitives.example import Example
            from typing import TypedDict
            
            class S(TypedDict): task: str; result: str
            g = StateGraph(S)
            e = Example(task="test", result="ok")
            g.add_node("process", lambda s: {"result": "processed"})
            g.add_edge(START, "process")
            g.add_edge("process", END)
            c = g.compile()
            out = c.invoke({"task": "test", "result": ""})
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="langgraph_dspy",
                category="cross_piece",
                passed=True,
                latency_ms=latency,
                score=1.0,
                details={"graph_output": out.get("result", "")},
            ))
        except Exception as e:
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="langgraph_dspy", category="cross_piece",
                passed=False, latency_ms=latency, error=str(e)[:100],
            ))
        
        # Test 2: CrewAI + AutoGen
        start = time.time()
        try:
            from crewai import Process
            from autogen_core.models import UserMessage
            msg = UserMessage(content="test", source="user")
            assert Process.sequential.value == "sequential"
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="crewai_autogen",
                category="cross_piece",
                passed=True, latency_ms=latency, score=1.0,
            ))
        except Exception as e:
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="crewai_autogen", category="cross_piece",
                passed=False, latency_ms=latency, error=str(e)[:100],
            ))
        
        # Test 3: Mem0 + DSPy + LangGraph
        start = time.time()
        try:
            from mem0.configs.base import MemoryConfig
            from dspy.primitives.example import Example
            from langgraph.constants import START, END
            mc = MemoryConfig()
            e = Example(memory="stored")
            assert START is not None
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="mem0_dspy_langgraph",
                category="cross_piece",
                passed=True, latency_ms=latency, score=1.0,
            ))
        except Exception as e:
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="mem0_dspy_langgraph", category="cross_piece",
                passed=False, latency_ms=latency, error=str(e)[:100],
            ))
        
        # Test 4: Full composition via orchestrator
        start = time.time()
        try:
            from ai_earth.orchestrator import AIEarth
            earth = AIEarth()
            earth.create_langgraph("bench_graph")
            earth.create_crew("bench_crew", [
                {"name": "agent1", "role": "Worker", "goal": "Work"},
            ])
            earth.create_memory("bench_mem")
            composed = earth.compose("bench_pipeline",
                graph_name="bench_graph",
                crew_agents=["agent1"],
                memory_store="bench_mem",
            )
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="full_orchestrator",
                category="cross_piece",
                passed=True, latency_ms=latency, score=1.0,
                details={"pieces": list(composed["pieces"].keys())},
            ))
        except Exception as e:
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="full_orchestrator", category="cross_piece",
                passed=False, latency_ms=latency, error=str(e)[:100],
            ))
        
        return results

    # ─── Category 4: Evolution Quality ─────────────────

    def _bench_evolution(self) -> List[BenchResult]:
        """Benchmark self-evolution quality."""
        results = []
        
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        
        # Test improvement over iterations
        start = time.time()
        try:
            result = core.evolve(
                "Analyze and optimize a multi-agent workflow",
                max_iterations=5,
            )
            latency = (time.time() - start) * 1000
            
            scores = [h["metrics"]["overall_score"] for h in result.history]
            improvement = scores[-1] - scores[0] if scores else 0
            
            results.append(BenchResult(
                name="evolution_improvement",
                category="evolution",
                passed=result.success,
                latency_ms=latency,
                score=min(1.0, max(0.0, improvement * 5)),  # Scale improvement
                details={
                    "iterations": result.iterations,
                    "start_score": round(scores[0], 4) if scores else 0,
                    "end_score": round(scores[-1], 4) if scores else 0,
                    "improvement": round(improvement, 4),
                    "learnings": core.num_learnings(),
                },
            ))
        except Exception as e:
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="evolution_improvement", category="evolution",
                passed=False, latency_ms=latency, error=str(e)[:100],
            ))
        
        # Test strategy learning
        start = time.time()
        try:
            strategies = core.learned_strategies()
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="strategy_learning",
                category="evolution",
                passed=len(strategies) > 0,
                latency_ms=latency,
                score=min(1.0, len(strategies) / 3.0),
                details={"strategies": strategies},
            ))
        except Exception as e:
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="strategy_learning", category="evolution",
                passed=False, latency_ms=latency, error=str(e)[:100],
            ))
        
        return results

    # ─── Category 5: Platform Health ───────────────────

    def _bench_health(self) -> List[BenchResult]:
        """Benchmark overall platform health."""
        results = []
        
        # Platform info completeness
        start = time.time()
        try:
            from ai_earth.orchestrator import AIEarth
            earth = AIEarth()
            info = earth.platform_info()
            latency = (time.time() - start) * 1000
            
            has_pieces = len(info.get("lego_pieces", {})) >= 7
            has_totals = "totals" in info
            has_tests = info.get("totals", {}).get("tests", 0) >= 500
            
            results.append(BenchResult(
                name="platform_info",
                category="health",
                passed=has_pieces and has_totals,
                latency_ms=latency,
                score=1.0 if has_pieces and has_tests else 0.5,
                details={
                    "pieces": len(info.get("lego_pieces", {})),
                    "tests": info.get("totals", {}).get("tests", 0),
                },
            ))
        except Exception as e:
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="platform_info", category="health",
                passed=False, latency_ms=latency, error=str(e)[:100],
            ))
        
        # Model Router health
        start = time.time()
        try:
            from ai_earth.model_router import ModelRouter
            router = ModelRouter()
            router.configure()  # Real LLM via Key Pool
            response = router.chat(prompt="health check", model="gpt-4o-mini")
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="model_router",
                category="health",
                passed=response.content is not None,
                latency_ms=latency,
                score=1.0,
                details={"model": response.model, "cached": response.cached},
            ))
        except Exception as e:
            latency = (time.time() - start) * 1000
            results.append(BenchResult(
                name="model_router", category="health",
                passed=False, latency_ms=latency, error=str(e)[:100],
            ))
        
        return results

    # ─── Report Formatting ─────────────────────────────

    @staticmethod
    def format_report(report: BenchReport) -> str:
        """Format benchmark report as readable string."""
        lines = [
            "📊 AI Earth — Benchmark Report",
            "════════════════════════════════════",
            "",
            f"Total:  {report.total} benchmarks",
            f"Passed: {report.passed} ✅",
            f"Failed: {report.failed} ❌",
            f"Score:  {report.avg_score:.2f}/1.00",
            f"Time:   {report.total_time_ms:.0f}ms",
            "",
        ]
        
        for cat, results in report.by_category().items():
            cat_score = sum(r.score for r in results) / len(results) if results else 0
            cat_passed = sum(1 for r in results if r.passed)
            lines.append(f"  {cat.upper()} ({cat_score:.2f}): {cat_passed}/{len(results)} passed")
            for r in results:
                icon = "✅" if r.passed else "❌"
                lines.append(f"    {icon} {r.name}: {r.latency_ms:.1f}ms, score={r.score:.2f}")
        
        lines.extend(["", f"Overall: {report.avg_score:.2f}/1.00 ({report.passed}/{report.total})"])
        return "\n".join(lines)
