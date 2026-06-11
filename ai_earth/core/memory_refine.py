"""
🧬 Memory Re-Infection Engine (v1.3.0)
═══════════════════════════════════════════════════════════
Analyzes historical thoughts in the Ledger to optimize future 
cognition paths. Moving from logging to active learning.
"""

import sqlite3
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("ai_earth.core.memory_refine")

class MemoryRefiner:
    def __init__(self, db_path="/home/user/ai-earth/data/earth_ledger.db"):
        self.db_path = db_path

    def distill_best_practices(self) -> Dict[str, Any]:
        """
        يحلل أنجح عمليات التفكير (التي حصلت على أعلى سكور) ويستخلص منها 'البصمة'.
        """
        logger.info("🧪 Distilling best practices from historical thoughts...")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # جلب أفضل العمليات اللي سجلناها
            cursor.execute("SELECT task, insight FROM synapse_thoughts ORDER BY id DESC LIMIT 10")
            records = cursor.fetchall()
            
        if not records:
            return {"status": "Empty Ledger", "rules": []}

        # عملية 'الحقن' (Re-Infection): تحويل الداتا لـ 'بروتوكولات'
        distilled_rules = []
        for task, insight in records:
            distilled_rules.append(f"For task '{task[:50]}...', successful path involved: {insight[:100]}")
            
        return {
            "status": "Infected",
            "protocol_count": len(distilled_rules),
            "active_protocols": distilled_rules
        }

    def get_efficiency_report(self):
        """يحسب كفاءة الموديلات والمفاتيح بناءً على الـ Latency التاريخي"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT model, AVG(latency_ms), COUNT(*) FROM llm_interactions GROUP BY model")
            stats = cursor.fetchall()
        
        return {model: {"avg_latency": avg, "calls": count} for model, avg, count in stats}
