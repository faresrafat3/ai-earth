"""
Tests for AI Earth Platform API — FastAPI endpoints
====================================================
Tests all REST API endpoints using TestClient.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai_earth', 'lego'))
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from ai_earth.api import app, get_earth, get_evolve_core, get_router

client = TestClient(app)


# ══════════════════════════════════════════════════════════════════════
# 1. Platform Endpoints
# ══════════════════════════════════════════════════════════════════════

class TestPlatformEndpoints:
    """Test platform-level endpoints."""

    def test_root_info(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "lego_pieces" in data
        assert "totals" in data
        assert data["totals"]["tests"] >= 543

    def test_stats(self):
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "platform" in data
        assert "evolution" in data
        assert "models" in data

    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.4.0"


# ══════════════════════════════════════════════════════════════════════
# 2. Evolution Endpoints
# ══════════════════════════════════════════════════════════════════════

class TestEvolutionEndpoints:
    """Test evolution API endpoints."""

    def test_evolve_basic(self):
        response = client.post("/evolve", json={
            "task": "Analyze data patterns",
            "max_iterations": 2,
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["iterations"] == 2
        assert "final_score" in data

    def test_evolve_with_strategy(self):
        response = client.post("/evolve", json={
            "task": "Optimize prompts for better output",
            "max_iterations": 1,
            "strategy": "prompt_optimize",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["iterations"] >= 1

    def test_evolve_invalid_strategy(self):
        response = client.post("/evolve", json={
            "task": "Test",
            "strategy": "nonexistent",
        })
        assert response.status_code == 400

    def test_evolve_history(self):
        # First run an evolution
        client.post("/evolve", json={"task": "Test for history", "max_iterations": 1})
        
        response = client.get("/evolve/history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert len(data["history"]) >= 1

    def test_evolve_learnings(self):
        response = client.get("/evolve/learnings")
        assert response.status_code == 200
        data = response.json()
        assert "learnings" in data

    def test_evolve_learnings_filtered(self):
        response = client.get("/evolve/learnings?task_type=analysis")
        assert response.status_code == 200

    def test_evolve_strategies(self):
        response = client.get("/evolve/strategies")
        assert response.status_code == 200
        data = response.json()
        assert "strategies" in data
        assert "info" in data


# ══════════════════════════════════════════════════════════════════════
# 3. Model Router Endpoints
# ══════════════════════════════════════════════════════════════════════

class TestModelEndpoints:
    """Test model router API endpoints."""

    def test_list_models(self):
        response = client.get("/models")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert len(data["models"]) > 0

    def test_list_models_by_provider(self):
        response = client.get("/models?provider=openai")
        assert response.status_code == 200
        data = response.json()
        assert all(m["provider"] == "openai" for m in data["models"])

    def test_list_providers(self):
        response = client.get("/models/providers")
        assert response.status_code == 200
        data = response.json()
        assert "providers" in data
        assert "openai" in data["providers"]

    def test_chat(self):
        response = client.post("/chat", json={
            "prompt": "Hello, world!",
            "model": "gpt-4o-mini",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert "gpt-4o-mini" in data["model"]

    def test_chat_with_system(self):
        response = client.post("/chat", json={
            "prompt": "What is AI?",
            "system": "You are a helpful assistant",
        })
        assert response.status_code == 200


# ══════════════════════════════════════════════════════════════════════
# 4. Graph Endpoints
# ══════════════════════════════════════════════════════════════════════

class TestGraphEndpoints:
    """Test LangGraph API endpoints."""

    def test_create_graph(self):
        response = client.post("/graphs", json={
            "name": "research_graph",
            "state_fields": {"query": "str", "result": "str"},
        })
        assert response.status_code == 200
        data = response.json()
        assert data["created"] is True
        assert data["name"] == "research_graph"

    def test_list_graphs(self):
        # Create one first
        client.post("/graphs", json={"name": "test_graph"})
        
        response = client.get("/graphs")
        assert response.status_code == 200
        data = response.json()
        assert "graphs" in data
        assert "test_graph" in data["graphs"]


# ══════════════════════════════════════════════════════════════════════
# 5. Crew Endpoints
# ══════════════════════════════════════════════════════════════════════

class TestCrewEndpoints:
    """Test CrewAI API endpoints."""

    def test_create_crew(self):
        response = client.post("/crews", json={
            "name": "research_team",
            "agents": [
                {"name": "researcher", "role": "Researcher", "goal": "Find info"},
                {"name": "writer", "role": "Writer", "goal": "Write reports"},
            ],
        })
        assert response.status_code == 200
        data = response.json()
        assert data["created"] is True
        assert data["crew"]["name"] == "research_team"

    def test_list_crews(self):
        response = client.get("/crews")
        assert response.status_code == 200
        data = response.json()
        assert "crews" in data
        assert "agent_roles" in data


# ══════════════════════════════════════════════════════════════════════
# 6. Memory Endpoints
# ══════════════════════════════════════════════════════════════════════

class TestMemoryEndpoints:
    """Test memory API endpoints."""

    def test_create_memory(self):
        response = client.post("/memory", json={"name": "conversation"})
        assert response.status_code == 200
        data = response.json()
        assert data["created"] is True
        assert "conversation" in data["stores"]

    def test_list_memory(self):
        client.post("/memory", json={"name": "test_mem"})
        
        response = client.get("/memory")
        assert response.status_code == 200
        data = response.json()
        assert "stores" in data


# ══════════════════════════════════════════════════════════════════════
# 7. Composition Endpoint
# ══════════════════════════════════════════════════════════════════════

class TestComposeEndpoint:
    """Test workflow composition endpoint."""

    def test_compose_basic(self):
        # Setup prerequisites
        client.post("/graphs", json={"name": "comp_graph"})
        client.post("/crews", json={
            "name": "comp_crew",
            "agents": [{"name": "agent1", "role": "Worker", "goal": "Work"}],
        })
        client.post("/memory", json={"name": "comp_memory"})
        
        response = client.post("/compose", json={
            "name": "full_pipeline",
            "graph_name": "comp_graph",
            "crew_agents": ["agent1"],
            "memory_store": "comp_memory",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "full_pipeline"
        assert "pieces" in data


# ══════════════════════════════════════════════════════════════════════
# 8. LEGO Endpoints
# ══════════════════════════════════════════════════════════════════════

class TestLEGOEndpoints:
    """Test LEGO piece info endpoints."""

    def test_list_lego(self):
        response = client.get("/lego")
        assert response.status_code == 200
        data = response.json()
        assert "pieces" in data
        assert len(data["pieces"]) == 9
        assert "totals" in data

    def test_get_lego_piece(self):
        response = client.get("/lego/dspy")
        assert response.status_code == 200
        data = response.json()
        assert "source" in data
        assert "files" in data
        assert data["files"] == 148

    def test_get_lego_piece_case_insensitive(self):
        response = client.get("/lego/CrewAI")
        assert response.status_code == 200

    def test_get_lego_not_found(self):
        response = client.get("/lego/nonexistent")
        assert response.status_code == 404


# ══════════════════════════════════════════════════════════════════════
# 9. Timing Headers
# ══════════════════════════════════════════════════════════════════════

class TestTimingHeader:
    """Test that all responses include timing header."""

    def test_timing_header(self):
        response = client.get("/health")
        assert "x-process-time" in response.headers
        assert "s" in response.headers["x-process-time"]
