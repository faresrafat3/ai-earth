"""
🏗️ The Living Agent Factory (v1.2.0)
═══════════════════════════════════════════════════════════
Turns research DNA into active, specialized agents.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger("ai_earth.core.factory")

class AgentFactory:
    def __init__(self, orchestrator):
        self.earth = orchestrator
        self.router = orchestrator.bridge().get_router()
        self.active_agents = {}

    def instantiate_agent_from_research(self, paper_name: str) -> Dict[str, Any]:
        """يخلق وكيل متخصص بناءً على اسم البحث"""
        logger.info(f"🔨 Instantiating Specialist: {paper_name}")
        
        agent_spec = {
            "name": f"{paper_name}_Specialist",
            "role": f"Expert Analyst in {paper_name}",
            "backstory": f"Autonomous intelligence built from {paper_name}.",
            "status": "Active"
        }
        
        self.active_agents[paper_name] = agent_spec
        return agent_spec

    def summon_swarm(self, task: str) -> List[str]:
        # Using a simpler logic to avoid API 402 during test if needed
        return list(self.active_agents.keys())[:3]
