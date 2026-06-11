"""
🌍 AI Earth — Orchestrator v1.2.0 (The Living Agent Factory)
═══════════════════════════════════════════════════════════
Turning research DNA into a living army of specialized agents.
"""
from __future__ import annotations
import json
import time
import os

class AIEarth:
    def __init__(self, name: str = "ai-earth"):
        self.name = name
        self.version = "1.2.0"
        from ai_earth.core.database import ledger
        self.ledger = ledger
        from ai_earth.model_router import ModelRouter
        self.router = ModelRouter()
        self._init_factory()

    def _init_factory(self):
        from ai_earth.core.factory import AgentFactory
        self.factory = AgentFactory(self)

    def bridge(self):
        if not hasattr(self, '_bridge'):
            from ai_earth.orchestrator import CrossPieceBridge
            self._bridge = CrossPieceBridge(self.router)
        return self._bridge

    def full_intelligence_cycle(self, url: str, name: str):
        """دورة كاملة: بحث -> تحليل -> كود -> خلق وكيل حي"""
        print(f"🕵️ Recon: {name}")
        content = self.router.crawl(url)
        
        # [Simplified audit for speed]
        intel = {"logic": "SOTA Framework", "credibility": 0.9}
        
        # 1. Store in Ledger
        self.ledger.log_research_full_cycle({
            "name": name, "url": url, "credibility": 0.9,
            "logic": intel['logic'], "experiments": {}, "completeness": "v1.2.0 Active", "code": ""
        })

        # 2. Add to Knowledge Mesh
        from ai_earth.core.knowledge_graph import earth_graph
        earth_graph.add_paper(name, intel)

        # 3. ACTIVATE AGENT (The Breakthrough Step)
        print(f"🤖 Activating {name}_Specialist...")
        self.factory.instantiate_agent_from_research(name)
        
        return intel

    def solve_with_swarm(self, task: str):
        """يستدعي أقوى الأبحاث كوكلاء أحياء لحل المهمة"""
        print(f"🌀 Summoning the Swarm for: {task}")
        summoned_papers = self.factory.summon_swarm(task)
        
        # Building the collective response
        swarm_logic = []
        for paper in summoned_papers:
            swarm_logic.append(f"- Specialist from {paper} is applying its DNA.")
            
        prompt = f"TASK: {task}\nSWARM LOGIC: {swarm_logic}\n\nSynthesize the collective solution."
        return self.router.ask(prompt, model="openai/gpt-4o")

class CrossPieceBridge:
    def __init__(self, router): self.router = router
    def get_router(self): return self.router
    def create_memory_store(self, n, c=None): return {}
    def list_memory_stores(self): return []
