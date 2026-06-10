"""Stub for gepa — lightweight replacement for import resolution."""
from __future__ import annotations

class EvaluationBatch:
    def __init__(self, *args, **kwargs):
        pass

class GEPAResult:
    def __init__(self, *args, **kwargs):
        pass

class GEPAAdapter:
    """Base adapter class — subscriptable for type hints."""
    def __init__(self, *args, **kwargs):
        pass
    
    def __class_getitem__(cls, item):
        return cls
