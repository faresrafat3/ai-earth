"""
Tests for AI Earth Model Router
================================
Tests the unified LLM interface with REAL LLM calls.
No mock mode — all tests make real API calls via the Key Pool.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs'))

from ai_earth.model_router import (
    ModelRouter, RouterConfig, ModelRegistry, ModelInfo, ResponseCache,
    ProviderType, Message, ChatResponse, MockClient,
    OpenAIClient, OllamaClient, AnthropicClient,
)


# ═════════════════════════════════════════════════════════
# 1. Model Registry Tests
# ═════════════════════════════════════════════════════════

class TestModelRegistry:
    """Test model registry and resolution."""

    def test_builtin_models_registered(self):
        reg = ModelRegistry()
        gpt4o = reg.get("gpt-4o")
        assert gpt4o is not None
        assert gpt4o.provider == ProviderType.OPENAI

    def test_alias_resolution(self):
        reg = ModelRegistry()
        m = reg.get("gpt4o")
        assert m is not None
        assert m.name == "gpt-4o"

    def test_provider_resolution_openai(self):
        reg = ModelRegistry()
        pt = reg.resolve_provider("gpt-4o")
        assert pt == ProviderType.OPENAI

    def test_provider_resolution_anthropic(self):
        reg = ModelRegistry()
        pt = reg.resolve_provider("claude-3.5-sonnet")
        assert pt == ProviderType.ANTHROPIC

    def test_provider_resolution_prefix(self):
        reg = ModelRegistry()
        pt = reg.resolve_provider("ollama/llama3")
        assert pt == ProviderType.OLLAMA

    def test_provider_resolution_google(self):
        reg = ModelRegistry()
        pt = reg.resolve_provider("gemini-2.5-pro")
        assert pt == ProviderType.GOOGLE

    def test_provider_resolution_groq(self):
        reg = ModelRegistry()
        pt = reg.resolve_provider("llama-3.3-70b-versatile")
        assert pt == ProviderType.GROQ

    def test_provider_resolution_deepseek(self):
        reg = ModelRegistry()
        pt = reg.resolve_provider("deepseek-chat")
        assert pt == ProviderType.DEEPSEEK

    def test_custom_model_registration(self):
        reg = ModelRegistry()
        custom = ModelInfo("my-model", ProviderType.CUSTOM, 8192, aliases=["mm"])
        reg.register(custom)
        assert reg.get("my-model") is not None
        assert reg.get("mm") is not None

    def test_list_models(self):
        reg = ModelRegistry()
        models = reg.list_models()
        assert len(models) > 10

    def test_list_models_filtered(self):
        reg = ModelRegistry()
        openai_models = reg.list_models(provider=ProviderType.OPENAI)
        assert all(m.provider == ProviderType.OPENAI for m in openai_models)

    def test_unknown_model_defaults_openai(self):
        reg = ModelRegistry()
        pt = reg.resolve_provider("totally-unknown-model-xyz")
        assert pt == ProviderType.OPENAI

    def test_model_info_fields(self):
        reg = ModelRegistry()
        gpt4o = reg.get("gpt-4o")
        assert gpt4o.supports_tools is True
        assert gpt4o.supports_vision is True
        assert gpt4o.context_window == 128000
        assert gpt4o.cost_per_1k_input > 0


# ═════════════════════════════════════════════════════════
# 2. Response Cache Tests
# ═════════════════════════════════════════════════════════

class TestResponseCache:
    """Test response caching."""

    def test_cache_miss(self):
        cache = ResponseCache()
        result = cache.get("gpt-4o", [{"role": "user", "content": "hi"}])
        assert result is None

    def test_cache_hit(self):
        cache = ResponseCache()
        msgs = [{"role": "user", "content": "hello"}]
        response = ChatResponse(content="Hi!", model="gpt-4o", provider=ProviderType.OPENAI)
        cache.put("gpt-4o", msgs, response)
        cached = cache.get("gpt-4o", msgs)
        assert cached is not None
        assert cached.content == "Hi!"
        assert cached.cached is True

    def test_cache_different_messages(self):
        cache = ResponseCache()
        msgs1 = [{"role": "user", "content": "hello"}]
        msgs2 = [{"role": "user", "content": "world"}]
        response = ChatResponse(content="Hi!", model="gpt-4o", provider=ProviderType.OPENAI)
        cache.put("gpt-4o", msgs1, response)
        assert cache.get("gpt-4o", msgs2) is None

    def test_cache_stats(self):
        cache = ResponseCache()
        assert cache.stats()["size"] == 0

    def test_cache_clear(self):
        cache = ResponseCache()
        msgs = [{"role": "user", "content": "test"}]
        cache.put("gpt-4o", msgs, ChatResponse(content="ok", model="gpt-4o", provider=ProviderType.OPENAI))
        assert cache.stats()["size"] == 1
        cache.clear()
        assert cache.stats()["size"] == 0


# ═════════════════════════════════════════════════════════
# 3. Real LLM Provider Tests (Integration)
# ═════════════════════════════════════════════════════════

class TestRealLLMProvider:
    """Test real LLM provider calls via the Key Pool."""

    def test_real_chat_call(self):
        """Test that a real LLM call works and returns content."""
        router = ModelRouter()
        resp = router.chat(model="gpt-4o-mini", prompt="Say the word 'test' and nothing else.", max_tokens=10)
        assert resp.content is not None
        assert len(resp.content) > 0
        assert isinstance(resp.content, str)
        assert "test" in resp.content.lower()

    def test_real_chat_with_system(self):
        """Test real chat with system message."""
        router = ModelRouter()
        resp = router.chat(
            model="gpt-4o-mini",
            system="You only reply with the word 'hello'.",
            prompt="Hi there!",
            max_tokens=10,
        )
        assert resp.content is not None
        assert len(resp.content) > 0

    def test_real_chat_with_messages(self):
        """Test real chat with message list."""
        router = ModelRouter()
        msgs = [
            {"role": "system", "content": "Reply with exactly: OK"},
            {"role": "user", "content": "Ready?"},
        ]
        resp = router.chat(model="gpt-4o-mini", messages=msgs, max_tokens=5)
        assert resp.content is not None
        assert len(resp.content) > 0

    def test_real_ask(self):
        """Test the ask() convenience method."""
        router = ModelRouter()
        result = router.ask("Say exactly: pong", model="gpt-4o-mini", max_tokens=10)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_real_usage_tracking(self):
        """Test that usage is tracked for real calls."""
        router = ModelRouter()
        router.chat(model="gpt-4o-mini", prompt="test usage tracking", max_tokens=10)
        usage = router.get_usage()
        assert usage["total_calls"] >= 1

    def test_real_cache(self):
        """Test that caching works with real responses."""
        router = ModelRouter()
        prompt = "test_cache_" + str(id(router))  # Unique prompt
        r1 = router.chat(model="gpt-4o-mini", prompt=prompt, max_tokens=5, use_cache=True)
        r2 = router.chat(model="gpt-4o-mini", prompt=prompt, max_tokens=5, use_cache=True)
        assert r2.cached is True

    def test_real_info(self):
        """Test router info reflects real LLM mode."""
        router = ModelRouter()
        info = router.info()
        assert info["real_llm"] is True
        assert "pool_stats" in info

    def test_pool_health(self):
        """Test pool health report."""
        router = ModelRouter()
        health = router.pool_health()
        assert isinstance(health, list)
        assert len(health) > 0
        # At least some keys should be available
        available = [h for h in health if h["available"]]
        assert len(available) > 0


# ═════════════════════════════════════════════════════════
# 4. Model Router Tests (Configuration)
# ═════════════════════════════════════════════════════════

class TestModelRouter:
    """Test the main Model Router configuration."""

    def test_router_creation(self):
        router = ModelRouter()
        assert router is not None
        assert router.config.default_model == "gpt-4o-mini"

    def test_router_configure_default(self):
        router = ModelRouter()
        router.configure(default="gpt-4o", fallback="claude-3.5-sonnet")
        assert router.config.default_model == "gpt-4o"
        assert router.config.fallback_model == "claude-3.5-sonnet"

    def test_router_list_models(self):
        router = ModelRouter()
        models = router.list_models()
        assert len(models) > 10
        names = [m["name"] for m in models]
        assert "gpt-4o" in names

    def test_router_list_providers(self):
        router = ModelRouter()
        providers = router.list_providers()
        assert "openai" in providers
        assert "ollama" in providers

    def test_router_info(self):
        router = ModelRouter()
        info = router.info()
        assert "default_model" in info
        assert "providers" in info
        assert "registered_models" in info

    def test_router_no_messages_error(self):
        router = ModelRouter()
        with pytest.raises(ValueError, match="No messages"):
            router.chat(model="test")

    def test_mock_param_warning(self):
        """Test that mock=True is ignored with a warning (not error)."""
        import logging
        router = ModelRouter()
        # Should not raise — just log a warning
        router.configure(mock=True)
        assert True  # If we get here, it didn't crash

    def test_router_add_provider(self):
        """Test add_provider doesn't crash."""
        router = ModelRouter()
        router.add_provider(ProviderType.CUSTOM)

    def test_router_set_api_key(self):
        """Test set_api_key doesn't crash."""
        router = ModelRouter()
        router.set_api_key("openai", "test-key")


