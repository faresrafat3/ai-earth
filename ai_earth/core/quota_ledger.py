"""
📒 AI Earth — Persistent Quota Ledger
═══════════════════════════════════════════════════════════
Disk-backed daily quota tracking that SURVIVES sessions.

Why this exists:
  The sandbox loses process state between sessions, but the
  workspace (and git) persist. Rate limits are *daily* — so an
  in-memory counter is useless across restarts. This ledger
  writes every LLM/search attempt to data/quota_ledger.json and
  refuses calls for a provider whose daily cap is reached —
  BEFORE any HTTP request is made (fail-fast, zero hang).

Design rules:
  - stdlib ONLY (json, os, time, threading, tempfile) — this
    module must be importable by llm_pool with zero risk.
  - Atomic writes (tmp file + os.replace) — a crash can never
    corrupt the ledger.
  - Process-safe best-effort via fcntl lock when available.
  - Keeps only the last 30 days (bounded file size).

Daily caps (env-overridable):
  AI_EARTH_DAILY_CAP_GITHUB      default 120   (free tier ~150/day → headroom)
  AI_EARTH_DAILY_CAP_OPENROUTER  default 500
  AI_EARTH_DAILY_CAP_GOOGLE      default 150
  AI_EARTH_DAILY_CAP_SERPER      default 60    (2500 one-time credits → sip slowly)

Usage:
    from ai_earth.core.quota_ledger import get_ledger
    led = get_ledger()
    if led.allowed("github"):
        ...make the call...
        led.record("github", tokens=123, cost_usd=0.0, success=True)
    print(led.status())
"""

from __future__ import annotations

import json
import os
import threading
import time
from typing import Any, Dict, Optional

try:
    import fcntl  # POSIX only — best-effort cross-process lock
    _HAS_FCNTL = True
except ImportError:  # pragma: no cover
    _HAS_FCNTL = False

_KEEP_DAYS = 30

_DEFAULT_CAPS: Dict[str, int] = {
    "github": 120,
    "openrouter": 500,
    "google": 150,
    "serper": 60,
}


def _repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))       # ai_earth/core
    return os.path.dirname(os.path.dirname(here))            # repo root


def _utc_day(ts: Optional[float] = None) -> str:
    return time.strftime("%Y-%m-%d", time.gmtime(ts if ts is not None else time.time()))


