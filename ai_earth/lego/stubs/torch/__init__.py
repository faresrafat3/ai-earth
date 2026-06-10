"""Stub for torch (PyTorch) — lightweight import-only stub."""
import numpy as np

def tensor(data, *args, **kwargs):
    return np.array(data)

def no_grad():
    class _NoGrad:
        def __enter__(self): return self
        def __exit__(self, *a): pass
    return _NoGrad()

def load(path, *args, **kwargs):
    raise NotImplementedError("Stub torch.load — install PyTorch for real usage")

def save(obj, path, *args, **kwargs):
    raise NotImplementedError("Stub torch.save — install PyTorch for real usage")

class nn:
    class Module:
        pass

class optim:
    class Optimizer:
        pass
