"""
🧩 STORM LEGO Piece
═══════════════════════════════════════════════════════════
Source: "Assisting in Writing Wikipedia-like Articles from Scratch with Large Language Models" (STORM)
Pattern: Multi-Perspective Recursive Research
"""

import logging
from typing import List, Dict, Any
from ai_earth.model_router import ModelRouter

logger = logging.getLogger("ai_earth.lego.storm")

class STORM:
    """
    Implements the STORM research pattern:
    1. Multi-perspective Questioning (generate questions from different roles)
    2. Recursive Search (search for each question)
    3. Information Synthesis (organize findings into a structured report)
    """

    def __init__(self, router: ModelRouter = None):
        self.router = router or ModelRouter()

    def generate_perspectives(self, topic: str) -> List[str]:
        """Generate diverse expert perspectives for a topic."""
        prompt = f"Identify 3-5 diverse expert roles that would have different perspectives on the topic: '{topic}'. Just list the roles."
        response = self.router.ask(prompt, model="gpt-4o-mini")
        roles = [r.strip("- ") for r in response.split("\n") if r.strip()]
        return roles[:5]

    def generate_questions(self, topic: str, perspective: str) -> List[str]:
        """Generate specific research questions from a certain perspective."""
        prompt = f"As a(n) {perspective}, what are the 3 most critical questions you would ask to understand '{topic}' deeply?"
        response = self.router.ask(prompt, model="gpt-4o-mini")
        questions = [q.strip("12345. ") for q in response.split("\n") if q.strip()]
        return questions[:3]

    def deep_research(self, topic: str) -> Dict[str, Any]:
        """Run the full STORM research loop."""
        logger.info(f"Starting STORM deep research on: {topic}")
        
        # 1. Perspectives
        roles = self.generate_perspectives(topic)
        
        all_findings = []
        
        # 2. Multi-perspective Questioning + Search
        for role in roles:
            logger.info(f"Researching from perspective: {role}")
            questions = self.generate_questions(topic, role)
            
            role_results = {"perspective": role, "qa": []}
            for q in questions:
                # Use platform's web search via router
                search_results = self.router.web_search(q, num_results=2)
                context = "\n".join([r["snippet"] for r in search_results])
                
                # Synthesis of findings for this question
                answer_prompt = f"Topic: {topic}\nPerspective: {role}\nQuestion: {q}\n\nSearch Context:\n{context}\n\nSynthesize a detailed answer based ONLY on the context."
                answer = self.router.ask(answer_prompt, model="gpt-4o-mini")
                
                role_results["qa"].append({"question": q, "answer": answer})
            
            all_findings.append(role_results)
            
        # 3. Final Synthesis
        summary_prompt = f"Synthesize a comprehensive research report on '{topic}' using the following perspective-based findings:\n\n{str(all_findings)[:10000]}"
        final_report = self.router.ask(summary_prompt, model="gpt-4o")
        
        return {
            "topic": topic,
            "perspectives_explored": roles,
            "findings": all_findings,
            "final_report": final_report
        }

    def info(self):
        return {
            "name": "STORM",
            "pattern": "Recursive Multi-Perspective Research",
            "origin": "Stanford NLP"
        }
