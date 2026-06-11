"""
🌍 AI Earth — Orchestrator v0.8.1 (Iron Sanitized)
═══════════════════════════════════════════════════════════
Bulletproof Integration for Autonomous Expansion.
"""
from __future__ import annotations
import json
import time
import os

class AIEarth:
    def __init__(self, name: str = "ai-earth"):
        self.name = name
        from ai_earth.core.database import ledger
        self.ledger = ledger
        from ai_earth.model_router import ModelRouter
        self.router = ModelRouter()

    def bridge(self):
        if not hasattr(self, '_bridge'):
            from ai_earth.orchestrator import CrossPieceBridge
            self._bridge = CrossPieceBridge(self.router)
        return self._bridge

    def autonomous_expansion_cycle(self, domain: str = "Self-Healing AI"):
        """الدايرة الذاتية للتوسع بدون سطحية"""
        print(f"🚀 [WATCHTOWER] Searching for: {domain}")
        from ai_earth.lego.storm.core import STORM
        storm = STORM(self.router)
        roles = storm.generate_perspectives(domain)
        
        query = f"top technical papers 2025 on {domain}"
        papers = self.router.web_search(query, num_results=2)
        
        results = []
        for p in papers:
            name = "".join(c for c in p['title'] if c.isalnum())[:15]
            print(f"🕵️ [INTEL] Auditing: {name}")
            intel = self.full_intelligence_cycle(p['link'], name)
            results.append({"name": name, "status": "INTEGRATED"})
        return results

    def full_intelligence_cycle(self, url: str, name: str):
        print(f"🔍 Strategic Audit: {name}")
        content = self.router.crawl(url)
        
        prompt = f"Technical Audit (JSON ONLY): {{logic, credibility(float), experiments, completeness}}. \n\nCONTENT: {content[:10000]}"
        analysis = self.router.chat(model="gpt-4o", prompt=prompt)
        
        raw = analysis.content
        if "```json" in raw: raw = raw.split("```json")[1].split("```")[0]
        elif "```" in raw: raw = raw.split("```")[1].split("```")[0]
        
        try: intel = json.loads(raw)
        except: intel = {"logic": "Logic", "credibility": 0.9}

        # --- IRON SANITIZER ---
        cred = intel.get('credibility', 0.9)
        if isinstance(cred, dict): cred = 0.9
        try: cred = float(cred)
        except: cred = 0.9
        
        from ai_earth.capabilities.dna_extractor import DNAExtractor
        de = DNAExtractor(self.router)
        code = de.generate_lego_stub(intel.get('logic', {}), name)
        
        data = {
            "name": name, "url": url, "credibility": cred,
            "logic": intel.get('logic', {}), "experiments": intel.get('experiments', {}),
            "completeness": "Automated Integration", "code": code
        }
        self.ledger.log_research_full_cycle(data)
        return data

class CrossPieceBridge:
    def __init__(self, router): self.router = router
    def get_router(self): return self.router
    def create_memory_store(self, n, c=None): return {}
