"""
🧬 LEGO DNA Extractor
═══════════════════════════════════════════════════════════
The "Digestion Engine" of AI Earth. Extracts the structural logic
and agentic patterns from research papers to turn them into LEGO.
"""

from typing import List, Dict, Any
import logging
import json
from ai_earth.model_router import ModelRouter

logger = logging.getLogger("ai_earth.dna_extractor")

class DNAExtractor:
    def __init__(self, router: ModelRouter = None):
        self.router = router or ModelRouter()

    def extract_dna(self, paper_content: str) -> Dict[str, Any]:
        """
        Analyze paper content and extract the 'Agentic DNA'.
        """
        prompt = f"""
        Analyze the following AI research paper and extract its 'Agentic DNA' in a structured JSON format.
        Focus on how to implement this as a composable LEGO piece.

        Structure to extract:
        1. Core Pattern (e.g., Graph, Sequential, Tree, Multi-Agent)
        2. Roles (What agents are defined and what are their specific goals?)
        3. Flow (What are the steps or transitions between states?)
        4. Optimization (Does the paper suggest a new way to optimize prompts or workflows?)
        5. State (What data is tracked throughout the process?)

        Paper Content:
        {paper_content[:10000]}

        Return ONLY a JSON object.
        """
        
        response = self.router.chat(
            model="gpt-4o",  # Using a smart model for extraction
            prompt=prompt,
            response_format={"type": "json_object"}
        )
        
        try:
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            return json.loads(content.strip())
        except Exception as e:
            logger.error(f"Failed to parse DNA JSON: {e}")
            return {"error": "Failed to parse extraction", "raw": response.content}

    def generate_lego_stub(self, dna: Dict[str, Any], name: str) -> str:
        """
        Generate a Python stub file for the new LEGO piece based on its DNA.
        """
        prompt = f"""
        Based on the following Agentic DNA extracted from a research paper, 
        generate a clean, modular Python class that follows the AI Earth LEGO pattern.
        
        DNA:
        {json.dumps(dna, indent=2)}
        
        Name: {name}
        
        The class should be ready to be integrated via CrossPieceBridge.
        Include docstrings and placeholders for the core logic.
        """
        
        code = self.router.ask(prompt, model="gpt-4o")
        return code
