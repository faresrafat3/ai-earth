import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth/lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth'))

from agent_judge.core import AgentJudge

def test_agent_judge_info():
    judge = AgentJudge()
    assert judge.info()["name"] == "Agent-as-a-Judge"

@pytest.mark.llm
def test_agent_judge_evaluation():
    """LIVE: evaluate_trace makes a real LLM call through the pool."""
    judge = AgentJudge()
    res = judge.evaluate_trace("Add 2+2", "The answer is 5 because logic.")
    assert "score" in res
    assert "gaps" in res
