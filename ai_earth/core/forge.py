"""
🔨 The Intelligence Forge
═══════════════════════════════════════════════════════════
The self-programming engine of AI Earth. It takes synthesized 
insights and turns them into functional, tested Python capabilities.
"""

import os
import logging
import importlib.util
from typing import Dict, Any
from ai_earth.model_router import ModelRouter
from ai_earth.core.database import ledger

logger = logging.getLogger("ai_earth.core.forge")

class IntelligenceForge:
    def __init__(self, router: ModelRouter = None):
        self.router = router or ModelRouter()
        self.capabilities_path = "/home/user/ai-earth/ai_earth/capabilities"
        os.makedirs(self.capabilities_path, exist_ok=True)

    def forge_capability(self, insight: str, capability_name: str) -> Dict[str, Any]:
        """
        Takes a breakthrough insight and forges it into a real Python capability.
        """
        logger.info(f"🔥 Forging new capability: {capability_name}...")

        # 1. Generate Python Code
        prompt = f"""
        Based on this breakthrough insight:
        {insight}

        Generate a high-quality, professional, and robust Python class named '{capability_name}' 
        that implements the logic described. 
        
        Requirements:
        - Use standard library or already installed packages (requests, pydantic, numpy, networkx).
        - Include detailed docstrings.
        - Add a 'run' method that executes the core logic.
        - The code must be production-ready and error-handled.

        Return ONLY the Python code. No markdown formatting blocks.
        """
        
        code = self.router.ask(prompt, model="gpt-4o")
        
        # Clean code
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        # 2. Persist to Disk
        file_name = f"{capability_name.lower()}.py"
        full_path = os.path.join(self.capabilities_path, file_name)
        
        with open(full_path, "w") as f:
            f.write(code)

        # 3. Log to Ledger
        ledger.log_synapse(
            task=f"Forge {capability_name}",
            process=f"Generated code size: {len(code)} chars",
            insight=f"Capability forged at {full_path}"
        )

        return {
            "capability": capability_name,
            "file_path": full_path,
            "status": "Forged",
            "code_preview": code[:500] + "..."
        }

    def load_capability(self, capability_name: str):
        """
        Dynamically loads a forged capability into the runtime.
        """
        file_name = f"{capability_name.lower()}.py"
        path = os.path.join(self.capabilities_path, file_name)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Capability {capability_name} not found.")

        spec = importlib.util.spec_from_file_location(capability_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return getattr(module, capability_name)()
