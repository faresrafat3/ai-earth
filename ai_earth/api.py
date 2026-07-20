"""
🌐 AI Earth — Platform API
═══════════════════════════════════════════════════════════
REST API exposing all platform capabilities via FastAPI.

Endpoints:
    GET  /                          — Platform info
    GET  /stats                     — Detailed statistics
    GET  /health                    — Health check

    POST /evolve                    — Run self-evolution loop
    GET  /evolve/history            — Get evolution history
    GET  /evolve/learnings          — Get stored learnings
    GET  /evolve/strategies         — Get learned strategies

    GET  /models                    — List available models
    GET  /models/providers          — List providers & availability
    POST /chat                      — Chat with real LLM via Key Pool

    POST /graphs                    — Create a LangGraph graph
    GET  /graphs                    — List all graphs

    POST /crews                     — Create a crew
    GET  /crews                     — List all crews

    POST /memory                    — Create memory store
    GET  /memory                    — List memory stores

    POST /compose                   — Compose multi-piece workflow

    GET  /lego                      — List all LEGO pieces
    GET  /lego/{name}               — Get LEGO piece details

Usage:
    uvicorn ai_earth.api:app --host 0.0.0.0 --port 8000 --reload

    # Then visit:
    http://localhost:8000/docs        — Swagger UI
    http://localhost:8000/redoc       — ReDoc
"""

from __future__ import annotations

import sys
import os
import time
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Ensure LEGO paths are available
_lego_path = os.path.join(os.path.dirname(__file__), 'lego')
_stubs_path = os.path.join(_lego_path, 'stubs')
if _stubs_path not in sys.path:
    sys.path.append(_stubs_path)
if _lego_path not in sys.path:
    sys.path.insert(0, _lego_path)


# ═════════════════════════════════════════════════════════
# Pydantic Request/Response Models
# ═════════════════════════════════════════════════════════

class EvolveRequest(BaseModel):
    """Request for self-evolution."""
    task: str = Field(..., description="Natural language task description", min_length=1)
    max_iterations: int = Field(3, description="Max evolution iterations", ge=1, le=20)
    strategy: str = Field("hybrid", description="Evolution strategy")
    quality_threshold: float = Field(0.8, description="Target quality score", ge=0.0, le=1.0)
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    llm: bool = Field(True, description="Use real LLM intelligence in the evolution phases (False = deterministic offline mode)")

class ExecuteRequest(BaseModel):
    """Request to execute a task through a LEGO strategy."""
    task: str = Field(..., description="Natural language task", min_length=1)
    strategy: str = Field("auto", description="langgraph | crewai | autogen | dspy | hybrid | auto")
    context: Optional[Dict[str, Any]] = Field(None, description="Extra context")
    llm: bool = Field(True, description="Real LLM intelligence (False = structural mode, zero API calls)")
    budget: int = Field(6, description="Max LLM calls for this run", ge=0, le=12)

class ChatRequest(BaseModel):
    """Request for LLM chat."""
    prompt: str = Field(..., description="User prompt", min_length=1)
    model: Optional[str] = Field(None, description="Model to use")
    system: Optional[str] = Field(None, description="System prompt")
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(2048, ge=1, le=100000)

class GraphCreateRequest(BaseModel):
    """Request to create a LangGraph graph."""
    name: str = Field(..., description="Graph name", min_length=1)
    state_fields: Dict[str, str] = Field(
        default={"messages": "list", "context": "str"},
        description="State schema fields: {name: type}",
    )

class CrewCreateRequest(BaseModel):
    """Request to create a crew."""
    name: str = Field(..., description="Crew name", min_length=1)
    agents: List[Dict[str, str]] = Field(
        ..., description="List of agent defs: [{name, role, goal, backstory?}]",
        min_length=1,
    )
    process: str = Field("sequential", description="Process type: sequential|hierarchical")

class MemoryCreateRequest(BaseModel):
    """Request to create a memory store."""
    name: str = Field(..., description="Store name", min_length=1)
    config: Optional[Dict[str, Any]] = Field(None, description="Memory config")

