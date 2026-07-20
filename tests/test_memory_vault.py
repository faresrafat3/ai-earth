"""
Tests for MemoryVault — persistent cross-session memory
========================================================
All structural (no LLM, no network). Every test uses tmp_path
so the real data/vault/ is never polluted.
"""

import json
import os
import sys
import threading

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))

from ai_earth.memory.vault import MemoryVault, get_default_vault


@pytest.fixture()
def vault(tmp_path):
    return MemoryVault(root=str(tmp_path / "vault"))


# ═════════════════════════════════════════════════════════
# 1. Basics — remember / recall
# ═════════════════════════════════════════════════════════

class TestVaultBasics:
    def test_remember_returns_entry(self, vault):
        e = vault.remember("learnings", "k1", {"score": 0.9})
        assert e["key"] == "k1"
        assert e["value"] == {"score": 0.9}
        assert "id" in e and "ts" in e

    def test_recall_roundtrip(self, vault):
        vault.remember("learnings", "k1", {"a": 1})
        got = vault.recall("learnings")
        assert len(got) == 1
        assert got[0]["value"] == {"a": 1}

    def test_recall_by_key(self, vault):
        vault.remember("ns", "k1", 1)
        vault.remember("ns", "k2", 2)
        got = vault.recall("ns", key="k2")
        assert len(got) == 1 and got[0]["value"] == 2

    def test_recall_by_tag(self, vault):
        vault.remember("ns", "k1", 1, tags=["research"])
        vault.remember("ns", "k2", 2, tags=["exec"])
        got = vault.recall("ns", tag="research")
        assert len(got) == 1 and got[0]["key"] == "k1"

    def test_recall_limit(self, vault):
        for i in range(10):
            vault.remember("ns", f"k{i}", i)
        got = vault.recall("ns", limit=3)
        assert len(got) == 3
        assert got[-1]["value"] == 9  # newest last

    def test_same_key_keeps_history(self, vault):
        vault.remember("ns", "k", "v1")
        vault.remember("ns", "k", "v2")
        got = vault.recall("ns", key="k")
        assert [e["value"] for e in got] == ["v1", "v2"]

    def test_latest(self, vault):
        for i in range(5):
            vault.remember("ns", f"k{i}", i)
        got = vault.latest("ns", n=2)
        assert [e["value"] for e in got] == [3, 4]

    def test_empty_namespace_recall(self, vault):
        assert vault.recall("nothing_here") == []


# ═════════════════════════════════════════════════════════
# 2. Search / forget / clear
# ═════════════════════════════════════════════════════════

class TestVaultOps:
    def test_search_in_value(self, vault):
        vault.remember("ns", "k1", {"note": "self-evolving platform"})
        vault.remember("ns", "k2", {"note": "something else"})
        got = vault.search("ns", "evolving")
        assert len(got) == 1 and got[0]["key"] == "k1"

    def test_search_case_insensitive(self, vault):
        vault.remember("ns", "K", "Hello World")
        assert len(vault.search("ns", "hello")) == 1

    def test_search_in_tags(self, vault):
        vault.remember("ns", "k1", 0, tags=["arxiv"])
        assert len(vault.search("ns", "arxiv")) == 1

    def test_search_arabic(self, vault):
        vault.remember("ns", "k1", {"ملاحظة": "منصة الذكاء"})
        assert len(vault.search("ns", "الذكاء")) == 1

    def test_forget(self, vault):
        vault.remember("ns", "k", "v1")
        vault.remember("ns", "k", "v2")
        vault.remember("ns", "other", "x")
        removed = vault.forget("ns", "k")
        assert removed == 2
        assert vault.recall("ns", key="k") == []
        assert len(vault.recall("ns")) == 1

    def test_forget_missing_key(self, vault):
        assert vault.forget("ns", "ghost") == 0

    def test_clear(self, vault):
        for i in range(4):
            vault.remember("ns", f"k{i}", i)
        assert vault.clear("ns") == 4
        assert vault.recall("ns") == []


# ═════════════════════════════════════════════════════════
# 3. Persistence & durability
# ═════════════════════════════════════════════════════════

