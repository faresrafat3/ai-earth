import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth/lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth'))

from storm.core import STORM

@pytest.mark.llm
def test_storm_perspectives():
    """LIVE: generate_perspectives makes a real LLM call through the pool."""
    storm = STORM()
    roles = storm.generate_perspectives("Quantum Computing")
    assert isinstance(roles, list)
    assert len(roles) > 0

@pytest.mark.llm
def test_storm_questions():
    """LIVE: generate_questions makes a real LLM call through the pool."""
    storm = STORM()
    qs = storm.generate_questions("AI Ethics", "Legal Expert")
    assert len(qs) > 0
    # The first line might be introductory, but questions should exist
    assert any("?" in q for q in qs)

def test_storm_info():
    storm = STORM()
    assert storm.info()["name"] == "STORM"
