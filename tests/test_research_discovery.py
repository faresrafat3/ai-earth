"""
Tests for ResearchDiscovery — live intelligence aggregation
============================================================
Structural tests: injected fake search/crawl (zero network, zero LLM).
Live tests: marked @pytest.mark.llm (real Serper + real LLM, tiny budget).
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))

from ai_earth.capabilities.research_discovery import ResearchDiscovery, _strip_html
from ai_earth.memory.vault import MemoryVault


# ─── fakes (IO isolation for structural tests — not AI mock) ───

def fake_search(query, count):
    return [
        {"title": f"Paper {i}: Self-Evolving Agents", "link": f"https://arxiv.org/abs/2500.{i:05d}",
         "snippet": f"We propose method {i} for recursive self-improvement."}
        for i in range(count)
    ]


def fake_crawl(url):
    return ("<html><script>evil()</script><body>"
            + "Abstract: This paper introduces a framework for self-evolving "
              "AI agents with memory persistence and workflow optimization. " * 5
            + "</body></html>")


class CountingFakeRouter:
    """Counts chat calls — used ONLY to unit-test budget logic."""
    def __init__(self):
        self.calls = 0

    def chat(self, **kwargs):
        self.calls += 1

        class R:
            content = "• contribution • method • results • relevance • code: yes"
            usage = {"prompt_tokens": 100, "completion_tokens": 50}
        return R()


# ═════════════════════════════════════════════════════════
# 1. Discovery (structural)
# ═════════════════════════════════════════════════════════

class TestDiscoverPapers:
    def test_returns_structured_papers(self):
        rd = ResearchDiscovery(llm=False, search_fn=fake_search)
        papers = rd.discover_papers("self-evolving agents", count=3)
        assert len(papers) == 3
        for p in papers:
            assert p["title"] and p["url"].startswith("https://arxiv.org")
            assert p["source"] == "web_search"
            assert "discovered_at" in p

    def test_respects_count(self):
        rd = ResearchDiscovery(llm=False, search_fn=fake_search)
        assert len(rd.discover_papers("x", count=1)) == 1

    def test_empty_results_ok(self):
        rd = ResearchDiscovery(llm=False, search_fn=lambda q, c: [])
        assert rd.discover_papers("nothing") == []


# ═════════════════════════════════════════════════════════
# 2. Summarization modes (structural)
# ═════════════════════════════════════════════════════════

class TestSummarizeModes:
    def test_crawl_failed_is_honest(self):
        rd = ResearchDiscovery(llm=False, crawl_fn=lambda u: "")
        s = rd.summarize_paper("https://example.org/x")
        assert s["mode"] == "crawl_failed"
        assert "crawl failed" in s["summary"]
        # NEVER fake content on failure
        assert "Simulated" not in s["summary"]

    def test_structural_mode_zero_llm(self):
        router = CountingFakeRouter()
        rd = ResearchDiscovery(router=router, llm=False, crawl_fn=fake_crawl)
        s = rd.summarize_paper("https://arxiv.org/abs/2500.00001")
        assert s["mode"] == "structural"
        assert s["summary"].startswith("[structural]")
        assert router.calls == 0

    def test_llm_mode_calls_router(self):
        router = CountingFakeRouter()
        rd = ResearchDiscovery(router=router, llm=True, crawl_fn=fake_crawl)
        s = rd.summarize_paper("https://arxiv.org/abs/2500.00001")
        assert s["mode"] == "llm"
        assert router.calls == 1
        assert rd.stats()["llm_cost_usd"] > 0

    def test_budget_never_exceeded(self):
        router = CountingFakeRouter()
        rd = ResearchDiscovery(router=router, llm=True, crawl_fn=fake_crawl,
                               max_llm_calls=2)
        modes = [rd.summarize_paper(f"https://x.org/{i}")["mode"] for i in range(5)]
        assert router.calls == 2  # hard cap
        assert modes[:2] == ["llm", "llm"]
        assert all(m == "budget_exhausted" for m in modes[2:])

    def test_html_stripping(self):
        text = _strip_html("<html><script>bad()</script><b>Good</b> text</html>")
        assert "bad()" not in text and "<b>" not in text
        assert "Good" in text


# ═════════════════════════════════════════════════════════
# 3. Full pipeline + vault (structural)
# ═════════════════════════════════════════════════════════

class TestAggregateAndVault:
    def test_aggregate_structural(self, tmp_path):
        v = MemoryVault(root=str(tmp_path / "v"))
        rd = ResearchDiscovery(llm=False, vault=v,
                               search_fn=fake_search, crawl_fn=fake_crawl)
        intel = rd.aggregate_intelligence("workflow optimization", papers=3)
        assert intel["total_papers"] == 3
        assert intel["llm_calls"] == 0
        assert all("summary" in p for p in intel["intelligence_pieces"])

    def test_discoveries_persisted(self, tmp_path):
        v = MemoryVault(root=str(tmp_path / "v"))
        rd = ResearchDiscovery(llm=False, vault=v,
                               search_fn=fake_search, crawl_fn=fake_crawl)
        rd.aggregate_intelligence("memory systems", papers=2)
        stored = v.recall("discoveries")
        assert len(stored) == 2
        assert "memory-systems" in stored[0]["tags"]
        assert "paper" in stored[0]["tags"]

    def test_recent_discoveries_readback(self, tmp_path):
        v = MemoryVault(root=str(tmp_path / "v"))
        rd = ResearchDiscovery(llm=False, vault=v,
                               search_fn=fake_search, crawl_fn=fake_crawl)
        rd.aggregate_intelligence("agents", papers=2)
        recent = rd.recent_discoveries(1)
        assert len(recent) == 1

    def test_no_vault_ok(self):
        # persist=False → ephemeral run, never touches the real data/vault/
        rd = ResearchDiscovery(llm=False, persist=False,
                               search_fn=fake_search, crawl_fn=fake_crawl)
        intel = rd.aggregate_intelligence("agents", papers=1)
        assert intel["total_papers"] == 1
        assert rd.recent_discoveries() == []

    def test_persist_default_attaches_vault(self, tmp_path, monkeypatch):
        # Live default (no injected vault) auto-attaches a MemoryVault so
        # discoveries survive environment resets — the platform's mission.
        import ai_earth.memory.vault as vaultmod
        monkeypatch.setattr(vaultmod, "_repo_root", lambda: tmp_path)
        rd = ResearchDiscovery(llm=False, search_fn=fake_search, crawl_fn=fake_crawl)
        assert rd.stats()["persist_enabled"] is True
        rd.aggregate_intelligence("auto-persist", papers=1)
        assert len(rd.recent_discoveries()) == 1

    def test_survives_new_session(self, tmp_path):
        root = str(tmp_path / "v")
        rd1 = ResearchDiscovery(llm=False, vault=MemoryVault(root=root),
                                search_fn=fake_search, crawl_fn=fake_crawl)
        rd1.aggregate_intelligence("evolution", papers=1)
        # fresh objects — same disk (post-reset scenario)
        rd2 = ResearchDiscovery(llm=False, vault=MemoryVault(root=root))
        assert len(rd2.recent_discoveries()) == 1


# ═════════════════════════════════════════════════════════
# 4. Honesty guarantees (no fake content anywhere)
# ═════════════════════════════════════════════════════════

class TestHonesty:
    def test_crawl_url_returns_empty_on_failure(self, monkeypatch):
        import ai_earth.llm_pool as lp

        def boom(*a, **k):
            raise RuntimeError("network down")
        monkeypatch.setattr(lp.requests, "get", boom)
        out = lp.crawl_url("https://nope.invalid/x")
        assert out == ""  # honest empty — no "Simulated content"

    def test_router_crawl_method_exists(self):
        from ai_earth.model_router import ModelRouter
        assert callable(getattr(ModelRouter(), "crawl", None))

    def test_stats_shape(self):
        rd = ResearchDiscovery(llm=False)
        s = rd.stats()
        for k in ("llm_enabled", "llm_calls_made", "max_llm_calls",
                  "llm_cost_usd", "vault_attached"):
            assert k in s


# ═════════════════════════════════════════════════════════
# 5. Live tests — real Serper + real LLM (tiny budget)
# ═════════════════════════════════════════════════════════

@pytest.mark.llm
class TestLiveDiscovery:
    def test_live_serper_search(self):
        rd = ResearchDiscovery(llm=False)  # network yes, LLM no
        papers = rd.discover_papers("self-evolving LLM agents", count=2)
        assert len(papers) >= 1
        assert papers[0]["url"].startswith("http")

    def test_live_aggregate_one_paper(self, tmp_path):
        v = MemoryVault(root=str(tmp_path / "v"))
        rd = ResearchDiscovery(llm=True, vault=v, max_llm_calls=1)
        intel = rd.aggregate_intelligence("LLM agent memory", papers=1)
        assert intel["total_papers"] == 1
        piece = intel["intelligence_pieces"][0]
        assert piece["mode"] in ("llm", "crawl_failed")  # arxiv may block
        if piece["mode"] == "llm":
            assert len(piece["summary"]) > 50
            assert intel["llm_cost_usd"] < 0.01  # tiny budget respected
        assert len(v.recall("discoveries")) == 1
