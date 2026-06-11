"""
🧩 Agent-as-a-Judge LEGO Piece
═══════════════════════════════════════════════════════════
Source: "Agent-as-a-Judge: Predict, Explain, and Improve Reasoning Systems" (2025)
Pattern: Self-Correcting Meta-Reasoning
"""

import logging
from typing import List, Dict, Any
from ai_earth.model_router import ModelRouter

logger = logging.getLogger("ai_earth.lego.agent_judge")

class AgentJudge:
    """
    Implements the Agent-as-a-Judge pattern:
    1. PREDICT: Guess the success probability of a reasoning trace.
    2. EXPLAIN: Provide a justification for the prediction.
    3. IMPROVE: Generate a corrected or enhanced reasoning path.
    """

    def __init__(self, router: ModelRouter = None):
        self.router = router or ModelRouter()

    def evaluate_trace(self, task: str, reasoning_trace: str) -> Dict[str, Any]:
        """Evaluates a reasoning path and provides feedback."""
        prompt = f"""
        TASK: {task}
        REASONING TRACE: {reasoning_trace}

        Act as a Meta-Judge. 
        1. Rate this reasoning (0.0 to 1.0).
        2. Identify the logical gaps.
        3. Suggest a specific improvement.

        Return in JSON format: {{"score": float, "gaps": [], "improvement": str}}
        """
        
        response = self.router.chat(
            model="gpt-4o",
            prompt=prompt,
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.content)

    def self_correct(self, task: str, original_solution: str) -> str:
        """Runs the judge and then generates a corrected solution."""
        logger.info(f"⚖️ AgentJudge is auditing solution for: {task}")
        
        evaluation = self.evaluate_trace(task, original_solution)
        
        if evaluation['score'] > 0.9:
            return original_solution
            
        correction_prompt = f"""
        Original Task: {task}
        Original Solution: {original_solution}
        Judge's Feedback: {evaluation['improvement']}
        
        Generate an improved, verified solution that addresses all feedback.
        """
        
        return self.router.ask(correction_prompt, model="gpt-4o")

    def info(self):
        return {
            "name": "Agent-as-a-Judge",
            "capability": "Meta-Evaluation & Self-Correction",
            "year": 2025
        }
