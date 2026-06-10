"""
🌍 AI Earth — The Living Intelligence Ecosystem

A self-improving, self-evolving intelligence system built from
LEGO pieces extracted from research papers.

Architecture: 7 Layers
    L1: Core (BaseModule, Registry, Config)
    L2: Models + Prompts (BaseLLM, PromptTemplate)
    L3: Agents + Actions (Agent, Action)
    L4: Workflow (WorkFlowGraph, SequentialWorkFlowGraph, Operators)
    L5: Memory + RAG (ShortTerm, LongTerm, MemoryManager, RAG Pipeline)
    L6: Evaluation (Evaluator, 10 Benchmarks)
    L7: Optimizers (SEW, AFlow, TextGrad, MIPRO, EvoPrompt, MapElites)

LEGO Source: EvoAgentX (arXiv:2507.03616, EMNLP 2025)

Usage:
    from ai_earth.orchestrator import AIEarth
    
    earth = AIEarth()
    
    workflow = (
        earth.builder()
        .goal("Your workflow goal")
        .task("step1", inputs={"x": "desc"}, outputs={"y": "desc"})
        .task("step2", inputs={"y": "desc"}, outputs={"z": "desc"})
        .sequential()
        .build()
    )
    
    graph = earth.create_workflow_from_spec(workflow)
    earth.save_workflow("my-workflow", graph)
"""

__version__ = "0.1.0"
__author__ = "Fares Rafat"
__status__ = "Phase 1 — LEGO Pieces Assembled + Orchestrator Operational"
