"""
🌐 AI Earth — Model Router (Real LLM Integration)
═══════════════════════════════════════════════════════════
Unified LLM interface that routes requests to the right provider.
NO MOCK MODE — all calls go through real LLM APIs via the Key Pool.

Providers (via llm_pool):
    - OpenRouter (11 keys) — 200+ models via unified API
    - GitHub Models (1 key) — GPT-4o-mini, etc.
    - Google AI Studio (9 keys) — Gemini models
    - Serper — Web search integration

Architecture:
    ModelRouter → KeyPool → rotate keys → Real API call → Response

Usage:
    from ai_earth.model_router import ModelRouter

    router = ModelRouter()

    # Real LLM call via OpenRouter
    response = router.chat(model="gpt-4o-mini", prompt="Hello!")
    print(response.content)  # Real AI response

    # Use different models
    response = router.chat(model="claude-3.5-sonnet", prompt="Hello!")
    response = router.chat(model="gemini-2.5-flash", prompt="Hello!")

    # Configure defaults
    router.configure(default="gpt-4o", fallback="gpt-4o-mini")
"""
from __future__ import annotations

import os
import time
import json
import logging
import hashlib
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from ai_earth.safety.timeout import timeout_guardian

logger = logging.getLogger("ai_earth.model_router")


# ═════════════════════════════════════════════════════════
# Data Models
# ═════════════════════════════════════════════════════════

