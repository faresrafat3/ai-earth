"""Stub for textgrad.optimizer module."""

class TextualGradientDescent:
    """Stub for TextualGradientDescent — the core TextGrad optimizer."""
    def __init__(self, engine, variables, constraints=None, **kwargs):
        self.engine = engine
        self.variables = variables
        self.constraints = constraints or []

    def step(self):
        raise NotImplementedError("Stub TextualGradientDescent — install textgrad for real usage")

    def zero_grad(self):
        pass
