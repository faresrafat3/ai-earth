"""
Tests for AI Earth — Boot and Package Structure

Verifies that the package structure is intact and all imports resolve.
These tests grow as components are implemented.
"""

import pytest


class TestPackageStructure:
    """Verify package can be imported and basic structure exists."""

    def test_import_ai_earth(self):
        """AI Earth package is importable."""
        import ai_earth
        assert hasattr(ai_earth, '__version__')
        assert ai_earth.__version__ == "2.3.0"

    def test_import_core(self):
        """Core layer is importable."""
        import ai_earth.core
        assert ai_earth.core is not None

    def test_import_capabilities(self):
        """Capabilities layer is importable."""
        import ai_earth.capabilities
        assert ai_earth.capabilities is not None

    def test_import_agents(self):
        """Agents layer is importable."""
        import ai_earth.agents
        assert ai_earth.agents is not None

    def test_import_workflow(self):
        """Workflow layer is importable."""
        import ai_earth.workflow
        assert ai_earth.workflow is not None

    def test_import_safety(self):
        """Safety layer is importable."""
        import ai_earth.safety
        assert ai_earth.safety is not None

    def test_import_memory(self):
        """Memory layer is importable."""
        import ai_earth.memory
        assert ai_earth.memory is not None

    def test_import_insight(self):
        """Insight layer is importable."""
        import ai_earth.insight
        assert ai_earth.insight is not None

    def test_import_legacy_compat(self):
        """Legacy compatibility layer is importable."""
        import ai_earth.LEGACY_COMPAT
        assert ai_earth.LEGACY_COMPAT is not None


class TestVersion:
    """Verify version and metadata."""

    def test_version_format(self):
        """Version follows semver."""
        import ai_earth
        parts = ai_earth.__version__.split('.')
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_author_defined(self):
        """Author is defined."""
        import ai_earth
        assert hasattr(ai_earth, '__author__')
        assert ai_earth.__author__ == "Fares Rafat"
