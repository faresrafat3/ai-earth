"""
🌍 AI Earth — The Living Intelligence Ecosystem

Self-evolving AI agent platform built from LEGO pieces extracted
from 6 major open-source research frameworks (100K+ ⭐ combined).

Architecture:
    🧬 Self-Evolving Core (7-phase loop + 6 strategies)
    🔗 CrossPieceBridge (composes all LEGO pieces)
    🌐 Platform API (FastAPI REST)
    🧱 6 LEGO Pieces:
        - EvoAgentX (192 files) — Workflow Engine + 6 Optimizers
        - DSPy (148 files) — Signatures + 8 Predictors + 15 Teleprompters
        - Mem0 (144 files) — Memory + 13 Embeddings + 25 Vector Stores
        - Model Router (2 files) — Unified LLM Interface (7 providers)
        - LangGraph (86 files) — Graph Engine + Channels + Pregel
        - CrewAI (153 files) — Multi-Agent Crews + Flow + Knowledge

Usage:
    # Platform API
    from ai_earth.api import app

    # Self-evolving core
    from ai_earth.self_evolve import SelfEvolveCore
    core = SelfEvolveCore()
    result = core.evolve("Your task here", max_iterations=3)

    # Orchestrator
    from ai_earth.orchestrator import AIEarth
    earth = AIEarth()
    earth.create_langgraph("graph")
    earth.create_crew("team", [...])
    earth.compose("pipeline", ...)

    # Model Router
    from ai_earth.model_router import ModelRouter
    router = ModelRouter()
    response = router.chat(prompt="Hello", model="gpt-4o-mini")

Stats: 725 files, 177,630 lines, 487 tests, 6 papers
"""

__version__ = "0.2.0"
__author__ = "Fares Rafat"
__status__ = "Self-Evolving Platform with API — 487 tests passing"
