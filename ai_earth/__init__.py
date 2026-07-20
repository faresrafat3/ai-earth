"""
🌍 AI Earth — The Intelligence Aggregation Platform
═══════════════════════════════════════════════════════

A self-evolving intelligence platform that aggregates ALL AI research
and composes them into a unified, living system via LEGO pieces.

AI Earth is NOT just an agent platform — it is a comprehensive
aggregation layer for the entire AI research landscape:
    - Research papers extracted verbatim as LEGO pieces
    - Self-evolving intelligence with a 7-phase evolution loop
    - Real LLM integration via Key Pool (OpenRouter, GitHub, Google)
    - Web search, memory, optimization, multi-agent orchestration
    - Every piece composable through the CrossPieceBridge

Architecture:
    🧬 Self-Evolving Core (7-phase loop + 6 strategies)
    🔗 CrossPieceBridge (composes all LEGO pieces)
    🔑 Key Pool (21 API keys with smart rotation)
    🌐 Platform API (FastAPI REST — 19 endpoints)
    🎨 Streamlit UI (4 interactive pages)
    🔍 Web Search (Serper integration)

    🧱 7 LEGO Pieces (836 files, 197K+ lines from 7 papers):
        1. EvoAgentX (192 files) — EMNLP 2025 — Workflow Engine + 6 Optimizers
        2. DSPy (148 files) — ICLR 2024, 28K⭐ — Signatures + 8 Predictors + 15 Teleprompters
        3. Mem0 (144 files) — 25K⭐ — Memory + 13 Embeddings + 25 Vector Stores
        4. Model Router (2 files) — Real LLM via Key Pool (21 keys, 3 providers)
        5. LangGraph (86 files) — 25K⭐ — Graph Engine + Channels + Pregel
        6. CrewAI (153 files) — 22K⭐ — Multi-Agent Crews + Flow + Knowledge
        7. AutoGen (111 files) — Microsoft, 42K⭐ — Event-Driven Multi-Agent

Usage:
    # Platform API
    from ai_earth.api import app

    # Real LLM calls (no mock — ever)
    from ai_earth.model_router import ModelRouter
    router = ModelRouter()
    response = router.chat(prompt="Hello", model="gpt-4o-mini")
    print(response.content)  # Real AI response

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

    # Web search
    from ai_earth.llm_pool import web_search
    results = web_search("AI research 2025")

Stats: 836+ files, 197K+ lines, 592 tests, 7 papers, 21 API keys
"""

__version__ = "2.7.0"
__author__ = "Fares Rafat"
__status__ = "Autonomous Engineering — v2.3.0 (80 SOTA Papers)"
