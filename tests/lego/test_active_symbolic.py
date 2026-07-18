import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth/lego'))

from active_symbolic.core import ActiveSymbolic

def test_active_symbolic_initialization():
    as_lego = ActiveSymbolic()
    assert as_lego.roles["Builder/Breaker"] is not None
    assert len(as_lego.flow_steps) == 6
    
def test_active_symbolic_info():
    as_lego = ActiveSymbolic()
    info = as_lego.info()
    assert info["pattern"] == "Category-Theoretic Composition"
    assert "MDL" in str(info["techniques"])

def test_active_symbolic_workflow():
    as_lego = ActiveSymbolic()
    as_lego.initialize_system_state({"data": "test"})
    assert as_lego.tracked_state["system_state"]["data"] == "test"
    
    opt = as_lego.optimize_workflow({})
    assert opt["optimized"] is True
