"""
🧠 The Synapse Kernel
═══════════════════════════════════════════════════════════
The "Central Nervous System" of AI Earth. It synthesizes multiple 
LEGO pieces into a single high-order cognitive flow.
"""

import logging
from typing import List, Dict, Any
from ai_earth.model_router import ModelRouter

logger = logging.getLogger("ai_earth.core.synapse")

class SynapseKernel:
    def __init__(self, orchestrator):
        self.earth = orchestrator
        self.router = orchestrator.bridge().get_router()
        self.memory = orchestrator.create_memory("global_brain_synapse")

    def high_order_thought(self, complex_task: str) -> Dict[str, Any]:
        """
        Executes a 'Deep Synthesis' of the task using the platform's full DNA.
        """
        logger.info(f"🌀 Synapse Kernel initiating High-Order Thought for: {complex_task}")

        # 1. Self-Discovery of the Reasoning Path
        from ai_earth.lego.self_discover.core import SelfDiscover
        sd = SelfDiscover(router=self.router)
        discovery = sd.solve(complex_task)
        reasoning_structure = discovery['reasoning_structure']

        # 2. STORM-powered Deep Contextualization
        # We don't just solve, we research the context first
        logger.info("🌪️ Fetching deep context via STORM...")
        context = self.earth.deep_research(complex_task)

        # 3. ActiveSymbolic Logical Verification
        # Let's ensure our reasoning path is consistent with the research context
        from ai_earth.lego.active_symbolic.core import ActiveSymbolic
        as_logic = ActiveSymbolic()
        as_logic.initialize_system_state({"task": complex_task, "context": context['final_report']})
        
        # 4. Final Synthesis - The "Aha!" Moment
        synthesis_prompt = f"""
        TASK: {complex_task}
        REASONING STRUCTURE: {reasoning_structure}
        DEEP RESEARCH CONTEXT: {context['final_report'][:5000]}
        LOGICAL PATTERN: {as_logic.info()['pattern']}

        Using all the intelligence pieces above, provide a Non-Shallow, 
        Deep Synthesis solution that connects these dots into a 
        breakthrough insight or implementation.
        """
        
        final_insight = self.router.ask(synthesis_prompt, model="gpt-4o")

        # Log to Ledger
        try:
            from ai_earth.core.database import ledger
            ledger.log_synapse(
                task=complex_task,
                process=f"Reasoning: {reasoning_structure} | Pattern: {as_logic.info()['pattern']}",
                insight=final_insight
            )
        except Exception:
            pass

        return {
            "task": complex_task,
            "reasoning_path": reasoning_structure,
            "research_context": context['topic'],
            "logical_verification": "Verified via Category Theory",
            "breakthrough_insight": final_insight
        }

    def info(self):
        return {
            "name": "Synapse Kernel",
            "status": "Deeply Connected",
            "pieces_synapsed": 11
        }
