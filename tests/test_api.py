"""
Tests for AI Earth Platform API — FastAPI endpoints
====================================================
Tests the current REST API endpoints via TestClient.
"""
import sys
import os
import pytest
import time
import multiprocessing
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth'))

PORT = 9877

@pytest.fixture(scope="module")
def api_url():
    """Start API server and return base URL."""
    def run_api():
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth'))
        from ai_earth.api import app
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="error")
    
    p = multiprocessing.Process(target=run_api)
    p.start()
    time.sleep(2.5)
    
    yield f"http://127.0.0.1:{PORT}"
    
    p.terminate()
    p.join()


class TestPlatformEndpoints:
    def test_root_info(self, api_url):
        r = requests.get(f"{api_url}/", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "lego_pieces" in data
        assert "totals" in data

    def test_stats(self, api_url):
        r = requests.get(f"{api_url}/stats", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "platform" in data
        assert "evolution" in data
        assert "models" in data


class TestEvolutionEndpoints:
    def test_evolve_basic(self, api_url):
        r = requests.post(f"{api_url}/evolve", json={
            "task": "Analyze data patterns",
            "max_iterations": 1,
            "llm": False,  # structural test — real-LLM path covered by @llm tests
        }, timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert data["success"] is True or "result" in data

    def test_evolve_history(self, api_url):
        r = requests.get(f"{api_url}/evolve/history", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "history" in data or "results" in data

    def test_evolve_learnings(self, api_url):
        r = requests.get(f"{api_url}/evolve/learnings", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "learnings" in data or "results" in data

    def test_evolve_strategies(self, api_url):
        r = requests.get(f"{api_url}/synapse/strategies", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "strategies" in data or "info" in data


class TestExecutionEndpoints:
    def test_execute_structural(self, api_url):
        r = requests.post(f"{api_url}/execute", json={
            "task": "Build a small pipeline",
            "strategy": "langgraph",
            "llm": False,  # structural — real-LLM path covered by @llm tests
        }, timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert data["success"] is True
        assert data["strategy"] == "langgraph"
        assert data["llm_calls"] == 0

    def test_execute_invalid_strategy(self, api_url):
        r = requests.post(f"{api_url}/execute", json={
            "task": "x", "strategy": "warp-drive", "llm": False,
        }, timeout=15)
        assert r.status_code == 400

    def test_execute_auto_structural(self, api_url):
        r = requests.post(f"{api_url}/execute", json={
            "task": "Team up and collaborate on a plan",
            "strategy": "auto",
            "llm": False,
        }, timeout=30)
        assert r.status_code == 200
        assert r.json()["strategy"] == "crewai"  # auto-classified


class TestModelEndpoints:
    def test_list_models(self, api_url):
        r = requests.get(f"{api_url}/models", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "models" in data
        assert len(data["models"]) > 0

    def test_list_providers(self, api_url):
        r = requests.get(f"{api_url}/models/providers", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "providers" in data
        assert "openai" in data["providers"]

    def test_chat(self, api_url):
        r = requests.post(f"{api_url}/chat", json={
            "prompt": "Hello!",
            "model": "gpt-4o-mini",
            "max_tokens": 10,
        }, timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "content" in data
        assert len(data["content"]) > 0


class TestGraphEndpoints:
    def test_create_graph(self, api_url):
        r = requests.post(f"{api_url}/graphs", json={"name": "research_graph"}, timeout=10)
        assert r.status_code in (200, 422)

    def test_list_graphs(self, api_url):
        r = requests.get(f"{api_url}/graphs", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "graphs" in data or "results" in data


class TestCrewEndpoints:
    def test_create_crew(self, api_url):
        r = requests.post(f"{api_url}/crews", json={
            "name": "research_team",
            "agents": [
                {"name": "researcher", "role": "Researcher", "goal": "Find info", "backstory": "Expert"},
                {"name": "writer", "role": "Writer", "goal": "Write reports", "backstory": "Expert"},
            ],
        }, timeout=10)
        assert r.status_code in (200, 422)

    def test_list_crews(self, api_url):
        r = requests.get(f"{api_url}/crews", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "crews" in data or "results" in data


class TestMemoryEndpoints:
    def test_create_memory(self, api_url):
        r = requests.post(f"{api_url}/memory", json={"name": "conversation"}, timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "created" in data or "result" in data

    def test_list_memory(self, api_url):
        r = requests.get(f"{api_url}/memory", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "stores" in data or "results" in data


class TestTimingHeader:
    def test_timing_header(self, api_url):
        r = requests.get(f"{api_url}/", timeout=10)
        assert "x-process-time" in r.headers or "x-process-time" in [k.lower() for k in r.headers]