class ComposeRequest(BaseModel):
    """Request to compose a multi-piece workflow."""
    name: str = Field(..., description="Workflow name", min_length=1)
    graph_name: Optional[str] = Field(None, description="LangGraph graph to use")
    crew_agents: Optional[List[str]] = Field(None, description="Crew agent names")
    memory_store: Optional[str] = Field(None, description="Memory store to use")

class ResearchRequest(BaseModel):
    """Request for intelligence discovery."""
    topic: str = Field(..., description="Research topic", min_length=1)
    count: int = Field(3, description="Number of papers to aggregate", ge=1, le=10)

class DigestRequest(BaseModel):
    """Request to digest a specific paper."""
    url: str = Field(..., description="Paper URL")
    name: str = Field(..., description="Desired LEGO piece name")


# ═════════════════════════════════════════════════════════
# App Initialization
# ═════════════════════════════════════════════════════════

app = FastAPI(
    title="🌍 AI Earth — The Living Intelligence Ecosystem",
    description="Self-evolving AI intelligence aggregation platform built from LEGO pieces extracted from research papers",
    version="0.4.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Platform state (lazy-initialized)
_earth = None
_evolve_core = None
_router = None


def get_earth():
    """Get or create the AIEarth orchestrator."""
    global _earth
    if _earth is None:
        from ai_earth.orchestrator import AIEarth
        _earth = AIEarth()
    return _earth


def get_evolve_core():
    """Get or create the SelfEvolveCore."""
    global _evolve_core
    if _evolve_core is None:
        from ai_earth.self_evolve import SelfEvolveCore
        _evolve_core = SelfEvolveCore()
    return _evolve_core


def get_router():
    """Get or create the ModelRouter."""
    global _router
    if _router is None:
        from ai_earth.model_router import ModelRouter
        _router = ModelRouter()
    return _router


# ═════════════════════════════════════════════════════════
# Middleware
# ═════════════════════════════════════════════════════════

@app.middleware("http")
async def add_timing_header(request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    response.headers["X-Process-Time"] = f"{elapsed:.3f}s"
    return response


# ═════════════════════════════════════════════════════════
# Platform Endpoints
# ═════════════════════════════════════════════════════════

@app.get("/", tags=["Platform"])
async def platform_info():
    """Get platform information including all LEGO pieces."""
    earth = get_earth()
    return earth.platform_info()


@app.get("/stats", tags=["Platform"])
async def platform_stats():
    """Get human-readable platform statistics."""
    earth = get_earth()
    core = get_evolve_core()
    return {
        "platform": earth.platform_stats(),
        "evolution": core.stats(),
        "models": get_router().info(),
    }


@app.post("/research/discover", tags=["Research"])
async def discover_intelligence(req: ResearchRequest):
    """Discover and aggregate intelligence on a topic."""
    earth = get_earth()
    try:
        result = earth.discover_intelligence(req.topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research/deep", tags=["Research"])
async def deep_research(req: ResearchRequest):
    """Run deep multi-perspective STORM research."""
    earth = get_earth()
    try:
        result = earth.deep_research(req.topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synapse/think", tags=["Core"])
async def synapse_think(req: ResearchRequest):
    """Run High-Order Synthesis through the Synapse Kernel."""
    earth = get_earth()
    try:
        # Re-using ResearchRequest for topic input
        result = earth.synapse_think(req.topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research/digest", tags=["Research"])
async def digest_paper(req: DigestRequest):
    """Digest a paper: extract DNA and generate LEGO code."""
    earth = get_earth()
    try:
        result = earth.digest_research(req.url, req.name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═════════════════════════════════════════════════════════
# Evolution Endpoints
# ═════════════════════════════════════════════════════════

@app.post("/evolve", tags=["Evolution"])
async def run_evolution(req: EvolveRequest):
    """Run the self-evolution loop on a task."""
    core = get_evolve_core()
    from ai_earth.self_evolve import Strategy
    
    try:
        strategy = Strategy(req.strategy)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid strategy '{req.strategy}'. Valid: {[s.value for s in Strategy]}",
        )
    
    # Configure core
    core._quality_threshold = req.quality_threshold
    core._llm_enabled = req.llm  # caller controls real-LLM vs offline deterministic
    
    result = core.evolve(
        task=req.task,
        max_iterations=req.max_iterations,
        strategy=strategy,
        context=req.context,
    )
    
    return result.to_dict()


@app.post("/execute", tags=["Execution"])
async def execute_task(req: ExecuteRequest):
    """Execute a task through a LEGO strategy with real LLM intelligence."""
    from ai_earth.executor import ExecutionEngine, ExecStrategy
    valid = [s.value for s in ExecStrategy]
    if req.strategy not in valid:
        raise HTTPException(status_code=400, detail=f"Invalid strategy '{req.strategy}'. Valid: {valid}")
    engine = ExecutionEngine(llm=req.llm, llm_budget_per_run=req.budget)
    result = engine.run(req.task, strategy=req.strategy, context=req.context)
    return result.to_dict()


@app.get("/evolve/history", tags=["Evolution"])
async def evolution_history(limit: int = Query(10, ge=1, le=100)):
    """Get evolution history."""
    core = get_evolve_core()
    return {"history": core.evolution_history()[-limit:]}


@app.get("/evolve/learnings", tags=["Evolution"])
async def evolution_learnings(
    task_type: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
):
    """Get stored learnings."""
    core = get_evolve_core()
    return {"learnings": core.get_learning(task_type=task_type, limit=limit)}


@app.get("/synapse/strategies", tags=["Evolution"])
async def evolution_strategies():
    """Get learned strategies and their weights."""
    core = get_evolve_core()
    return {
        "strategies": core.learned_strategies(),
        "info": core.info(),
    }

@app.get("/ledger/stats", tags=["Data"])
async def get_ledger_stats():
    """Get stats from the OmniLog Database."""
    from ai_earth.core.database import ledger
    return ledger.get_stats()

@app.get("/ledger/export", tags=["Data"])
async def export_training_data():
    """Export training data in JSONL format."""
    path = "/home/user/ai-earth/data/vault/llm_training_data.jsonl"
    if os.path.exists(path):
        with open(path, "r") as f:
            return {"data": [json.loads(line) for line in f.readlines()]}
    return {"data": []}


# ═════════════════════════════════════════════════════════
# Quota Ledger Endpoints (daily rate-limit protection)
# ═════════════════════════════════════════════════════════

@app.get("/quota", tags=["Quota"])
async def get_quota_status():
    """Today's per-provider usage vs daily caps (persistent across sessions)."""
    from ai_earth.core.quota_ledger import get_ledger
    return get_ledger().status()

@app.get("/quota/history", tags=["Quota"])
async def get_quota_history(days: int = Query(7, ge=1, le=30)):
    """Last N days of provider usage from the persistent ledger."""
    from ai_earth.core.quota_ledger import get_ledger
    return {"days": get_ledger().history(days=days)}


# ═════════════════════════════════════════════════════════
# Memory Vault Endpoints (cross-session persistent memory)
# ═════════════════════════════════════════════════════════

@app.get("/vault", tags=["Vault"])
async def get_vault_stats():
    """Vault overview: namespaces, entry counts, size on disk."""
    from ai_earth.memory.vault import MemoryVault
    return MemoryVault().stats()

@app.get("/vault/{namespace}", tags=["Vault"])
async def get_vault_namespace(
    namespace: str,
    key: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = Query(20, ge=1, le=200),
):
    """Recall entries from one vault namespace (newest last)."""
    from ai_earth.memory.vault import MemoryVault
    vault = MemoryVault()
    if namespace not in vault.namespaces():
        raise HTTPException(status_code=404, detail=f"namespace '{namespace}' not found. Available: {vault.namespaces()}")
    return {
        "namespace": namespace,
        "entries": vault.recall(namespace, key=key, tag=tag, limit=limit),
    }


# ═════════════════════════════════════════════════════════
# Model Router Endpoints
# ═════════════════════════════════════════════════════════

@app.get("/models", tags=["Models"])
async def list_models(provider: Optional[str] = None):
    """List available models, optionally filtered by provider."""
    router = get_router()
    return {"models": router.list_models(provider=provider)}


@app.get("/models/providers", tags=["Models"])
async def list_providers():
    """List LLM providers and their availability."""
    router = get_router()
    return {"providers": router.list_providers()}


@app.post("/chat", tags=["Models"])
async def chat(req: ChatRequest):
    """Chat with a real LLM via the Key Pool."""
    router = get_router()
    try:
        response = router.chat(
            model=req.model,
            prompt=req.prompt,
            system=req.system,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        return {
            "content": response.content,
            "model": response.model,
            "provider": response.provider.value if hasattr(response.provider, "value") else str(response.provider),
            "usage": response.usage,
            "latency_ms": response.latency_ms,
            "cached": response.cached,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═════════════════════════════════════════════════════════
# Graph Endpoints (LangGraph)
# ═════════════════════════════════════════════════════════

@app.post("/graphs", tags=["Graphs"])
async def create_graph(req: GraphCreateRequest):
    """Create a LangGraph StateGraph."""
    earth = get_earth()
    bridge = earth.bridge()
    
    graph = bridge.create_graph(req.name)
    return {
        "name": req.name,
        "state_fields": req.state_fields,
        "created": True,
        "graphs": bridge.list_graphs(),
    }


@app.get("/graphs", tags=["Graphs"])
async def list_graphs():
    """List all registered graphs."""
    earth = get_earth()
    return {"graphs": earth.bridge().list_graphs()}


# ═════════════════════════════════════════════════════════
# Crew Endpoints (CrewAI)
# ═════════════════════════════════════════════════════════

@app.post("/crews", tags=["Crews"])
async def create_crew(req: CrewCreateRequest):
    """Create a crew with agent roles."""
    earth = get_earth()
    crew = earth.create_crew(req.name, req.agents)
    return {
        "created": True,
        "crew": crew,
    }


@app.get("/crews", tags=["Crews"])
async def list_crews():
    """List all registered crews."""
    earth = get_earth()
    bridge = earth.bridge()
    return {
        "crews": list(bridge._crews.keys()),
        "agent_roles": bridge.list_agent_roles(),
    }


# ═════════════════════════════════════════════════════════
# Memory Endpoints (Mem0)
# ═════════════════════════════════════════════════════════

@app.post("/memory", tags=["Memory"])
async def create_memory(req: MemoryCreateRequest):
    """Create a memory store."""
    earth = get_earth()
    memory = earth.create_memory(req.name, req.config)
    return {
        "created": True,
        "name": req.name,
        "stores": earth.bridge().list_memory_stores(),
    }


@app.get("/memory", tags=["Memory"])
async def list_memory():
    """List all memory stores."""
    earth = get_earth()
    return {"stores": earth.bridge().list_memory_stores()}


# ═════════════════════════════════════════════════════════
# Composition Endpoint
# ═════════════════════════════════════════════════════════

@app.post("/compose", tags=["Compose"])
async def compose_workflow(req: ComposeRequest):
    """Compose a workflow from multiple LEGO pieces."""
    earth = get_earth()
    composed = earth.compose(
        req.name,
        graph_name=req.graph_name,
        crew_agents=req.crew_agents,
        memory_store=req.memory_store,
    )
    return composed


# ═════════════════════════════════════════════════════════
# LEGO Pieces Endpoints
# ═════════════════════════════════════════════════════════

@app.get("/lego", tags=["LEGO"])
async def list_lego_pieces():
    """List all LEGO pieces."""
    earth = get_earth()
    info = earth.platform_info()
    return {"pieces": info["lego_pieces"], "totals": info["totals"]}


@app.get("/lego/{name}", tags=["LEGO"])
async def get_lego_piece(name: str):
    """Get details about a specific LEGO piece."""
    earth = get_earth()
    info = earth.platform_info()
    name_lower = name.lower()
    
    if name_lower in info["lego_pieces"]:
        return info["lego_pieces"][name_lower]
    
    raise HTTPException(
        status_code=404,
        detail=f"LEGO piece '{name}' not found. Available: {list(info['lego_pieces'].keys())}",
    )