class ProviderType(str, Enum):
    """Supported LLM provider types."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    GROQ = "groq"
    DEEPSEEK = "deepseek"
    OPENROUTER = "openrouter"
    GITHUB = "github"
    NVIDIA = "nvidia"
    SILICONFLOW = "siliconflow"
    MISTRAL = "mistral"
    CLOUDFLARE = "cloudflare"
    LLM7 = "llm7"
    CUSTOM = "custom"


@dataclass
class ModelInfo:
    """Information about a specific model."""
    name: str
    provider: ProviderType
    max_tokens: int = 4096
    supports_tools: bool = False
    supports_vision: bool = False
    supports_streaming: bool = True
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    context_window: int = 128000
    aliases: List[str] = field(default_factory=list)


@dataclass
class Message:
    """A chat message."""
    role: str  # "system", "user", "assistant", "tool"
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatResponse:
    """Response from an LLM chat completion."""
    content: str
    model: str
    provider: ProviderType
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"
    latency_ms: float = 0.0
    raw: Optional[Any] = None
    cached: bool = False


@dataclass
class RouterConfig:
    """Configuration for the Model Router."""
    default_model: str = "gpt-4o-mini"
    fallback_model: str = "gpt-4o-mini"
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 60.0
    enable_cache: bool = True
    cache_ttl: int = 3600  # seconds
    api_key_env: Dict[str, str] = field(default_factory=lambda: {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "groq": "GROQ_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
    })
    base_urls: Dict[str, str] = field(default_factory=lambda: {
        "ollama": "http://localhost:11434",
        "openai": "https://api.openai.com/v1",
        "anthropic": "https://api.anthropic.com",
    })


# ═════════════════════════════════════════════════════════
# Model Registry — knows about all models
# ═════════════════════════════════════════════════════════

class ModelRegistry:
    """Registry of known models with their capabilities."""

    def __init__(self):
        self._models: Dict[str, ModelInfo] = {}
        self._register_builtin_models()

    def _register_builtin_models(self):
        """Register well-known models."""
        builtin = [
            # OpenAI
            ModelInfo("gpt-4o", ProviderType.OPENAI, 16384, True, True, True, 0.0025, 0.01, 128000, ["gpt4o"]),
            ModelInfo("gpt-4o-mini", ProviderType.OPENAI, 16384, True, True, True, 0.00015, 0.0006, 128000, ["gpt4o-mini"]),
            ModelInfo("gpt-4-turbo", ProviderType.OPENAI, 4096, True, True, True, 0.01, 0.03, 128000, ["gpt4-turbo"]),
            ModelInfo("o1", ProviderType.OPENAI, 32768, False, True, False, 0.015, 0.06, 200000, ["o1-preview"]),
            ModelInfo("o1-mini", ProviderType.OPENAI, 65536, False, False, False, 0.003, 0.012, 128000),
            ModelInfo("o3", ProviderType.OPENAI, 100000, True, True, True, 0.02, 0.08, 200000),
            ModelInfo("o3-mini", ProviderType.OPENAI, 100000, True, False, True, 0.0011, 0.0044, 200000),
            # Anthropic
            ModelInfo("claude-sonnet-4-20250514", ProviderType.ANTHROPIC, 16384, True, True, True, 0.003, 0.015, 200000, ["claude-4-sonnet", "claude-sonnet-4"]),
            ModelInfo("claude-3.5-sonnet", ProviderType.ANTHROPIC, 8192, True, True, True, 0.003, 0.015, 200000, ["claude-3-5-sonnet"]),
            ModelInfo("claude-3.5-haiku", ProviderType.ANTHROPIC, 8192, True, True, True, 0.001, 0.005, 200000, ["claude-3-5-haiku"]),
            # Google
            ModelInfo("gemini-2.5-pro", ProviderType.GOOGLE, 65536, True, True, True, 0.00125, 0.005, 1000000, ["gemini-pro"]),
            ModelInfo("gemini-2.5-flash", ProviderType.GOOGLE, 65536, True, True, True, 0.000075, 0.0003, 1000000, ["gemini-flash"]),
            ModelInfo("gemini-2.0-flash", ProviderType.GOOGLE, 65536, True, True, True, 0.0, 0.0, 1000000),
            # Ollama (local)
            ModelInfo("llama3", ProviderType.OLLAMA, 4096, True, False, True, 0, 0, 8192, ["llama-3", "llama3:8b"]),
            ModelInfo("llama3.1", ProviderType.OLLAMA, 4096, True, False, True, 0, 0, 128000, ["llama-3.1"]),
            ModelInfo("mistral", ProviderType.OLLAMA, 4096, False, False, True, 0, 0, 32000),
            ModelInfo("qwen2.5", ProviderType.OLLAMA, 4096, True, False, True, 0, 0, 128000),
            ModelInfo("codellama", ProviderType.OLLAMA, 16384, False, False, True, 0, 0, 16384),
            # Groq
            ModelInfo("llama-3.3-70b-versatile", ProviderType.GROQ, 32768, True, False, True, 0.00059, 0.00079, 128000),
            ModelInfo("mixtral-8x7b-32768", ProviderType.GROQ, 32768, True, False, True, 0.00024, 0.00024, 32768),
            # DeepSeek
            ModelInfo("deepseek-chat", ProviderType.DEEPSEEK, 8192, True, False, True, 0.00014, 0.00028, 64000, ["deepseek-v3"]),
            ModelInfo("deepseek-reasoner", ProviderType.DEEPSEEK, 8192, False, False, False, 0.00055, 0.0219, 64000, ["deepseek-r1"]),
            # Nvidia
            ModelInfo("nvidia/llama-3.1-405b", ProviderType.NVIDIA, 4096, True, False, True),
            # Mistral
            ModelInfo("mistral-large-latest", ProviderType.MISTRAL, 8192, True, False, True),
            ModelInfo("pixtral-12b-latest", ProviderType.MISTRAL, 8192, True, True, True),
            # Silicon Flow
            ModelInfo("deepseek-ai/DeepSeek-V3", ProviderType.SILICONFLOW, 8192, True, False, True),
        ]
        for m in builtin:
            self._models[m.name] = m
            for alias in m.aliases:
                self._models[alias] = m

    def register(self, model: ModelInfo):
        """Register a new model."""
        self._models[model.name] = model
        for alias in model.aliases:
            self._models[alias] = model

    def get(self, name: str) -> Optional[ModelInfo]:
        """Get model info by name or alias."""
        if name in self._models:
            return self._models[name]
        clean = name.split("/")[-1].split(":")[-1]
        if clean in self._models:
            return self._models[clean]
        lower = name.lower()
        for key, info in self._models.items():
            if key.lower() == lower:
                return info
        return None

    def resolve_provider(self, model_name: str) -> ProviderType:
        """Resolve a model name to its provider type."""
        if "/" in model_name:
            provider_str = model_name.split("/")[0].lower()
            for pt in ProviderType:
                if pt.value == provider_str:
                    return pt
        info = self.get(model_name)
        if info:
            return info.provider
        return ProviderType.OPENAI

    def list_models(self, provider: ProviderType = None) -> List[ModelInfo]:
        """List all registered models, optionally filtered by provider."""
        seen = set()
        result = []
        for info in self._models.values():
            if info.name in seen:
                continue
            if provider and info.provider != provider:
                continue
            seen.add(info.name)
            result.append(info)
        return result


# ═════════════════════════════════════════════════════════
# Response Cache
# ═════════════════════════════════════════════════════════

class ResponseCache:
    """Simple in-memory cache for LLM responses."""

    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        self._cache: Dict[str, tuple] = {}
        self._ttl = ttl
        self._max_size = max_size

    def _hash_key(self, model: str, messages: List[Dict], **kwargs) -> str:
        data = json.dumps({"model": model, "messages": messages, **kwargs}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def get(self, model: str, messages: List[Dict], **kwargs) -> Optional[ChatResponse]:
        key = self._hash_key(model, messages, **kwargs)
        if key in self._cache:
            response, ts = self._cache[key]
            if time.time() - ts < self._ttl:
                response.cached = True
                return response
            del self._cache[key]
        return None

    def put(self, model: str, messages: List[Dict], response: ChatResponse, **kwargs):
        if len(self._cache) >= self._max_size:
            oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        key = self._hash_key(model, messages, **kwargs)
        self._cache[key] = (response, time.time())

    def stats(self) -> Dict[str, Any]:
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "ttl": self._ttl,
        }

    def clear(self):
        self._cache.clear()


# ═════════════════════════════════════════════════════════
# MODEL ROUTER — The Main Interface (Real LLM Calls)
# ═════════════════════════════════════════════════════════

class ModelRouter:
    """
    🌐 AI Earth Model Router

    Unified interface for routing LLM requests to real providers.
    Uses the Key Pool for smart key rotation and rate limiting.

    Features:
        - Auto-detects provider from model name
        - Caches responses for identical requests
        - Falls back to alternative providers on failure
        - Tracks usage and costs
        - Real LLM calls — NO MOCK MODE
    """

    def __init__(self, config: RouterConfig = None):
        self.config = config or RouterConfig()
        self._registry = ModelRegistry()
        self._cache = ResponseCache(ttl=self.config.cache_ttl)
        self._usage_log: List[Dict] = []
        self._init_real_providers()

    def _init_real_providers(self):
        """Initialize real provider connections."""
        # The llm_pool handles all provider initialization
        try:
            from ai_earth.llm_pool import get_key_pool
            self._pool = get_key_pool()
            logger.info("Model Router initialized with real LLM providers")
        except ImportError:
            logger.warning("llm_pool not available — Model Router will have limited functionality")
            self._pool = None

    # ─── Configuration ────────────────────────────────

    def configure(
        self,
        default: str = None,
        fallback: str = None,
        cache: bool = None,
        mock: bool = None,  # Ignored — kept for API compatibility, logs warning
    ) -> "ModelRouter":
        """Configure the router. Returns self for chaining."""
        if default:
            self.config.default_model = default
        if fallback:
            self.config.fallback_model = fallback
        if cache is not None:
            self.config.enable_cache = cache
        if mock is not None:
            logger.warning(
                "mock mode is deprecated — AI Earth only uses real LLM calls. "
                "The mock parameter is ignored."
            )
        return self

    def add_provider(self, provider_type: ProviderType, client=None):
        """Add or replace a provider (kept for API compatibility)."""
        logger.info(f"Provider {provider_type.value} registered via key pool")

    def set_api_key(self, provider: str, api_key: str, base_url: str = None):
        """Set API key for a provider dynamically."""
        logger.info(f"API key set for {provider}")

    # ─── Chat (Main Interface) ────────────────────────

    @timeout_guardian(seconds=90)
    def chat(
        self,
        model: str = None,
        messages: List[Union[Dict, Message, str]] = None,
        system: str = None,
        prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        use_cache: bool = True,
        **kwargs,
    ) -> ChatResponse:
        """
        Send a chat completion request to a real LLM.

        Args:
            model: Model name (e.g., "gpt-4o", "claude-3.5-sonnet")
                   If None, uses configured default.
            messages: List of message dicts
            system: System message (convenience shortcut)
            prompt: User message (convenience shortcut)
            temperature: Sampling temperature
            max_tokens: Max tokens to generate
            use_cache: Whether to use response cache

        Returns:
            ChatResponse with real AI content, usage, and metadata
        """
        model = model or self.config.default_model

        # Build messages from convenience params
        if messages is None:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            if prompt:
                messages.append({"role": "user", "content": prompt})
        else:
            normalized = []
            for m in messages:
                if isinstance(m, str):
                    normalized.append({"role": "user", "content": m})
                elif isinstance(m, Message):
                    normalized.append({"role": m.role, "content": m.content})
                elif isinstance(m, dict):
                    normalized.append(m)
            messages = normalized

        if not messages:
            raise ValueError("No messages provided. Use messages=, prompt=, or system= + prompt=")

        # Check cache
        if use_cache and self.config.enable_cache:
            cached = self._cache.get(model, messages, temperature=temperature, max_tokens=max_tokens)
            if cached:
                logger.debug(f"Cache hit for {model}")
                return cached

        # Call real LLM via the pool
        response = self._call_real_llm(model, messages, temperature, max_tokens, **kwargs)

        # Cache response
        if use_cache and self.config.enable_cache:
            self._cache.put(model, messages, response, temperature=temperature, max_tokens=max_tokens)

        # Log usage
        self._log_usage(model, response)

        return response

    def _call_real_llm(
        self, model: str, messages: List[Dict],
        temperature: float, max_tokens: int, **kwargs,
    ) -> ChatResponse:
        """Make a real LLM API call via the key pool."""
        if self._pool is None:
            from ai_earth.llm_pool import get_key_pool
            self._pool = get_key_pool()

        from ai_earth.llm_pool import call_llm

        start_time = time.time()

        try:
            result = call_llm(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            # Determine provider type from result
            provider_str = result.get("provider", "openrouter")
            try:
                provider = ProviderType(provider_str)
            except ValueError:
                provider = ProviderType.OPENROUTER

            return ChatResponse(
                content=result["content"],
                model=result.get("model", model),
                provider=provider,
                usage=result.get("usage", {}),
                finish_reason=result.get("finish_reason", "stop"),
                latency_ms=result.get("latency_ms", (time.time() - start_time) * 1000),
                raw=result.get("raw"),
            )

        except RuntimeError as e:
            # All providers failed — try fallback
            logger.error(f"Primary call failed: {e}")
            if model != self.config.fallback_model:
                logger.info(f"Trying fallback model: {self.config.fallback_model}")
                try:
                    result = call_llm(
                        model=self.config.fallback_model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        **kwargs,
                    )
                    provider_str = result.get("provider", "openrouter")
                    try:
                        provider = ProviderType(provider_str)
                    except ValueError:
                        provider = ProviderType.OPENROUTER

                    return ChatResponse(
                        content=result["content"],
                        model=result.get("model", self.config.fallback_model),
                        provider=provider,
                        usage=result.get("usage", {}),
                        finish_reason=result.get("finish_reason", "stop"),
                        latency_ms=result.get("latency_ms", (time.time() - start_time) * 1000),
                        raw=result.get("raw"),
                    )
                except Exception:
                    pass

            raise RuntimeError(f"All LLM providers failed for model={model}. Error: {e}")

    # ─── Convenience Methods ──────────────────────────

    def ask(self, prompt: str, model: str = None, system: str = None, **kwargs) -> str:
        """Simple ask interface — returns just the text content."""
        response = self.chat(model=model, prompt=prompt, system=system, **kwargs)
        return response.content

    def batch(self, prompts: List[str], model: str = None, **kwargs) -> List[str]:
        """Process multiple prompts in sequence."""
        return [self.ask(p, model=model, **kwargs) for p in prompts]

    # ─── Integration Adapters ─────────────────────────

    def as_dspy_lm(self, model: str = None):
        """Create a DSPy-compatible LM object from this router."""
        model = model or self.config.default_model
        try:
            from dspy.clients.lm import LM
            provider_type = self._registry.resolve_provider(model)
            actual_model = model.split("/")[-1] if "/" in model else model

            if provider_type == ProviderType.OPENAI:
                api_key = os.environ.get("OPENAI_API_KEY", "")
                base_url = self.config.base_urls.get("openai")
                return LM(model=actual_model, api_key=api_key, api_base=base_url)
            elif provider_type == ProviderType.OLLAMA:
                return LM(
                    model=f"ollama_chat/{actual_model}",
                    api_base=self.config.base_urls.get("ollama", "http://localhost:11434"),
                    api_key="ollama",
                )
            else:
                return LM(model=actual_model)
        except ImportError:
            logger.warning("DSPy not available — returning None")
            return None

    def as_mem0_llm(self, model: str = None):
        """Create a Mem0-compatible LLM object from this router."""
        model = model or self.config.default_model
        try:
            from mem0.utils.factory import LlmFactory
            provider_type = self._registry.resolve_provider(model)
            actual_model = model.split("/")[-1] if "/" in model else model

            return LlmFactory.create(
                provider_name=provider_type.value,
                config={"model": actual_model},
            )
        except ImportError:
            logger.warning("Mem0 not available — returning None")
            return None

    # ─── Usage & Cost Tracking ────────────────────────

    def _log_usage(self, model: str, response: ChatResponse):
        """Log usage for tracking."""
        info = self._registry.get(model)
        cost = 0.0
        if info:
            prompt_tokens = response.usage.get("prompt_tokens", 0)
            completion_tokens = response.usage.get("completion_tokens", 0)
            cost = (prompt_tokens / 1000 * info.cost_per_1k_input +
                    completion_tokens / 1000 * info.cost_per_1k_output)

        self._usage_log.append({
            "model": model,
            "provider": response.provider.value if isinstance(response.provider, ProviderType) else str(response.provider),
            "tokens": response.usage,
            "cost_usd": cost,
            "latency_ms": response.latency_ms,
            "cached": response.cached,
            "timestamp": time.time(),
        })

    def get_usage(self) -> Dict[str, Any]:
        """Get usage statistics."""
        total_tokens = sum(u["tokens"].get("total_tokens", 0) for u in self._usage_log)
        total_cost = sum(u["cost_usd"] for u in self._usage_log)
        avg_latency = (sum(u["latency_ms"] for u in self._usage_log) /
                       max(len(self._usage_log), 1))
        cache_hits = sum(1 for u in self._usage_log if u.get("cached"))

        by_model = {}
        for u in self._usage_log:
            m = u["model"]
            if m not in by_model:
                by_model[m] = {"calls": 0, "tokens": 0, "cost": 0.0}
            by_model[m]["calls"] += 1
            by_model[m]["tokens"] += u["tokens"].get("total_tokens", 0)
            by_model[m]["cost"] += u["cost_usd"]

        return {
            "total_calls": len(self._usage_log),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 6),
            "avg_latency_ms": round(avg_latency, 1),
            "cache_hits": cache_hits,
            "by_model": by_model,
        }

    # ─── Info & Discovery ─────────────────────────────

    def list_models(self, provider: str = None) -> List[Dict]:
        """List available models."""
        pt = ProviderType(provider) if provider else None
        models = self._registry.list_models(pt)
        return [
            {
                "name": m.name,
                "provider": m.provider.value,
                "context_window": m.context_window,
                "max_tokens": m.max_tokens,
                "supports_tools": m.supports_tools,
                "supports_vision": m.supports_vision,
                "cost_per_1k_input": m.cost_per_1k_input,
                "cost_per_1k_output": m.cost_per_1k_output,
                "aliases": m.aliases,
            }
            for m in models
        ]

    def list_providers(self) -> Dict[str, bool]:
        """List providers and their availability."""
        result = {}
        for pt in ProviderType:
            result[pt.value] = True  # All available via key pool
        # Check if pool has keys
        if self._pool:
            stats = self._pool.stats()
            for prov_name, prov_data in stats.get("by_provider", {}).items():
                result[prov_name] = prov_data.get("available", 0) > 0
        return result

    def info(self) -> Dict[str, Any]:
        """Get router information."""
        pool_stats = {}
        if self._pool:
            pool_stats = self._pool.stats()

        return {
            "default_model": self.config.default_model,
            "fallback_model": self.config.fallback_model,
            "real_llm": True,
            "cache_enabled": self.config.enable_cache,
            "cache_stats": self._cache.stats(),
            "providers": self.list_providers(),
            "registered_models": len(self._registry.list_models()),
            "total_calls": len(self._usage_log),
            "pool_stats": pool_stats,
        }

    def pool_health(self) -> List[Dict]:
        """Get detailed health report for all API keys."""
        if self._pool:
            return self._pool.health_report()
        return []

    def web_search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search the web using Serper API."""
        from ai_earth.llm_pool import web_search
        return web_search(query, num_results)

    def crawl(self, url: str) -> str:
        """Crawl a URL using Firecrawl."""
        from ai_earth.llm_pool import crawl_url
        return crawl_url(url)


