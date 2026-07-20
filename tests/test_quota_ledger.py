"""
Tests for QuotaLedger — persistent daily rate-limit protection
==============================================================
All structural (no LLM, no network). Every test uses tmp_path
so the real data/quota_ledger.json is never polluted.
"""

import json
import os
import sys
import threading
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))

from ai_earth.core.quota_ledger import QuotaLedger, get_ledger, reset_ledger, _utc_day


@pytest.fixture()
def ledger(tmp_path):
    return QuotaLedger(path=str(tmp_path / "ledger.json"))


# ═════════════════════════════════════════════════════════
# 1. Basics
# ═════════════════════════════════════════════════════════

class TestLedgerBasics:
    def test_fresh_ledger_allows_all(self, ledger):
        for prov in ["github", "openrouter", "google", "serper"]:
            assert ledger.allowed(prov) is True

    def test_default_caps(self, ledger):
        assert ledger.cap("github") == 120
        assert ledger.cap("openrouter") == 500
        assert ledger.cap("google") == 150
        assert ledger.cap("serper") == 60

    def test_unknown_provider_gets_default_cap(self, ledger):
        assert ledger.cap("some-new-provider") == 100

    def test_record_increments_usage(self, ledger):
        ledger.record("github", tokens=50, cost_usd=0.001)
        assert ledger.used_today("github") == 1
        assert ledger.remaining("github") == 119

    def test_record_failure_still_counts(self, ledger):
        ledger.record("github", success=False)
        assert ledger.used_today("github") == 1
        s = ledger.status()
        assert s["providers"]["github"]["fail"] == 1
        assert s["providers"]["github"]["ok"] == 0

    def test_file_created_on_record(self, ledger):
        ledger.record("github")
        assert os.path.exists(ledger.path)
        data = json.load(open(ledger.path))
        assert "days" in data and "lifetime" in data


# ═════════════════════════════════════════════════════════
# 2. Cap Enforcement (the anti-rate-limit core)
# ═════════════════════════════════════════════════════════

class TestCapEnforcement:
    def test_blocked_at_cap(self, ledger):
        for _ in range(60):
            ledger.record("serper")
        assert ledger.allowed("serper") is False
        assert ledger.remaining("serper") == 0

    def test_one_below_cap_still_allowed(self, ledger):
        for _ in range(59):
            ledger.record("serper")
        assert ledger.allowed("serper") is True
        assert ledger.remaining("serper") == 1

    def test_exhausted_flag_in_status(self, ledger):
        for _ in range(60):
            ledger.record("serper")
        s = ledger.status()
        assert s["providers"]["serper"]["exhausted"] is True
        assert s["providers"]["github"]["exhausted"] is False

    def test_env_cap_override(self, ledger, monkeypatch):
        monkeypatch.setenv("AI_EARTH_DAILY_CAP_GITHUB", "3")
        assert ledger.cap("github") == 3
        for _ in range(3):
            ledger.record("github")
        assert ledger.allowed("github") is False

    def test_env_cap_bad_value_falls_back(self, ledger, monkeypatch):
        monkeypatch.setenv("AI_EARTH_DAILY_CAP_GITHUB", "not-a-number")
        assert ledger.cap("github") == 120


# ═════════════════════════════════════════════════════════
# 3. Persistence & Resilience
# ═════════════════════════════════════════════════════════

class TestPersistence:
    def test_survives_reload(self, tmp_path):
        p = str(tmp_path / "led.json")
        l1 = QuotaLedger(path=p)
        l1.record("github", tokens=10)
        # brand-new instance, same file (simulates a new session)
        l2 = QuotaLedger(path=p)
        assert l2.used_today("github") == 1

    def test_lifetime_totals_accumulate(self, ledger):
        ledger.record("github", tokens=10, cost_usd=0.001)
        ledger.record("google", tokens=20, cost_usd=0.002)
        s = ledger.status()
        assert s["lifetime"]["calls"] == 2
        assert s["lifetime"]["tokens"] == 30
        assert abs(s["lifetime"]["cost_usd"] - 0.003) < 1e-9

    def test_corrupt_file_recovers(self, tmp_path):
        p = str(tmp_path / "led.json")
        with open(p, "w") as f:
            f.write("{{{ not json")
        led = QuotaLedger(path=p)
        assert led.allowed("github") is True
        led.record("github")
        assert led.used_today("github") == 1
        # corrupt copy preserved for forensics
        assert os.path.exists(p + ".corrupt")

    def test_atomic_write_no_tmp_leftover(self, ledger):
        ledger.record("github")
        assert not os.path.exists(ledger.path + ".tmp")

    def test_prunes_old_days(self, ledger):
        # inject 40 fake old days directly
        data = {"days": {}, "lifetime": {"calls": 0, "tokens": 0, "cost_usd": 0.0}}
        for i in range(40):
            data["days"][f"2020-01-{i+1:02d}"] = {"providers": {}, "total_calls": 0}
        ledger._write(data)
        ledger.record("github")  # triggers prune on write
        stored = json.load(open(ledger.path))
        assert len(stored["days"]) <= 31  # 30 kept + today

    def test_thread_safety(self, ledger):
        def worker():
            for _ in range(10):
                ledger.record("github")
        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert ledger.used_today("github") == 50


