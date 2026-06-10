"""Stub for textgrad.autograd module."""

class StringBasedFunction:
    """Stub for textgrad StringBasedFunction — wraps a callable as a differentiable function."""
    def __init__(self, func, description=""):
        self.func = func
        self.description = description

    def __call__(self, inputs, output_description=""):
        if isinstance(inputs, dict):
            return self.func(**inputs)
        return self.func(inputs)
