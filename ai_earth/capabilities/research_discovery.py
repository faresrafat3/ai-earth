"""
🔭 ResearchDiscovery — Live intelligence aggregation from the research web

Source:
    - AI Earth original (the platform's core mission: aggregate ALL
      AI research into composable intelligence)
    - Serper.dev (web search) + direct crawl + LLM summarization

Stolen From:
    - Nothing verbatim — this is glue built on our own llm_pool

What Was Missed:
    - Full PDF parsing (arXiv abstract pages are enough for discovery;
      deep extraction happens later in the LEGO pipeline)

GENESIS/AI Earth Adaptation:
    - NO fake/simulated content anywhere: crawl failure → honest "",
      LLM off → summaries explicitly labeled "[structural]"
    - Budget-guarded: max_llm_calls per aggregation run, never exceeded
    - Discoveries persist to MemoryVault ("discoveries" namespace) —
      the platform's research map survives environment resets

Usage:
    from ai_earth.capabilities.research_discovery import ResearchDiscovery
    rd = ResearchDiscovery()                       # live mode
    intel = rd.aggregate_intelligence("self-evolving agents", papers=3)
    rd.recent_discoveries(5)

    # offline/structural (zero network, zero LLM):
    rd = ResearchDiscovery(llm=False, search_fn=my_fake, crawl_fn=my_fake)

Integration:
    - يُستدعى من: api.py (/research endpoints)، orchestrator، UI
    - يستدعي: llm_pool.web_search / crawl_url، ModelRouter.chat، MemoryVault
    - يُنتج: data/vault/discoveries.json

Tests:
    tests/test_research_discovery.py

Decision:
    DECISION-RD-2: search/crawl injectable كـ functions — عشان الاختبارات
    الهيكلية تشتغل من غير network نهائياً (مش mock للذكاء، بس عزل للـ IO).

Last Updated: 2026-06-10
"""

from __future__ import annotations

import logging
import re
import time
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("ai_earth.research_discovery")

__all__ = ["ResearchDiscovery"]

_TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_HTML_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t]+")


def _strip_html(html: str) -> str:
    """Very light HTML→text (stdlib only): drop scripts/styles/tags."""
    if not html:
        return ""
    text = _TAG_RE.sub(" ", html)
    text = _HTML_RE.sub(" ", text)
    text = _WS_RE.sub(" ", text)
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


