"""
Decision Log — Records Every Architectural Decision

Every design choice in AI Earth is logged here with:
- What was decided
- Why it was decided
- What alternatives were considered
- What impact it has

This is the institutional memory of the project.

Reference: AGENT_DEVELOPMENT_CONTEXT.md §9 (6 decisions from GENESIS)

Last Updated: 2026-06-09
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional


@dataclass
class Decision:
    """A single architectural decision."""
    
    id: str                          # DECISION-NNN
    title: str                       # Short description
    date: str                        # YYYY-MM-DD
    context: str                     # Why this decision was needed
    decision: str                    # What was decided
    alternatives: List[str]          # What else was considered
    impact: str                      # What this affects
    decided_by: str                  # "F." or "A." or "F.+A."
    status: str = "active"           # active / superseded / deprecated
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Decision':
        return cls(**data)


# ═══════════════════════════════════════════════════════
# GENESIS LEGACY DECISIONS (Preserved from original project)
# ═══════════════════════════════════════════════════════

GENESIS_DECISIONS = [
    Decision(
        id="DECISION-001",
        title="global_before_local scope in INTENT_ENGINE",
        date="2026-06-08",
        context="micro_task run showed geographic bias (Egypt filter too early)",
        decision="Sub-goals search globally first, Egypt filter in last sub-goal only",
        alternatives=["Always local first", "No local filter", "Balanced global/local"],
        impact="INTENT_ENGINE goal_specification",
        decided_by="F.+A."
    ),
    Decision(
        id="DECISION-002",
        title="Sandbox = tmpdir subprocess (not Docker)",
        date="2026-06-08",
        context="Free tier infrastructure, Docker adds complexity and cost",
        decision="Use tmpdir subprocess for sandbox execution",
        alternatives=["Docker containers", "Firejail", "nsjail"],
        impact="SKILL_ENGINE, TOOL_HUB, all sandbox operations",
        decided_by="F.+A."
    ),
    Decision(
        id="DECISION-003",
        title="Backward compatibility — old imports stay working",
        date="2026-06-08",
        context="Orchestrator has many import points, changing all = risk",
        decision="genesis/tools/web_search.py never deleted, only wrapped",
        alternatives=["Big bang migration", "Feature flags"],
        impact="LEGACY_COMPAT layer, all imports",
        decided_by="F.+A."
    ),
    Decision(
        id="DECISION-004",
        title="AgentSpec JSON-serializable from day 1",
        date="2026-06-08",
        context="Future vibe-web interface requires REST API",
        decision="All AgentHub dataclasses must have to_dict() + from_dict()",
        alternatives=["Pickle serialization", "Protobuf"],
        impact="AGENT_HUB, future REST API, future web UI",
        decided_by="F.+A."
    ),
    Decision(
        id="DECISION-005",
        title="TextVariable = target_agent.py (not a prompt)",
        date="2026-06-08",
        context="GENESIS optimizes agents not prompts",
        decision="TextGrad gradient = 'what patterns in agent code led to improvement'",
        alternatives=["Optimize prompts", "Optimize system prompts only"],
        impact="META_ENGINE TextGrad implementation",
        decided_by="F.+A."
    ),
    Decision(
        id="DECISION-006",
        title="Skill extraction offline (after gen) not online (during gen)",
        date="2026-06-08",
        context="Runtime skill_create requires Docker-grade sandbox",
        decision="SKILL_ENGINE extracts from successful target_agent.py after evaluation",
        alternatives=["Online skill creation", "Human-in-the-loop extraction"],
        impact="SKILL_ENGINE extraction pipeline",
        decided_by="F.+A."
    ),
]


# ═══════════════════════════════════════════════════════
# AI EARTH NEW DECISIONS
# ═══════════════════════════════════════════════════════

AI_EARTH_DECISIONS = [
    Decision(
        id="DECISION-E001",
        title="AI Earth as separate repository from GENESIS",
        date="2026-06-09",
        context="Need clean architecture without GENESIS legacy baggage",
        decision="New repo 'AI-Earth' with clean structure, GENESIS as reference",
        alternatives=["Continue in GENESIS repo", "Monorepo with both"],
        impact="Project structure, CI/CD, documentation",
        decided_by="F."
    ),
    Decision(
        id="DECISION-E002",
        title="7-layer architecture",
        date="2026-06-09",
        context="Need clear separation of concerns and modularity",
        decision="7 layers: Infrastructure → Capabilities → Agents → Workflow → Safety → Memory → Insight",
        alternatives=["Flat structure", "3-layer", "Microservices"],
        impact="All components, directory structure, dependencies",
        decided_by="F.+A."
    ),
    Decision(
        id="DECISION-E003",
        title="Methodology files for AI Agent orchestration",
        date="2026-06-09",
        context="Need structured way to give commands to AI Agent executor",
        decision="dev/methodologies/ contains rule files that AI Agent reads before executing",
        alternatives=["Inline instructions", "Configuration files only"],
        impact="How F. orchestrates the AI Agent",
        decided_by="F."
    ),
    Decision(
        id="DECISION-E004",
        title="4-tier memory architecture",
        date="2026-06-09",
        context="Need different memory types for different use cases",
        decision="Working → Episodic → Semantic → Procedural with Knowledge Graph",
        alternatives=["Single vector DB", "Flat file storage", "2-tier only"],
        impact="MEMORY layer, Knowledge Graph, all agents",
        decided_by="F.+A."
    ),
]


def get_all_decisions() -> List[Decision]:
    """Get all decisions (GENESIS + AI Earth)."""
    return GENESIS_DECISIONS + AI_EARTH_DECISIONS


def get_decision(decision_id: str) -> Optional[Decision]:
    """Get a specific decision by ID."""
    for d in get_all_decisions():
        if d.id == decision_id:
            return d
    return None


def get_active_decisions() -> List[Decision]:
    """Get only active (non-superseded) decisions."""
    return [d for d in get_all_decisions() if d.status == "active"]
