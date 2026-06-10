"""Stub for spacy NLP."""
def load(*a, **kw):
    class NLP:
        def __call__(self, text): return Doc()
    class Doc:
        @property
        def ents(self): return []
    return NLP()
