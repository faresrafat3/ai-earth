import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth/lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai_earth'))

from agent_judge.core import AgentJudge

def test_agent_judge_info():
    judge = AgentJudge()
    assert judge.info()["name"] == "Agent-as-a-Judge"

def test_agent_judge_evaluation():
    judge = AgentJudge()
    # Mock behavior testing structure
    res = judge.evaluate_trace("Add 2+2", "The answer is 5 because logic.")
    assert "score" in res
    assert "gaps" in res
