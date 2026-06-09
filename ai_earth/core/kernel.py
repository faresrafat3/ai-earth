"""
Kernel — Immutable Invariants

The kernel defines rules that CANNOT be changed at runtime.
These are the sacred boundaries of the system.

Inspired by: Garrus800-stack/genesis-agent Kernel architecture

Decision: DECISION-K001
    The kernel is the foundation — nothing can override these rules.
    Not the agent, not the orchestrator, not even the developer (without code change).

Last Updated: 2026-06-09
"""

from dataclasses import dataclass


# ═══════════════════════════════════════════════════════
# IMMUTABLE CONSTANTS
# ═══════════════════════════════════════════════════════

MAX_GENERATIONS_DEFAULT = 10
MAX_COST_USD_HARD_CAP = 50.0  # Never exceed $50 per run
MIN_TESTS_PASS_RATE = 1.0     # 100% — never commit with failing tests
MAX_HALLUCINATION_RATE = 0.5  # If > 50%, halt generation


@dataclass(frozen=True)
class PreservationInvariants:
    """
    11 Preservation Invariants — Cannot be broken.
    
    These rules protect system integrity regardless of what
    the agent, orchestrator, or any component does.
    """
    
    # 1. Tests must pass
    ALL_TESTS_MUST_PASS: bool = True
    
    # 2. No API keys in code
    NO_CREDENTIALS_IN_CODE: bool = True
    
    # 3. Backward compatibility
    OLD_IMPORTS_MUST_WORK: bool = True
    
    # 4. Budget is hard cap
    BUDGET_IS_HARD_CAP: bool = True
    
    # 5. Hallucination threshold
    HALLUCINATION_IS_HARD_LIMIT: bool = True
    
    # 6. Every artifact has schema
    EVERY_ARTIFACT_HAS_SCHEMA: bool = True
    
    # 7. Every decision is logged
    EVERY_DECISION_IS_LOGGED: bool = True
    
    # 8. Every component is JSON-serializable
    SERIALIZATION_REQUIRED: bool = True
    
    # 9. Sandbox for code execution
    CODE_EXECUTION_SANDBOXED: bool = True
    
    # 10. Rollback on failure
    ROLLBACK_ON_CRITICAL_FAILURE: bool = True
    
    # 11. Audit trail is immutable
    AUDIT_TRAIL_IMMUTABLE: bool = True


# Singleton instance — frozen, cannot be modified
INVARIANTS = PreservationInvariants()
