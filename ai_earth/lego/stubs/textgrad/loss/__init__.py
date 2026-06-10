"""Stub for textgrad.loss module."""

class TextLoss:
    """Stub for TextLoss — computes textual gradient from evaluation."""
    def __init__(self, evaluation_instruction, engine):
        self.evaluation_instruction = evaluation_instruction
        self.engine = engine

    def __call__(self, output, *args, **kwargs):
        raise NotImplementedError("Stub TextLoss — install textgrad for real usage")

class MultiFieldEvaluation:
    """Stub for MultiFieldEvaluation — multi-field loss function."""
    def __init__(self, evaluation_instruction, role_descriptions, engine):
        self.evaluation_instruction = evaluation_instruction
        self.role_descriptions = role_descriptions
        self.engine = engine

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Stub MultiFieldEvaluation — install textgrad for real usage")
