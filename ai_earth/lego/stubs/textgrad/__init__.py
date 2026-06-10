"""
Stub for textgrad library.
Source: https://github.com/zou-group/textgrad
This is a lightweight stub to allow imports without installing the full library.
"""
import logging

logger = logging.getLogger("textgrad")

class _StubFileHandler(logging.Handler):
    def emit(self, record):
        pass

sh = _StubFileHandler()

class Variable:
    """Stub for textgrad.Variable — represents a differentiable text variable."""
    def __init__(self, value, requires_grad=False, role_description=""):
        self.value = value
        self.requires_grad = requires_grad
        self.role_description = role_description
        self.parsed_outputs = {}
        self._gradients = []

    def get_short_value(self, n_words_offset=10):
        return self.value

    def __repr__(self):
        return f"Variable(value={self.value!r}, requires_grad={self.requires_grad})"

class EngineLM:
    """Stub for textgrad.EngineLM — LLM backend interface."""
    def generate(self, prompt, system_prompt=None, **kwargs):
        raise NotImplementedError("Stub EngineLM — install textgrad for real usage")

    def __call__(self, prompt, **kwargs):
        return self.generate(prompt, **kwargs)
