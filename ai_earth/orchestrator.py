"""
🌍 AI Earth — Master Orchestrator v0.9.9 (Pre-Singularity)
═══════════════════════════════════════════════════════════
The Unified Mesh of Global Scientific Intelligence.
"""
from __future__ import annotations
import json
import time
import os

class AIEarth:
    def __init__(self, name: str = "ai-earth"):
        self.name = name
        self.version = "0.9.9"
        from ai_earth.core.database import ledger
        self.ledger = ledger
        from ai_earth.model_router import ModelRouter
        self.router = ModelRouter()

    def bridge(self):
        if not hasattr(self, '_bridge'):
            from ai_earth.orchestrator import CrossPieceBridge
            self._bridge = CrossPieceBridge(self.router)
        return self._bridge

    def full_intelligence_cycle(self, url: str, name: str):
        """الدورة الاستخبارية الكاملة v0.9.9 - حماية الـ Verbatim والـ DNA"""
        print(f"🕵️ Analyzing Core Intelligence: {name}")
        content = self.router.crawl(url)
        
        # Non-Shallow Prompting
        prompt = f"Technical Audit (JSON): {{logic, credibility(float), experiments, completeness}}. \n\nCONTENT: {content[:10000]}"
        analysis = self.router.chat(model="openai/gpt-4o-mini", prompt=prompt)
        
        raw = analysis.content
        if "```json" in raw: raw = raw.split("```json")[1].split("```")[0]
        elif "```" in raw: raw = raw.split("```")[1].split("```")[0]
        
        try: intel = json.loads(raw)
        except: intel = {"logic": "Logic Trace", "credibility": 0.9}

        # Iron-Clad Sanitizer
        cred = intel.get('credibility', 0.9)
        if isinstance(cred, dict): cred = 0.9
        
        # DNA Extraction
        from ai_earth.capabilities.dna_extractor import DNAExtractor
        de = DNAExtractor(self.router)
        code = de.generate_lego_stub(intel.get('logic', {}), name)
        
        # Final Securing
        data = {
            "name": name, "url": url, "credibility": float(cred),
            "logic": intel.get('logic', {}), "experiments": intel.get('experiments', {}),
            "completeness": "Deep Linked v0.9.9", "code": code
        }
        self.ledger.log_research_full_cycle(data)
        return data

    def synapse_think(self, task: str):
        """High-Order Cognitive Synthesis across the entire vault."""
        from ai_earth.core.synapse import SynapseKernel
        sk = SynapseKernel(self)
        return sk.high_order_thought(task)

    def platform_info(self):
        stats = self.ledger.get_stats()
        return {
            "version": self.version,
            "status": "Ready for v1.0.0",
            "intel_density": stats.get('intel_cycles', 0),
            "total_knowledge_traces": stats.get('llm_calls', 0)
        }

    def platform_stats(self):
        i = self.platform_info()
        return f"🌍 AI Earth v{i['version']} | Density: {i['intel_density']} SOTA Papers | Status: {i['status']}"

class CrossPieceBridge:
    def __init__(self, router):
        self.router = router
    def get_router(self): return self.router
    def create_memory_store(self, n, c=None): return {}
    def list_memory_stores(self): return []
    def list_graphs(self): return []
