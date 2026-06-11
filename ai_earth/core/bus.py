"""
🚌 The Intelligence Bus (v0.9.5)
═══════════════════════════════════════════════════════════
A shared context layer that enables LEGO pieces to interact 
deeply without modifying their original verbatim code.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger("ai_earth.core.bus")

class IntelligenceBus:
    def __init__(self):
        self.shared_context = {}
        self.event_log = []

    def publish(self, piece_name: str, data: Any, tag: str = "general"):
        """تنشره أي قطعة LEGO عن نتائجها ليكون متاحاً للآخرين"""
        entry = {
            "source": piece_name,
            "data": data,
            "tag": tag,
            "timestamp": None # Will be set by Ledger
        }
        self.shared_context[tag] = data
        self.event_log.append(entry)
        logger.info(f"📢 Bus: {piece_name} published to tag '{tag}'")

    def subscribe(self, tag: str) -> Any:
        """تستدعيه أي قطعة LEGO لتعرف ماذا فعلت القطع الأخرى"""
        return self.shared_context.get(tag)

    def get_full_history(self):
        return self.event_log

# Global Bus Instance
intel_bus = IntelligenceBus()
