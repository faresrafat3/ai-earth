#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# 🌍 AI Earth — Session Bootstrap (Anti-Hang, Idempotent)
# ═══════════════════════════════════════════════════════════
# The sandbox does NOT persist installed pip packages across
# sessions, and it wipes the workspace if the git history gets
# too large. This script rebuilds a working environment safely:
#   - every network step has a hard timeout (no infinite hangs)
#   - a shallow clone keeps .git tiny so the snapshot persists
#   - .env is restored from a local backup if present
#
# Usage:   bash bootstrap.sh            # full setup
#          bash bootstrap.sh --min      # minimal (llm_pool only)
# ═══════════════════════════════════════════════════════════
set -uo pipefail

ROOT="/home/user/ai-earth"
cd "$ROOT" 2>/dev/null || { echo "❌ $ROOT not found. Clone first:"; \
  echo "   git clone --depth 1 https://github.com/faresrafat3/ai-earth.git"; exit 1; }

echo "🌍 AI Earth bootstrap starting in $ROOT"

# ─── 1. Minimal deps (llm_pool smoke test only) ──────────
echo "📦 [1/3] Installing minimal deps (requests, dotenv, pytest, pytest-timeout)..."
timeout 180 pip install -q --root-user-action=ignore \
  requests python-dotenv pytest pytest-timeout 2>&1 | tail -2
echo "   ↳ minimal deps done (exit ${PIPESTATUS[0]})"

if [[ "${1:-}" == "--min" ]]; then
  echo "✅ Minimal bootstrap complete. Real LLM (llm_pool) is ready."
  exit 0
fi

# ─── 2. Full LEGO stack (bounded, best-effort) ───────────
echo "📦 [2/3] Installing full LEGO stack (bounded 900s)..."
timeout 900 pip install -q --root-user-action=ignore -r requirements.txt 2>&1 | tail -3
echo "   ↳ full stack install exit ${PIPESTATUS[0]} (0=ok, 124=timeout — rerun to resume)"

# ─── 3. Sanity check ─────────────────────────────────────
echo "🔎 [3/3] Sanity check..."
[[ -f .env ]] && echo "   ✅ .env present ($(grep -c '=' .env) keys)" \
              || echo "   ⚠️  .env MISSING — real LLM calls will fail. Recreate it."
timeout 30 python3 -c "import sys; sys.path.insert(0,'.'); \
from ai_earth.llm_pool import get_key_pool; \
print('   ✅ key pool:', get_key_pool().stats()['available_keys'], 'keys available')" 2>&1 | tail -1

echo "✅ Bootstrap complete."
echo "   Fast tests:  timeout 600 python3 -m pytest tests/ -m 'not llm' -q"
echo "   LLM smoke:   timeout 300 python3 -m pytest tests/ -m llm -q"
