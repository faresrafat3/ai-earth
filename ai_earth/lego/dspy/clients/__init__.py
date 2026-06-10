"""DSPy clients module — LM abstraction layer."""
from dspy.clients.base_lm import BaseLM
from dspy.clients.lm import LM
from dspy.clients.provider import Provider

try:
    from dspy.clients.embedding import Embedder
except ImportError:
    class Embedder:
        """Stub Embedder for when embedding deps are missing."""
        def __init__(self, *args, **kwargs):
            pass
        def __call__(self, *args, **kwargs):
            raise NotImplementedError("Embedder requires embedding dependencies")

__all__ = ["BaseLM", "LM", "Provider", "Embedder"]
