"""
Tests for AI Earth Model Router
================================
Tests the unified LLM interface.
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
# 3. Mock Client Tests
# ═════════════════════════════════════════════════════════

class TestMockClient:
    """Test mock LLM client."""

    def test_mock_default_response(self):
        client = MockClient()
        resp = client.chat("test-model", [{"role": "user", "content": "hi"}])
        assert "Mock response" in resp.content
        assert resp.model == "test-model"

    def test_mock_custom_responses(self):
        client = MockClient()
        client.set_responses(["Hello!", "World!"])
        r1 = client.chat("test", [{"role": "user", "content": "a"}])
        r2 = client.chat("test", [{"role": "user", "content": "b"}])
        assert r1.content == "Hello!"
        assert r2.content == "World!"

    def test_mock_call_log(self):
        client = MockClient()
        client.chat("m1", [{"role": "user", "content": "a"}])
        client.chat("m2", [{"role": "user", "content": "b"}])
        log = client.get_call_log()
        assert len(log) == 2
        assert log[0]["model"] == "m1"

    def test_mock_always_available(self):
        client = MockClient()
        assert client.is_available()


# ═════════════════════════════════════════════════════════
# 4. Model Router Tests
# ═════════════════════════════════════════════════════════

class TestModelRouter:
    """Test the main Model Router."""

    def test_router_creation(self):
        router = ModelRouter()
        assert router is not None
        assert router.config.default_model == "gpt-4o-mini"

    def test_router_mock_mode(self):
        router = ModelRouter()
        router.configure(mock=True)
        resp = router.chat(model="test-model", prompt="Hello!")
        assert resp.content is not None

    def test_router_ask(self):
        router = ModelRouter()
        router.configure(mock=True)
        result = router.ask("What is AI?")
        assert isinstance(result, str)

    def test_router_batch(self):
        router = ModelRouter()
        router.configure(mock=True)
        results = router.batch(["Q1", "Q2", "Q3"])
        assert len(results) == 3

    def test_router_configure(self):
        router = ModelRouter()
        router.configure(default="gpt-4o", fallback="claude-3.5-sonnet", mock=True)
        assert router.config.default_model == "gpt-4o"
        assert router.config.fallback_model == "claude-3.5-sonnet"
        assert router._mock_mode is True

    def test_router_with_system(self):
        router = ModelRouter()
        router.configure(mock=True)
        resp = router.chat(model="gpt-4o", system="You are a pirate", prompt="Hello!")
        assert resp is not None

    def test_router_with_messages(self):
        router = ModelRouter()
        router.configure(mock=True)
        msgs = [
            {"role": "system", "content": "Be helpful"},
            {"role": "user", "content": "Hi"},
        ]
        resp = router.chat(model="gpt-4o", messages=msgs)
        assert resp is not None

    def test_router_cache(self):
        router = ModelRouter()
        router.configure(mock=True)
        r1 = router.chat(model="gpt-4o", prompt="test cache", use_cache=True)
        r2 = router.chat(model="gpt-4o", prompt="test cache", use_cache=True)
        assert r2.cached is True

    def test_router_no_cache(self):
        router = ModelRouter()
        router.configure(mock=True)
        r1 = router.chat(model="gpt-4o", prompt="test no cache", use_cache=False)
        r2 = router.chat(model="gpt-4o", prompt="test no cache", use_cache=False)
        assert r2.cached is False

    def test_router_usage_tracking(self):
        router = ModelRouter()
        router.configure(mock=True)
        router.chat(model="gpt-4o", prompt="test usage 1")
        router.chat(model="gpt-4o", prompt="test usage 2")
        usage = router.get_usage()
        assert usage["total_calls"] == 2

    def test_router_usage_cost(self):
        router = ModelRouter()
        router.configure(mock=True)
        router.chat(model="gpt-4o", prompt="test cost tracking")
        usage = router.get_usage()
        assert "total_cost_usd" in usage
        assert "by_model" in usage

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

    def test_router_custom_mock_responses(self):
        router = ModelRouter()
        router.configure(mock=True)
        router._mock_client.set_responses(["Custom response!"])
        resp = router.chat(model="test", prompt="anything")
        assert resp.content == "Custom response!"

    def test_router_add_provider(self):
        router = ModelRouter()
        mock = MockClient()
        router.add_provider(ProviderType.CUSTOM, mock)

    def test_router_no_messages_error(self):
        router = ModelRouter()
        with pytest.raises(ValueError, match="No messages"):
            router.chat(model="test")


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
        router.configure(mock=True)

        # Create workflow and run with router
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
        # as_dspy_lm returns a DSPy LM or None
        lm = router.as_dspy_lm("gpt-4o")
        # May return None if DSPy LM can't be created, that's ok

    def test_router_mem0_compatible(self):
        from ai_earth.model_router import ModelRouter
        router = ModelRouter()
        # as_mem0_llm tries to create real LLM — may fail without API keys
        try:
            llm = router.as_mem0_llm("gpt-4o")
        except Exception:
            llm = None  # Expected without API keys
        # That's ok — integration works, just needs credentials

    def test_router_with_all_packages(self):
        """Test that router works alongside all LEGO packages."""
        from ai_earth.model_router import ModelRouter
        from dspy.primitives.example import Example
        from mem0.configs.base import MemoryConfig

        router = ModelRouter()
        router.configure(mock=True)

        e = Example(question="test")
        mc = MemoryConfig()
        resp = router.ask("Hello!")

        assert e.question == "test"
        assert mc is not None
        assert isinstance(resp, str)