class ResearchDiscovery:
    """
    Live research aggregation: search → crawl → summarize → vault.

    llm=True  → real LLM summaries (budgeted, cheap model)
    llm=False → structural mode: zero LLM calls, snippet-only records
                clearly labeled "[structural]" (honest, never fake)
    """

    def __init__(
        self,
        router=None,
        vault=None,
        search_fn: Optional[Callable[[str, int], List[Dict]]] = None,
        crawl_fn: Optional[Callable[[str], str]] = None,
        llm: bool = True,
        llm_model: str = "gpt-4o-mini",
        max_llm_calls: int = 4,
        llm_max_tokens: int = 350,
        persist: bool = True,
    ):
        self._router = router
        self._vault = vault
        # When no vault is injected, auto-attach a file-backed MemoryVault
        # (data/vault/) so discoveries survive resets. Set persist=False for
        # ephemeral/offline runs that must not touch the real vault.
        self._persist_enabled = persist
        self._search_fn = search_fn
        self._crawl_fn = crawl_fn
        self._llm_enabled = llm
        self._llm_model = llm_model
        self._max_llm_calls = max(0, int(max_llm_calls))
        self._llm_max_tokens = llm_max_tokens
        self._llm_calls_made = 0
        self._llm_cost_usd = 0.0

    # ─── lazy deps ───────────────────────────────────────

    @property
    def router(self):
        if self._router is None:
            from ai_earth.model_router import ModelRouter
            self._router = ModelRouter()
        return self._router

    @property
    def vault(self):
        """Lazy MemoryVault — discoveries persist to data/vault/ by default
        so the platform's research map survives environment resets."""
        if self._vault is None and self._persist_enabled:
            try:
                from ai_earth.memory.vault import MemoryVault
                self._vault = MemoryVault()
            except Exception as e:  # persistence must never break discovery
                logger.warning(f"MemoryVault unavailable (non-fatal): {e}")
                self._vault = None
        return self._vault

    def _search(self, query: str, count: int) -> List[Dict]:
        if self._search_fn is not None:
            return self._search_fn(query, count)
        from ai_earth.llm_pool import web_search
        return web_search(query, num_results=count)

    def _crawl(self, url: str) -> str:
        if self._crawl_fn is not None:
            return self._crawl_fn(url)
        from ai_earth.llm_pool import crawl_url
        return crawl_url(url)

    # ─── discovery ───────────────────────────────────────

    def discover_papers(self, topic: str, count: int = 5) -> List[Dict[str, Any]]:
        """Search the research web for papers on a topic (no LLM)."""
        query = (
            f"latest AI research papers on {topic} "
            f"site:arxiv.org OR site:openreview.net"
        )
        results = self._search(query, count) or []
        papers = []
        for res in results[:count]:
            papers.append({
                "title": res.get("title", ""),
                "url": res.get("link", ""),
                "snippet": res.get("snippet", ""),
                "source": "web_search",
                "discovered_at": time.time(),
            })
        return papers

    # ─── summarization (budgeted LLM) ────────────────────

    def _budget_left(self) -> bool:
        return self._llm_calls_made < self._max_llm_calls

    def summarize_paper(self, url: str, title: str = "") -> Dict[str, Any]:
        """
        Crawl a paper page and summarize it.

        Returns {"summary": str, "mode": "llm"|"structural"|"budget_exhausted"
                 |"crawl_failed", "chars_crawled": int}
        """
        content = _strip_html(self._crawl(url))
        if len(content) < 100:
            return {
                "summary": "[crawl failed — no content retrieved]",
                "mode": "crawl_failed",
                "chars_crawled": len(content),
            }

        if not self._llm_enabled:
            return {
                "summary": f"[structural] first 400 chars: {content[:400]}",
                "mode": "structural",
                "chars_crawled": len(content),
            }

        if not self._budget_left():
            return {
                "summary": f"[budget exhausted at {self._max_llm_calls} calls] "
                           f"snippet: {content[:200]}",
                "mode": "budget_exhausted",
                "chars_crawled": len(content),
            }

        self._llm_calls_made += 1
        prompt = (
            f"Summarize this AI research paper page in 5 bullet points: "
            f"core contribution, method, results, why it matters for a "
            f"self-evolving intelligence platform, and whether it has "
            f"open-source code.\n\nTitle: {title}\n\nContent:\n{content[:8000]}"
        )
        resp = self.router.chat(
            model=self._llm_model,
            prompt=prompt,
            max_tokens=self._llm_max_tokens,
            temperature=0.3,
        )
        usage = resp.usage or {}
        self._llm_cost_usd += (
            usage.get("prompt_tokens", 0) * 0.00015
            + usage.get("completion_tokens", 0) * 0.0006
        ) / 1000
        return {
            "summary": resp.content,
            "mode": "llm",
            "chars_crawled": len(content),
        }

    # ─── full pipeline ───────────────────────────────────

    def aggregate_intelligence(
        self,
        topic: str,
        papers: int = 3,
        summarize: bool = True,
    ) -> Dict[str, Any]:
        """
        End-to-end: discover → (crawl+summarize) → persist to vault.
        """
        t0 = time.time()
        found = self.discover_papers(topic, count=papers)
        pieces: List[Dict[str, Any]] = []

        for paper in found:
            record = dict(paper)
            if summarize and paper.get("url"):
                s = self.summarize_paper(paper["url"], title=paper["title"])
                record.update(s)
            pieces.append(record)
            self._persist(topic, record)

        return {
            "topic": topic,
            "intelligence_pieces": pieces,
            "total_papers": len(pieces),
            "llm_calls": self._llm_calls_made,
            "llm_cost_usd": round(self._llm_cost_usd, 6),
            "elapsed_s": round(time.time() - t0, 2),
        }

    # ─── vault persistence ───────────────────────────────

    def _persist(self, topic: str, record: Dict[str, Any]) -> None:
        vault = self.vault
        if vault is None:
            return
        try:
            slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:40] or "general"
            vault.remember(
                "discoveries",
                record.get("url") or record.get("title") or "unknown",
                record,
                tags=[slug, "paper", record.get("mode", "found")],
            )
        except Exception as e:  # persistence must never break discovery
            logger.warning(f"Vault persist failed (non-fatal): {e}")

    def recent_discoveries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Read back the newest discoveries from the vault."""
        vault = self.vault
        if vault is None:
            return []
        return vault.recall("discoveries", limit=limit)

    # ─── stats ───────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        return {
            "llm_enabled": self._llm_enabled,
            "llm_model": self._llm_model,
            "llm_calls_made": self._llm_calls_made,
            "max_llm_calls": self._max_llm_calls,
            "llm_cost_usd": round(self._llm_cost_usd, 6),
            "vault_attached": self._vault is not None or self._persist_enabled,
            "persist_enabled": self._persist_enabled,
        }
