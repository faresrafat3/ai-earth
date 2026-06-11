import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth/lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth'))

from self_discover.core import SelfDiscover

def test_self_discover_selection():
    sd = SelfDiscover()
    modules = sd.select_modules("Solve a physics problem")
    assert len(modules) > 0

def test_self_discover_info():
    sd = SelfDiscover()
    assert sd.info()["name"] == "SelfDiscover"
    assert "Google" in sd.info()["origin"]
