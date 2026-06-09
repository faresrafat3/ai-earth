"""
LEGACY_COMPAT — Backward Compatibility Layer

Ensures all GENESIS imports continue to work during migration.
This layer will be removed in Phase 7 (Final Integration) after
all consumers are updated to the new import paths.

Golden Rule: backward compatibility is sacred.

Usage (old imports still work):
    from genesis.tools.web_search import web_search          ✅
    from genesis.goal_specification import run_goal_specification  ✅

New imports:
    from ai_earth.capabilities.tool_hub.tools.web_search import web_search
    from ai_earth.capabilities.concept_engine.intent import run_goal_specification

Migration Strategy:
    Phase 1-6: Both old and new paths work (via this layer)
    Phase 7: Evaluate removal (if all consumers updated)
"""

# NOTE: These imports will be wired during Phase 1 implementation
# when actual GENESIS code is migrated into ai_earth/

# from ai_earth.capabilities.tool_hub.tools.web_search import (
#     web_search, SearchResult, EvidenceLog, EvidenceClaim
# )
# from ai_earth.capabilities.concept_engine.intent import run_goal_specification
# from ai_earth.workflow.critic.open_evaluator import run_open_task_evaluation
