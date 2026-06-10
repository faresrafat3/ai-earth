"""
Mem0 — Memory Layer for AI Agents
===================================
Source: https://github.com/mem0ai/mem0 (48K ⭐)
Extracted as LEGO piece for AI Earth — verbatim source files, lazy init.
"""

try:
    from importlib.metadata import version as _version
    __version__ = _version("mem0ai")
except Exception:
    __version__ = "0.1.0"

# Lazy imports to avoid circular deps
try:
    from mem0.memory.base import MemoryBase
except ImportError:
    pass

try:
    from mem0.memory.main import Memory, AsyncMemory
except ImportError:
    pass

try:
    from mem0.memory.storage import SQLiteManager
except ImportError:
    pass

try:
    from mem0.configs.base import MemoryConfig
except ImportError:
    pass