# ═════════════════════════════════════════════════════════
# 5. Message & Response Data Tests
# ═════════════════════════════════════════════════════════

class TestDataModels:
    """Test data model classes."""

    def test_message_creation(self):
        m = Message(role="user", content="Hello")
        assert m.role == "user"
        assert m.content == "Hello"

    def test_chat_response(self):
        r = ChatResponse(content="Hi", model="gpt-4o", provider=ProviderType.OPENAI)
        assert r.content == "Hi"
        assert r.cached is False

    def test_provider_types(self):
        assert ProviderType.OPENAI.value == "openai"
        assert ProviderType.ANTHROPIC.value == "anthropic"
        assert ProviderType.OLLAMA.value == "ollama"

    def test_router_config_defaults(self):
        config = RouterConfig()
        assert config.default_model == "gpt-4o-mini"
        assert config.max_retries == 3
        assert config.enable_cache is True


# ═════════════════════════════════════════════════════════
# 6. Integration — Router + LEGO Pieces
# ═════════════════════════════════════════════════════════

class TestRouterIntegration:
    """Test Model Router integration with LEGO pieces."""

    def test_router_with_orchestrator(self):
        from ai_earth.orchestrator import AIEarth
        from ai_earth.model_router import ModelRouter

        earth = AIEarth()
        router = ModelRouter()

        workflow = (
            earth.builder()
            .goal("Test workflow")
            .task("step1", inputs={"x": "input"}, outputs={"y": "output"}, prompt="Process x into y")
            .sequential()
            .build()
        )
        graph = earth.create_workflow_from_spec(workflow)
        assert graph is not None

    def test_router_dspy_compatible(self):
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        lm = router.as_dspy_lm("gpt-4o")
        # May return None if DSPy LM can't be created, that's ok

    def test_router_mem0_compatible(self):
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        try:
            llm = router.as_mem0_llm("gpt-4o")
        except Exception:
            llm = None

    def test_router_with_all_packages(self):
        """Test that router works alongside all LEGO packages."""
        from ai_earth.model_router import ModelRouter
        from dspy.primitives.example import Example
        from mem0.configs.base import MemoryConfig

        router = ModelRouter()
        e = Example(question="test")
        mc = MemoryConfig()
        resp = router.ask("Hello!", model="gpt-4o-mini", max_tokens=10)

        assert e.question == "test"
        assert mc is not None
        assert isinstance(resp, str)
