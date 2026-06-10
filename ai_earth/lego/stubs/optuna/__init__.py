"""
Stub for optuna library.
Source: https://github.com/optuna/optuna
"""

class Trial:
    """Stub for optuna Trial."""
    def suggest_float(self, name, low, high, *args, **kwargs):
        return (low + high) / 2
    def suggest_int(self, name, low, high, *args, **kwargs):
        return (low + high) // 2
    def suggest_categorical(self, name, choices):
        return choices[0]
    def suggest_uniform(self, name, low, high):
        return (low + high) / 2

class FrozenTrial:
    """Stub for optuna FrozenTrial."""
    pass

class Study:
    """Stub for optuna Study."""
    def __init__(self, **kwargs):
        self.trials = []
        self.best_params = {}
        self.best_value = None
    def optimize(self, func, n_trials=100, **kwargs):
        raise NotImplementedError("Stub Study.optimize — install optuna for real usage")

def create_study(**kwargs):
    return Study(**kwargs)

def get_all_study_summaries(**kwargs):
    return []

# Namespaces
class _TrialModule:
    Trial = Trial
    FrozenTrial = FrozenTrial

trial = _TrialModule()
