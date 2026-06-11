"""
🧩 Self-Discover LEGO Piece
═══════════════════════════════════════════════════════════
Source: "SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures" (Google DeepMind)
Pattern: Task-Intrinsic Reasoning Structure Composition
"""

import logging
from typing import List, Dict, Any
from ai_earth.model_router import ModelRouter

logger = logging.getLogger("ai_earth.lego.self_discover")

class SelfDiscover:
    """
    Implements the Self-Discover pattern:
    1. SELECT: Choose relevant atomic reasoning modules.
    2. ADAPT: Tailor modules to the specific task.
    3. IMPLEMENT: Compose modules into a structured plan.
    """

    def __init__(self, router: ModelRouter = None):
        self.router = router or ModelRouter()
        self.atomic_modules = [
            "Critical Thinking",
            "Step-by-Step Thinking",
            "Hypothesis Testing",
            "Analogical Reasoning",
            "Recursive Decomposition"
        ]

    def select_modules(self, task: str) -> List[str]:
        """LLM selects relevant atomic reasoning modules for the task."""
        prompt = f"Given this task: '{task}', select the top 3 most relevant reasoning modules from this list: {self.atomic_modules}. Just list them."
        response = self.router.ask(prompt, model="gpt-4o-mini")
        selected = [m.strip("- ") for m in response.split("\n") if m.strip()]
        return selected[:3]

    def compose_structure(self, task: str, selected_modules: List[str]) -> str:
        """LLM composes selected modules into a specific reasoning structure."""
        prompt = f"Task: {task}\nSelected Modules: {selected_modules}\n\nCompose these modules into an explicit, step-by-step reasoning structure (plan) to solve the task."
        structure = self.router.ask(prompt, model="gpt-4o")
        return structure

    def solve(self, task: str) -> Dict[str, Any]:
        """Execute the self-discover flow."""
        logger.info(f"Self-Discover starting for task: {task}")
        
        # 1. Select
        modules = self.select_modules(task)
        
        # 2. Compose
        structure = self.compose_structure(task, modules)
        
        # 3. Execute (Solve)
        solve_prompt = f"Follow this reasoning structure to solve the task:\n\nStructure:\n{structure}\n\nTask: {task}\n\nFinal Answer:"
        final_answer = self.router.ask(solve_prompt, model="gpt-4o")
        
        return {
            "task": task,
            "selected_modules": modules,
            "reasoning_structure": structure,
            "final_answer": final_answer
        }

    def info(self):
        return {
            "name": "SelfDiscover",
            "origin": "Google DeepMind",
            "pattern": "Self-Composed Reasoning"
        }
