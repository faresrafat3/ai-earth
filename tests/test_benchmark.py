"""
Tests for Benchmark Suite — AI Earth Platform
===============================================
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth'))


class TestBenchResult:
    """Test BenchResult data model."""

    def test_passing_result(self):
        from ai_earth.benchmark import BenchResult
        r = BenchResult(name="test", category="cat", passed=True, score=0.9)
        d = r.to_dict()
        assert d["passed"]
        assert d["score"] == 0.9

    def test_failing_result(self):
        from ai_earth.benchmark import BenchResult
        r = BenchResult(name="test", category="cat", passed=False, error="fail")
        d = r.to_dict()
        assert not d["passed"]
        assert d["error"] == "fail"


class TestBenchReport:
    """Test BenchReport data model."""

    def test_empty_report(self):
        from ai_earth.benchmark import BenchReport
        report = BenchReport()
        assert report.total == 0
        assert report.passed == 0
        assert report.failed == 0
        assert report.avg_score == 0.0

    def test_report_with_results(self):
        from ai_earth.benchmark import BenchReport, BenchResult
        report = BenchReport(results=[
            BenchResult(name="a", category="cat1", passed=True, score=0.8),
            BenchResult(name="b", category="cat1", passed=True, score=0.6),
            BenchResult(name="c", category="cat2", passed=False, score=0.0),
        ])
        assert report.total == 3
        assert report.passed == 2
        assert report.failed == 1
        assert abs(report.avg_score - (0.8 + 0.6 + 0.0) / 3) < 0.01

    def test_by_category(self):
        from ai_earth.benchmark import BenchReport, BenchResult
        report = BenchReport(results=[
            BenchResult(name="a", category="speed", passed=True, score=1.0),
            BenchResult(name="b", category="speed", passed=True, score=0.9),
            BenchResult(name="c", category="quality", passed=True, score=0.7),
        ])
        cats = report.by_category()
        assert len(cats["speed"]) == 2
        assert len(cats["quality"]) == 1

    def test_to_dict(self):
        from ai_earth.benchmark import BenchReport, BenchResult
        report = BenchReport(results=[
            BenchResult(name="test", category="cat", passed=True, score=1.0),
        ])
        d = report.to_dict()
        assert d["total"] == 1
        assert d["passed"] == 1
        assert len(d["results"]) == 1


class TestBenchmarkSuite:
    """Test the benchmark suite execution."""

    def test_run_all(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        report = suite.run_all()
        assert report.total > 0
        assert report.passed >= report.total * 0.8  # At least 80% pass

    def test_import_benchmarks(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        results = suite._bench_imports()
        assert len(results) >= 10  # 11 import tests
        # Core imports should always pass
        passed_names = [r.name for r in results if r.passed]
        assert "import_model_router" in passed_names

    def test_execution_benchmarks(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        results = suite._bench_execution()
        assert len(results) == 5  # 5 strategies
        # All should pass with real LLM
        assert all(r.passed for r in results)

    def test_cross_piece_benchmarks(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        results = suite._bench_cross_piece()
        assert len(results) >= 3  # At least 3 cross-piece tests

    def test_evolution_benchmarks(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        results = suite._bench_evolution()
        assert len(results) == 2
        # Evolution should improve
        evo_result = [r for r in results if r.name == "evolution_improvement"][0]
        assert evo_result.passed
        assert evo_result.details["improvement"] > 0

    def test_health_benchmarks(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        results = suite._bench_health()
        assert len(results) == 2
        assert all(r.passed for r in results)

    def test_format_report(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        report = suite.run_all()
        text = suite.format_report(report)
        assert "Benchmark Report" in text
        assert "Overall:" in text


class TestBenchmarkCategories:
    """Test each benchmark category has proper structure."""

    def test_all_results_have_required_fields(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        report = suite.run_all()
        
        for r in report.results:
            d = r.to_dict()
            assert "name" in d
            assert "category" in d
            assert "passed" in d
            assert "latency_ms" in d
            assert "score" in d
            assert 0 <= d["score"] <= 1.0

    def test_all_categories_present(self):
        from ai_earth.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        report = suite.run_all()
        cats = set(r.category for r in report.results)
        assert "import_speed" in cats
        assert "execution" in cats
        assert "cross_piece" in cats
        assert "evolution" in cats
        assert "health" in cats
