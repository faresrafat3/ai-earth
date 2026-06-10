"""
Stub for dspy library.
Source: https://github.com/stanfordnlp/dspy
Lightweight stub to allow imports without installing the full library.
"""

class Signature:
    """Stub for DSPy Signature."""
    def __init__(self, *args, **kwargs):
        pass

class Module:
    """Stub for DSPy Module base class."""
    def __init__(self):
        pass
    
    def forward(self, **kwargs):
        raise NotImplementedError
    
    def __call__(self, **kwargs):
        return self.forward(**kwargs)

class Predict(Module):
    """Stub for DSPy Predict."""
    pass

class Example:
    """Stub for DSPy Example."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class Settings:
    """Stub for DSPy settings."""
    def __init__(self):
        self.configure = lambda *a, **kw: None

settings = Settings()

def load(*args, **kwargs):
    """Stub for DSPy load."""
    return None

class MIPROv2:
    """Stub for DSPy MIPROv2 optimizer."""
    def __init__(self, *args, **kwargs):
        pass
    def compile(self, *args, **kwargs):
        raise NotImplementedError("Stub MIPROv2 — install dspy for real usage")

class LM:
    """Stub for DSPy LM."""
    def __init__(self, *args, **kwargs):
        pass

class Provider:
    """Stub for DSPy Provider."""
    pass

# utils namespace
class _Utils:
    pass
utils = _Utils()