# ═════════════════════════════════════════════════════════
# 4. Status & History
# ═════════════════════════════════════════════════════════

class TestStatusHistory:
    def test_status_shape(self, ledger):
        s = ledger.status()
        assert set(["date", "providers", "today_total_calls", "lifetime"]).issubset(s)
        assert s["date"] == _utc_day()

    def test_history_limits_days(self, ledger):
        ledger.record("github")
        h = ledger.history(days=7)
        assert len(h) <= 7
        assert _utc_day() in h

    def test_singleton(self):
        reset_ledger()
        a = get_ledger()
        b = get_ledger()
        assert a is b
        reset_ledger()


# ═════════════════════════════════════════════════════════
# 5. llm_pool Integration (no network — fail-open contract)
# ═════════════════════════════════════════════════════════

class TestPoolIntegration:
    def test_ledger_helpers_exist(self):
        from ai_earth.llm_pool import _ledger_ok, _ledger_rec
        assert callable(_ledger_ok) and callable(_ledger_rec)

    def test_ledger_ok_fail_open(self, monkeypatch):
        """If the ledger itself explodes, calls must NOT be blocked."""
        import ai_earth.llm_pool as lp

        def boom():
            raise RuntimeError("ledger exploded")

        monkeypatch.setattr("ai_earth.core.quota_ledger.get_ledger", boom)
        assert lp._ledger_ok("github") is True   # fail-open
        lp._ledger_rec("github")                  # must not raise

    def test_exhausted_provider_skipped_preflight(self, tmp_path, monkeypatch):
        """call_llm must skip an exhausted provider BEFORE any HTTP."""
        import ai_earth.llm_pool as lp
        import ai_earth.core.quota_ledger as ql

        led = QuotaLedger(path=str(tmp_path / "led.json"))
        for _ in range(led.cap("github")):
            led.record("github")
        monkeypatch.setattr(ql, "_ledger", led, raising=False)

        assert lp._ledger_ok("github") is False
        assert lp._ledger_ok("google") is True

    def test_web_search_blocked_when_serper_exhausted(self, tmp_path, monkeypatch):
        import ai_earth.llm_pool as lp
        import ai_earth.core.quota_ledger as ql

        led = QuotaLedger(path=str(tmp_path / "led.json"))
        for _ in range(led.cap("serper")):
            led.record("serper")
        monkeypatch.setattr(ql, "_ledger", led, raising=False)

        called = {"n": 0}

        def fake_post(*a, **k):
            called["n"] += 1
            raise AssertionError("HTTP must not happen when quota exhausted")

        monkeypatch.setattr(lp.requests, "post", fake_post)
        assert lp.web_search("anything") == []
        assert called["n"] == 0  # zero HTTP attempts


# ═════════════════════════════════════════════════════════
# 6. API Endpoints (TestClient — no LLM)
# ═════════════════════════════════════════════════════════

class TestQuotaAPI:
    @pytest.fixture()
    def client(self):
        from fastapi.testclient import TestClient
        from ai_earth.api import app
        return TestClient(app)

    def test_get_quota(self, client):
        r = client.get("/quota")
        assert r.status_code == 200
        body = r.json()
        assert "providers" in body and "date" in body
        assert "github" in body["providers"]

    def test_get_quota_history(self, client):
        r = client.get("/quota/history?days=3")
        assert r.status_code == 200
        assert "days" in r.json()

    def test_get_vault_stats(self, client):
        r = client.get("/vault")
        assert r.status_code == 200
        assert "namespaces" in r.json() or "total_entries" in r.json() or isinstance(r.json(), dict)

    def test_get_vault_namespace_404(self, client):
        r = client.get("/vault/definitely-not-a-namespace-xyz")
        assert r.status_code == 404
