"""
🧬 Memory Re-Infection Engine (v1.3.6)
═══════════════════════════════════════════════════════════
"""

import sqlite3
import json
import logging
from typing import Dict, Any, List

class MemoryRefiner:
    def __init__(self, db_path="/home/user/ai-earth/data/earth_ledger.db"):
        self.db_path = db_path

    def distill_best_practices(self) -> Dict[str, Any]:
        """يستخدم العمود الصحيح: breakthrough_insight"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT task, breakthrough_insight FROM synapse_thoughts ORDER BY id DESC LIMIT 10")
                records = cursor.fetchall()
        except: records = []
            
        if not records:
            return {"status": "Awaiting Thoughts", "rules": []}

        distilled_rules = [f"Task: {t[:30]} | Success Path: {i[:50]}" for t, i in records]
            
        return {
            "status": "Infected",
            "active_protocols": distilled_rules
        }

    def get_efficiency_report(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT model, AVG(latency_ms), COUNT(*) FROM llm_interactions GROUP BY model")
                stats = cursor.fetchall()
        except: stats = []
        return {model: {"avg_latency": avg, "calls": count} for model, avg, count in stats}
