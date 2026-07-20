#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# 🛡️ AI Earth — Environment Bootstrap (Anti-Reset Recovery)
# ═══════════════════════════════════════════════════════════
# One bounded command restores the whole environment after a
# sandbox reset. EVERY step has a hard timeout — nothing here
# can hang. Total worst-case runtime: ~50 minutes, typical ~4.
#
# Usage:
#   bash scripts/bootstrap.sh            # install + fast tests
#   bash scripts/bootstrap.sh --no-test  # install only
#
# Requires: .env in repo root (never committed — recreate it
# from your key list if the sandbox was wiped).
# ═══════════════════════════════════════════════════════════
set -uo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
echo "🌍 AI Earth bootstrap @ $ROOT"

# ─── 1. Sanity: .env must exist ────────────────────────
if [[ ! -f .env ]]; then
    echo "❌ .env missing! Recreate it from .env.example + your keys."
    echo "   The platform will boot but real LLM calls will fail."
else
    echo "✅ .env present"
fi

# ─── 2. Install dependencies (bounded 1700s) ───────────
echo "📦 Installing dependencies (max 28 min)..."
if timeout -k 10 1700 pip3 install -q --no-input --disable-pip-version-check \
        -r requirements.txt requests; then
    echo "✅ dependencies installed"
else
    echo "❌ pip install failed or timed out"; exit 1
fi

# ─── 3. Verify platform boots + keys load (bounded 60s) ─
echo "🔑 Verifying platform boot + key pool..."
if timeout -k 5 60 python3 - <<'PY'
import sys
sys.path.insert(0, 'ai_earth/lego')
sys.path.insert(0, 'ai_earth/lego/stubs')
sys.path.insert(0, '.')
from ai_earth.llm_pool import get_key_pool
import ai_earth
s = get_key_pool().stats()
print(f"   version={ai_earth.__version__} keys={s['total_keys']} available={s['available_keys']}")
PY
then
    echo "✅ platform boots"
else
    echo "❌ platform failed to boot"; exit 1
fi

# ─── 4. Fast structural suite (bounded 950s, no LLM) ───
if [[ "${1:-}" != "--no-test" ]]; then
    echo "🧪 Running fast suite (no LLM calls, max 16 min)..."
    if timeout -k 10 950 python3 -m pytest -m "not llm" -q --tb=line 2>&1 | tail -3; then
        echo "✅ fast suite done"
    else
        echo "⚠️ fast suite had failures — inspect before continuing"
    fi
fi

echo "🎉 Bootstrap complete. LLM smoke check (optional, costs ~\$0.0001):"
echo "   timeout 240 python3 -m pytest tests/test_model_router.py::TestRealLLMProvider::test_real_chat_call -q"
