"""DSPy evaluate module."""
from dspy.evaluate.evaluate import Evaluate
from dspy.evaluate.metrics import normalize_text, answer_exact_match, answer_passage_match
from dspy.evaluate.auto_evaluation import SemanticF1

__all__ = ["Evaluate", "normalize_text", "answer_exact_match", "answer_passage_match", "SemanticF1"]