def _env_cap(provider: str) -> int:
    name = f"AI_EARTH_DAILY_CAP_{provider.upper()}"
    raw = os.environ.get(name)
    if raw is None:
        # try .env at repo root (same convention as llm_pool)
        env_path = os.path.join(_repo_root(), ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith(name + "="):
                            raw = line.split("=", 1)[1].strip()
                            break
            except OSError:
                pass
    try:
        return int(raw) if raw else _DEFAULT_CAPS.get(provider, 100)
    except (ValueError, TypeError):
        return _DEFAULT_CAPS.get(provider, 100)


class QuotaLedger:
    """Persistent daily per-provider quota ledger (thread/process safe)."""

    def __init__(self, path: Optional[str] = None):
        self.path = path or os.path.join(_repo_root(), "data", "quota_ledger.json")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._lock = threading.Lock()

    # ─── low-level IO (atomic, locked) ─────────────────────

    def _read(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {"days": {}, "lifetime": {"calls": 0, "tokens": 0, "cost_usd": 0.0}}
        try:
            with open(self.path, "r") as f:
                if _HAS_FCNTL:
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    data = json.load(f)
                finally:
                    if _HAS_FCNTL:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            if not isinstance(data, dict):
                raise ValueError("ledger root must be a dict")
            data.setdefault("days", {})
            data.setdefault("lifetime", {"calls": 0, "tokens": 0, "cost_usd": 0.0})
            return data
        except (json.JSONDecodeError, ValueError, OSError):
            # Corrupt ledger → back it up and start clean (never crash callers)
            try:
                os.replace(self.path, self.path + ".corrupt")
            except OSError:
                pass
            return {"days": {}, "lifetime": {"calls": 0, "tokens": 0, "cost_usd": 0.0}}

    def _write(self, data: Dict[str, Any]) -> None:
        # prune old days (bounded file)
        days = data.get("days", {})
        if len(days) > _KEEP_DAYS:
            for day in sorted(days)[: len(days) - _KEEP_DAYS]:
                days.pop(day, None)
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            if _HAS_FCNTL:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(data, f, indent=1)
                f.flush()
                os.fsync(f.fileno())
            finally:
                if _HAS_FCNTL:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        os.replace(tmp, self.path)

    # ─── public API ────────────────────────────────────────

    def cap(self, provider: str) -> int:
        return _env_cap(provider)

    def used_today(self, provider: str) -> int:
        data = self._read()
        day = data["days"].get(_utc_day(), {})
        return int(day.get("providers", {}).get(provider, {}).get("calls", 0))

    def remaining(self, provider: str) -> int:
        return max(0, self.cap(provider) - self.used_today(provider))

    def allowed(self, provider: str) -> bool:
        """Fast pre-flight check. True = provider still has daily budget."""
        return self.remaining(provider) > 0

    def record(
        self,
        provider: str,
        tokens: int = 0,
        cost_usd: float = 0.0,
        success: bool = True,
        calls: int = 1,
    ) -> None:
        """Record an attempt (counts against the daily cap even on failure —
        the remote rate limiter counted it too)."""
        with self._lock:
            data = self._read()
            day_key = _utc_day()
            day = data["days"].setdefault(
                day_key, {"providers": {}, "total_calls": 0}
            )
            prov = day["providers"].setdefault(
                provider, {"calls": 0, "ok": 0, "fail": 0, "tokens": 0, "cost_usd": 0.0}
            )
            prov["calls"] += calls
            prov["ok" if success else "fail"] += calls
            prov["tokens"] += int(tokens)
            prov["cost_usd"] = round(prov["cost_usd"] + float(cost_usd), 8)
            day["total_calls"] += calls

            lt = data["lifetime"]
            lt["calls"] += calls
            lt["tokens"] += int(tokens)
            lt["cost_usd"] = round(lt["cost_usd"] + float(cost_usd), 8)

            self._write(data)

    def status(self) -> Dict[str, Any]:
        """Today's usage vs caps + lifetime totals."""
        data = self._read()
        today = data["days"].get(_utc_day(), {"providers": {}, "total_calls": 0})
        providers = {}
        for prov in sorted(set(list(_DEFAULT_CAPS) + list(today.get("providers", {})))):
            used = int(today.get("providers", {}).get(prov, {}).get("calls", 0))
            cap = self.cap(prov)
            providers[prov] = {
                "used": used,
                "cap": cap,
                "remaining": max(0, cap - used),
                "ok": today.get("providers", {}).get(prov, {}).get("ok", 0),
                "fail": today.get("providers", {}).get(prov, {}).get("fail", 0),
                "tokens": today.get("providers", {}).get(prov, {}).get("tokens", 0),
                "cost_usd": today.get("providers", {}).get(prov, {}).get("cost_usd", 0.0),
                "exhausted": used >= cap,
            }
        return {
            "date": _utc_day(),
            "providers": providers,
            "today_total_calls": today.get("total_calls", 0),
            "lifetime": data.get("lifetime", {}),
            "days_tracked": len(data.get("days", {})),
            "path": self.path,
        }

    def history(self, days: int = 7) -> Dict[str, Any]:
        """Last N days of usage."""
        data = self._read()
        keys = sorted(data.get("days", {}))[-days:]
        return {k: data["days"][k] for k in keys}


# ─── module-level singleton ───────────────────────────────

_ledger: Optional[QuotaLedger] = None
_singleton_lock = threading.Lock()


def get_ledger() -> QuotaLedger:
    global _ledger
    if _ledger is None:
        with _singleton_lock:
            if _ledger is None:
                _ledger = QuotaLedger()
    return _ledger


def reset_ledger() -> None:
    """Testing hook — forget the singleton (does NOT delete the file)."""
    global _ledger
    _ledger = None
