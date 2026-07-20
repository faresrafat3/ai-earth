"""
🧠 ai_earth.memory — Persistent memory layer

MemoryVault: file-backed cross-session memory (survives sandbox resets).
"""

from ai_earth.memory.vault import MemoryVault, get_default_vault

__all__ = ["MemoryVault", "get_default_vault"]
