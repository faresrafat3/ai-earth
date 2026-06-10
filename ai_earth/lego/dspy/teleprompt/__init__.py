"""DSPy teleprompt module — optimizers for compiling DSPy programs."""
from dspy.teleprompt.teleprompt import Teleprompter
from dspy.teleprompt.vanilla import LabeledFewShot
from dspy.teleprompt.bootstrap import BootstrapFewShot
from dspy.teleprompt.ensemble import Ensemble
from dspy.teleprompt.random_search import BootstrapFewShotWithRandomSearch

__all__ = [
    "Teleprompter", "LabeledFewShot", "BootstrapFewShot",
    "Ensemble", "BootstrapFewShotWithRandomSearch",
]
