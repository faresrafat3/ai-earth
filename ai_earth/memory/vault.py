"""
🧠 MemoryVault — Persistent cross-session memory that survives sandbox resets

Source:
    - Mem0 (arXiv:2504.19413) — layered memory concept
    - AI Earth original — file-backed, git-committable design

Stolen From:
    - Mem0: namespace + tagged-entry recall pattern

What Was Missed:
    - Vector embeddings (not needed — substring search is enough for
      learnings/discoveries; zero heavy deps, zero network)

GENESIS/AI Earth Adaptation:
    - Storage is plain JSON inside the repo (data/vault/<ns>.json) so
      memories survive TOTAL environment resets via git push.
    - Atomic writes (tmp + os.replace) — a killed process can never
      corrupt the vault.
    - Bounded: max entries per namespace (default 500, newest win) so
      the repo never grows unbounded.

Usage:
    from ai_earth.memory.vault import MemoryVault
    vault = MemoryVault()                        # default: data/vault/
    vault.remember("learnings", "k1", {"a": 1}, tags=["research"])
    vault.recall("learnings", tag="research")
    vault.search("learnings", "resear")
    vault.stats()

Integration:
    - يُستدعى من: SelfEvolveCore (يحفظ learnings تلقائياً)،
      ResearchDiscovery (يحفظ discoveries)، api.py (/vault endpoints)
    - يستدعي: لا شيء خارجي — stdlib فقط
    - يُنتج: data/vault/*.json

Tests:
    tests/test_memory_vault.py

Decision:
    DECISION-VAULT-1: JSON-in-repo بدل SQLite/vector-DB — لأن الهدف الأول
    هو النجاة من تصفير البيئة، و git هو أضمن وسيلة نقل موجودة.

Last Updated: 2026-06-10
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

__all__ = ["MemoryVault", "get_default_vault"]

_DEFAULT_MAX_ENTRIES = 500
_VALID_NS_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789_-")


def _repo_root() -> Path:
    """ai_earth/memory/vault.py → parents[2] == repo root."""
    return Path(__file__).resolve().parents[2]


class MemoryVault:
    """File-backed persistent memory. Thread-safe, atomic, bounded."""

    def __init__(self, root: Optional[str] = None, max_entries: int = _DEFAULT_MAX_ENTRIES):
        self._root = Path(root) if root else _repo_root() / "data" / "vault"
        self._root.mkdir(parents=True, exist_ok=True)
        self._max_entries = max(1, int(max_entries))
        self._lock = threading.Lock()
        self._seq = 0

    # ─── internal io ─────────────────────────────────────

    def _ns_path(self, namespace: str) -> Path:
        ns = namespace.strip().lower()
        if not ns or any(c not in _VALID_NS_CHARS for c in ns):
            raise ValueError(
                f"Invalid namespace {namespace!r} — use [a-z0-9_-] only"
            )
        return self._root / f"{ns}.json"

    def _load(self, namespace: str) -> Dict[str, Any]:
        path = self._ns_path(namespace)
        if not path.exists():
            return {"namespace": namespace, "updated": 0.0, "entries": []}
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or "entries" not in data:
                return {"namespace": namespace, "updated": 0.0, "entries": []}
            return data
        except (json.JSONDecodeError, OSError):
            # Corrupt file → keep a .bak once, start fresh (never crash)
            bak = path.with_suffix(".json.bak")
            if not bak.exists():
                try:
                    path.rename(bak)
                except OSError:
                    pass
            return {"namespace": namespace, "updated": 0.0, "entries": []}

    def _save(self, namespace: str, data: Dict[str, Any]) -> None:
        """Atomic write: tmp file + os.replace — kill-safe."""
        path = self._ns_path(namespace)
        data["updated"] = time.time()
        # Bound entries (newest win)
        if len(data["entries"]) > self._max_entries:
            data["entries"] = data["entries"][-self._max_entries:]
        tmp = path.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1, default=str)
        os.replace(tmp, path)

    # ─── public api ──────────────────────────────────────

    def remember(
        self,
        namespace: str,
        key: str,
        value: Any,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Store an entry. Same key = new version appended (history kept)."""
        with self._lock:
            self._seq += 1
            entry = {
                "id": f"{int(time.time() * 1000)}-{self._seq}",
                "key": str(key),
                "value": value,
                "tags": [str(t) for t in (tags or [])],
                "ts": time.time(),
            }
            data = self._load(namespace)
            data["entries"].append(entry)
            self._save(namespace, data)
            return entry

    def recall(
        self,
        namespace: str,
        key: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Retrieve entries (newest last). Filter by key and/or tag."""
        with self._lock:
            entries = self._load(namespace)["entries"]
        if key is not None:
            entries = [e for e in entries if e.get("key") == key]
        if tag is not None:
            entries = [e for e in entries if tag in e.get("tags", [])]
        return entries[-max(1, int(limit)):]

    def latest(self, namespace: str, n: int = 1) -> List[Dict[str, Any]]:
        """Get the n newest entries."""
        return self.recall(namespace, limit=n)

    def search(self, namespace: str, text: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Case-insensitive substring search across key/value/tags."""
        needle = str(text).lower()
        with self._lock:
            entries = self._load(namespace)["entries"]
        hits = []
        for e in entries:
            hay = (e.get("key", "") + " " + json.dumps(e.get("value"), default=str, ensure_ascii=False)
                   + " " + " ".join(e.get("tags", []))).lower()
            if needle in hay:
                hits.append(e)
        return hits[-max(1, int(limit)):]

    def forget(self, namespace: str, key: str) -> int:
        """Delete all versions of a key. Returns how many were removed."""
        with self._lock:
            data = self._load(namespace)
            before = len(data["entries"])
            data["entries"] = [e for e in data["entries"] if e.get("key") != key]
            removed = before - len(data["entries"])
            if removed:
                self._save(namespace, data)
            return removed

    def clear(self, namespace: str) -> int:
        """Wipe a namespace. Returns how many entries were removed."""
        with self._lock:
            data = self._load(namespace)
            removed = len(data["entries"])
            data["entries"] = []
            self._save(namespace, data)
            return removed

    def namespaces(self) -> List[str]:
        """List all namespaces present on disk (json files, ignore bak/tmp)."""
        return sorted(
            p.stem for p in self._root.glob("*.json")
            if not p.name.endswith((".tmp", ".bak"))
        )

    def stats(self) -> Dict[str, Any]:
        """Vault-wide statistics."""
        out: Dict[str, Any] = {"root": str(self._root), "namespaces": {}, "total_entries": 0}
        for ns in self.namespaces():
            try:
                n = len(self._load(ns)["entries"])
            except ValueError:
                continue  # non-conforming filename (e.g. legacy jsonl siblings)
            out["namespaces"][ns] = n
            out["total_entries"] += n
        return out

    def export_markdown(self, namespace: str, limit: int = 30) -> str:
        """Human-readable dump of a namespace (for reports/UI)."""
        lines = [f"# 🧠 Vault — {namespace}", ""]
        for e in self.recall(namespace, limit=limit):
            ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(e["ts"]))
            tags = (" `" + "` `".join(e["tags"]) + "`") if e.get("tags") else ""
            val = json.dumps(e["value"], ensure_ascii=False, default=str)
            if len(val) > 300:
                val = val[:300] + "…"
            lines.append(f"- **{e['key']}** ({ts}){tags}: {val}")
        return "\n".join(lines)


# ─── module-level default vault (singleton) ──────────────

_default_vault: Optional[MemoryVault] = None
_default_lock = threading.Lock()


def get_default_vault() -> MemoryVault:
    """Shared vault at data/vault/ — the one that survives resets."""
    global _default_vault
    with _default_lock:
        if _default_vault is None:
            _default_vault = MemoryVault()
        return _default_vault