class TestVaultDurability:
    def test_survives_new_instance(self, tmp_path):
        root = str(tmp_path / "v")
        v1 = MemoryVault(root=root)
        v1.remember("learnings", "lesson", {"insight": "push early"})
        # simulate a fresh session — brand-new object, same disk
        v2 = MemoryVault(root=root)
        got = v2.recall("learnings", key="lesson")
        assert len(got) == 1
        assert got[0]["value"]["insight"] == "push early"

    def test_file_is_valid_json(self, tmp_path):
        root = tmp_path / "v"
        v = MemoryVault(root=str(root))
        v.remember("ns", "k", {"x": 1})
        raw = json.loads((root / "ns.json").read_text(encoding="utf-8"))
        assert raw["namespace"] == "ns"
        assert len(raw["entries"]) == 1

    def test_corrupt_file_recovers(self, tmp_path):
        root = tmp_path / "v"
        v = MemoryVault(root=str(root))
        v.remember("ns", "k", 1)
        (root / "ns.json").write_text("{{{ not json", encoding="utf-8")
        # must not crash — starts fresh, keeps .bak
        assert v.recall("ns") == []
        v.remember("ns", "k2", 2)
        assert len(v.recall("ns")) == 1
        assert (root / "ns.json.bak").exists()

    def test_max_entries_bounded(self, tmp_path):
        v = MemoryVault(root=str(tmp_path / "v"), max_entries=5)
        for i in range(12):
            v.remember("ns", f"k{i}", i)
        got = v.recall("ns", limit=50)
        assert len(got) == 5
        assert got[-1]["value"] == 11  # newest kept

    def test_no_tmp_leftovers(self, tmp_path):
        root = tmp_path / "v"
        v = MemoryVault(root=str(root))
        v.remember("ns", "k", 1)
        assert list(root.glob("*.tmp")) == []

    def test_thread_safety(self, vault):
        def worker(n):
            for i in range(20):
                vault.remember("ns", f"t{n}-{i}", i)
        threads = [threading.Thread(target=worker, args=(n,)) for n in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(vault.recall("ns", limit=200)) == 80


# ═════════════════════════════════════════════════════════
# 4. Namespaces / stats / export
# ═════════════════════════════════════════════════════════

class TestVaultMeta:
    def test_invalid_namespace_raises(self, vault):
        with pytest.raises(ValueError):
            vault.remember("../evil", "k", 1)
        with pytest.raises(ValueError):
            vault.remember("Spaces Bad", "k", 1)

    def test_namespaces_listing(self, vault):
        vault.remember("aaa", "k", 1)
        vault.remember("bbb", "k", 1)
        assert vault.namespaces() == ["aaa", "bbb"]

    def test_stats(self, vault):
        vault.remember("ns1", "k", 1)
        vault.remember("ns1", "k2", 2)
        vault.remember("ns2", "k", 3)
        s = vault.stats()
        assert s["total_entries"] == 3
        assert s["namespaces"] == {"ns1": 2, "ns2": 1}

    def test_export_markdown(self, vault):
        vault.remember("ns", "lesson", {"txt": "commit often"}, tags=["rule"])
        md = vault.export_markdown("ns")
        assert "# 🧠 Vault — ns" in md
        assert "lesson" in md and "commit often" in md and "`rule`" in md

    def test_default_vault_singleton(self):
        v1 = get_default_vault()
        v2 = get_default_vault()
        assert v1 is v2
        # default root points at repo data/vault
        assert str(v1.stats()["root"]).endswith(os.path.join("data", "vault"))


# ═════════════════════════════════════════════════════════
# 5. Integration — SelfEvolveCore persistence (offline, no LLM)
# ═════════════════════════════════════════════════════════

class TestVaultSelfEvolveIntegration:
    def test_evolve_persists_learning(self, tmp_path):
        from ai_earth.self_evolve import SelfEvolveCore
        v = MemoryVault(root=str(tmp_path / "v"))
        core = SelfEvolveCore(llm=False, verbose=False, vault=v)
        core.evolve("summarize the research landscape", max_iterations=1)
        stored = v.recall("learnings")
        assert len(stored) >= 1
        assert "final_score" in stored[0]["value"]

    def test_new_core_restores_learnings(self, tmp_path):
        from ai_earth.self_evolve import SelfEvolveCore
        v = MemoryVault(root=str(tmp_path / "v"))
        core1 = SelfEvolveCore(llm=False, verbose=False, vault=v)
        core1.evolve("classify these documents", max_iterations=1)
        n_persisted = len(v.recall("learnings"))
        # brand-new core (simulates a fresh session after env reset)
        core2 = SelfEvolveCore(llm=False, verbose=False, vault=v)
        assert core2.num_learnings() == n_persisted >= 1

    def test_no_vault_is_backward_compatible(self):
        from ai_earth.self_evolve import SelfEvolveCore
        core = SelfEvolveCore(llm=False, verbose=False)  # no vault param
        core.evolve("build a pipeline", max_iterations=1)
        assert core.num_learnings() >= 1  # in-memory only, no crash

    def test_broken_vault_never_breaks_evolution(self):
        from ai_earth.self_evolve import SelfEvolveCore

        class BrokenVault:
            def recall(self, *a, **k):
                raise RuntimeError("disk on fire")

            def remember(self, *a, **k):
                raise RuntimeError("disk on fire")

        core = SelfEvolveCore(llm=False, verbose=False, vault=BrokenVault())
        result = core.evolve("research quantum computing", max_iterations=1)
        assert result is not None  # evolution survived the broken vault
        assert core.num_learnings() >= 1
