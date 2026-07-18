"""
Tests for Streamlit Web UI — AI Earth Platform
===============================================
Tests that the UI module loads and all components initialize.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth'))


class TestUIModule:
    """Test UI module imports and components."""

    def test_ui_file_exists(self):
        assert os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'ui.py'))

    def test_ui_imports(self):
        """Test all required imports for UI are available."""
        # These are all the imports the UI needs
        from ai_earth.orchestrator import AIEarth
        from ai_earth.self_evolve import SelfEvolveCore
        from ai_earth.model_router import ModelRouter
        assert AIEarth is not None
        assert SelfEvolveCore is not None
        assert ModelRouter is not None

    def test_ui_platform_info(self):
        """Test platform info is available for dashboard."""
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        info = earth.platform_info()
        assert "lego_pieces" in info
        assert "totals" in info
        assert len(info["lego_pieces"]) == 9

    def test_ui_evolution_core(self):
        """Test evolution core is available for evolve page."""
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore()
        result = core.evolve("Test task for UI", max_iterations=1)
        assert result.iterations == 1
        assert result.to_dict() is not None

    @pytest.mark.llm
    def test_ui_model_router(self):
        """Test model router is available for chat page (real LLM call)."""
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        router.configure()  # Real LLM
        response = router.chat(prompt="Hello", model="gpt-4o-mini")
        assert response.content is not None
        assert "gpt-4o-mini" in response.model

    def test_ui_models_list(self):
        """Test model listing for UI selector."""
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        models = router.list_models()
        assert len(models) > 0
        model_names = [m["name"] for m in models]
        assert "gpt-4o" in model_names

    def test_ui_providers_list(self):
        """Test provider listing for UI."""
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        providers = router.list_providers()
        assert "openai" in providers

    def test_ui_lego_pieces_source_files(self):
        """Test source files are accessible for file browser."""
        base = os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego')
        
        dir_map = {
            "evoagentx": "evoagentx",
            "dspy": "dspy",
            "mem0": "mem0",
            "langgraph": "langgraph_src",
            "crewai": "crewai_src",
            "autogen": "autogen_src",
        }
        
        for name, dirname in dir_map.items():
            path = os.path.join(base, dirname)
            assert os.path.exists(path), f"Missing LEGO dir: {name} -> {dirname}"
            # Should have at least some .py files
            py_files = []
            for root, dirs, files in os.walk(path):
                py_files.extend(f for f in files if f.endswith(".py"))
            assert len(py_files) > 0, f"No Python files in {name}"

    def test_ui_platform_stats(self):
        """Test platform stats string generation."""
        from ai_earth.orchestrator import AIEarth
        earth = AIEarth()
        stats = earth.platform_stats()
        assert "ai-earth" in stats
        assert "543 tests" in stats
        assert "9" in stats  # 9 LEGO pieces/papers


class TestUIEvolutionIntegration:
    """Test the evolution loop works as the UI would use it."""

    def test_evolution_with_callback(self):
        """Test evolution with callback (like UI progress tracking)."""
        from ai_earth.self_evolve import SelfEvolveCore, EvolutionPhase
        
        core = SelfEvolveCore()
        phases_seen = []
        
        def callback(phase, cycle):
            phases_seen.append(phase.value)
        
        result = core.evolve(
            "Analyze and summarize research papers",
            max_iterations=2,
            strategy="hybrid",
            callback=callback,
        )
        
        assert result.iterations == 2
        assert "observe" in phases_seen
        assert "plan" in phases_seen
        assert "execute" in phases_seen

    def test_evolution_score_progression(self):
        """Test scores improve over iterations."""
        from ai_earth.self_evolve import SelfEvolveCore
        
        core = SelfEvolveCore()
        result = core.evolve("Complex analysis task", max_iterations=3)
        
        scores = [h["metrics"]["overall_score"] for h in result.history]
        assert len(scores) == 3
        assert scores[-1] >= scores[0]

    def test_evolution_strategies_for_ui(self):
        """Test all strategies available in UI selector."""
        from ai_earth.self_evolve import SelfEvolveCore, Strategy
        
        for strat in ["hybrid", "prompt_optimize", "workflow_evolve",
                       "agent_refine", "memory_augment", "graph_restructure"]:
            core = SelfEvolveCore()
            result = core.evolve("Test task", max_iterations=1, strategy=strat)
            assert result.iterations >= 1