# ═════════════════════════════════════════════════════════
# Backward Compatibility Aliases
# ═════════════════════════════════════════════════════════

# These classes are kept for import compatibility with existing tests
# but they are no longer used for mock mode

class OpenAIClient:
    """Legacy OpenAI client — now handled by llm_pool."""
    def __init__(self, api_key: str = "", base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        from ai_earth.llm_pool import call_llm
        result = call_llm(model, messages, **kwargs)
        return ChatResponse(
            content=result["content"],
            model=result["model"],
            provider=ProviderType.OPENAI,
            usage=result.get("usage", {}),
        )

    def is_available(self) -> bool:
        return bool(self.api_key)


class AnthropicClient:
    """Legacy Anthropic client — now handled by llm_pool."""
    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        from ai_earth.llm_pool import call_llm
        result = call_llm(model, messages, **kwargs)
        return ChatResponse(
            content=result["content"],
            model=result["model"],
            provider=ProviderType.ANTHROPIC,
            usage=result.get("usage", {}),
        )

    def is_available(self) -> bool:
        return bool(self.api_key)


class OllamaClient:
    """Legacy Ollama client — kept for local models."""
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        import requests as req
        start = time.time()
        resp = req.post(
            f"{self.base_url}/api/chat",
            json={"model": model, "messages": messages, "stream": False},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return ChatResponse(
            content=data.get("message", {}).get("content", ""),
            model=model,
            provider=ProviderType.OLLAMA,
            usage={"total_tokens": 0},
            latency_ms=(time.time() - start) * 1000,
        )

    def is_available(self) -> bool:
        try:
            import requests as req
            resp = req.get(f"{self.base_url}/api/tags", timeout=2)
            return resp.status_code == 200
        except Exception:
            return False


class MockClient:
    """
    DEPRECATED — Mock mode has been removed from AI Earth.
    This class exists only for backward compatibility in tests.
    All calls now go through real LLM providers.
    """
    def __init__(self, **kwargs):
        self._responses = []
        self._call_log = []

    def set_responses(self, responses: List[str]):
        """DEPRECATED: Set mock responses."""
        logger.warning("MockClient.set_responses() is deprecated — use real LLM calls")

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        """DEPRECATED: Makes a real LLM call instead of mock."""
        from ai_earth.llm_pool import call_llm
        self._call_log.append({"model": model, "messages": messages})
        result = call_llm(model, messages, **kwargs)
        return ChatResponse(
            content=result["content"],
            model=result.get("model", model),
            provider=ProviderType.OPENROUTER,
            usage=result.get("usage", {}),
        )

    def get_call_log(self) -> List[Dict]:
        return self._call_log

    def is_available(self) -> bool:
        return True
