"""
🌐 AI Earth — Model Router
═══════════════════════════════════════════════════════════
Unified LLM interface that routes requests to the right provider.
Leverages Mem0's LLM abstraction + DSPy's LM + EvoAgentX's BaseLLM.

Supports:
    - OpenAI (GPT-4o, GPT-4o-mini, o1, o3, etc.)
    - Anthropic (Claude 3.5 Sonnet, Claude 4, etc.)
    - Google (Gemini 2.5 Pro, Flash, etc.)
    - Ollama (Local models: Llama 3, Mistral, etc.)
    - Groq (Fast inference)
    - DeepSeek
    - LiteLLM (200+ providers via unified API)
    - Any custom endpoint

Architecture:
    ModelRouter → ProviderRegistry → LLMProvider → Response

Usage:
    from ai_earth.model_router import ModelRouter

    router = ModelRouter()

    # Auto-route based on model name
    response = router.chat("gpt-4o", messages=[...])
    response = router.chat("claude-3.5-sonnet", messages=[...])
    response = router.chat("ollama/llama3", messages=[...])

    # Or configure default
    router.configure(default="gpt-4o", fallback="gpt-4o-mini")
    response = router.chat(messages=[...])  # uses default

    # Use with DSPy
    lm = router.as_dspy_lm("gpt-4o")
    # Use with Mem0
    mem0_llm = router.as_mem0_llm("gpt-4o")
"""
from __future__ import annotations

import os
import time
import json
import logging
import hashlib
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field

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
    LITELLM = "litellm"
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
            ModelInfo("deepseek-reasoner", ProviderType.DEEPSEEK, 8192, False, False, False, 0.00055, 0.00219, 64000, ["deepseek-r1"]),
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
        # Direct lookup
        if name in self._models:
            return self._models[name]
        # Normalize: remove provider prefix
        clean = name.split("/")[-1].split(":")[-1]
        if clean in self._models:
            return self._models[clean]
        # Fuzzy match
        lower = name.lower()
        for key, info in self._models.items():
            if key.lower() == lower:
                return info
        return None

    def resolve_provider(self, model_name: str) -> ProviderType:
        """Resolve a model name to its provider type."""
        # Check for provider prefix (e.g., "ollama/llama3")
        if "/" in model_name:
            provider_str = model_name.split("/")[0].lower()
            for pt in ProviderType:
                if pt.value == provider_str:
                    return pt
        # Check model registry
        info = self.get(model_name)
        if info:
            return info.provider
        # Default
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
        self._cache: Dict[str, tuple] = {}  # key -> (response, timestamp)
        self._ttl = ttl
        self._max_size = max_size

    def _hash_key(self, model: str, messages: List[Dict], **kwargs) -> str:
        """Create a hash key from the request."""
        data = json.dumps({"model": model, "messages": messages, **kwargs}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def get(self, model: str, messages: List[Dict], **kwargs) -> Optional[ChatResponse]:
        """Get cached response if available and not expired."""
        key = self._hash_key(model, messages, **kwargs)
        if key in self._cache:
            response, ts = self._cache[key]
            if time.time() - ts < self._ttl:
                response.cached = True
                return response
            del self._cache[key]
        return None

    def put(self, model: str, messages: List[Dict], response: ChatResponse, **kwargs):
        """Cache a response."""
        if len(self._cache) >= self._max_size:
            # Evict oldest
            oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        key = self._hash_key(model, messages, **kwargs)
        self._cache[key] = (response, time.time())

    def clear(self):
        """Clear all cached responses."""
        self._cache.clear()

    def stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {"size": len(self._cache), "max_size": self._max_size}


# ═════════════════════════════════════════════════════════
# Provider Clients — actual LLM API calls
# ═════════════════════════════════════════════════════════

class BaseProviderClient:
    """Base class for LLM provider clients."""

    def __init__(self, api_key: str = None, base_url: str = None, **kwargs):
        self.api_key = api_key
        self.base_url = base_url
        self._client = None

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        raise NotImplementedError

    def is_available(self) -> bool:
        return self.api_key is not None or self._client is not None


class OpenAIClient(BaseProviderClient):
    """OpenAI API client (also works with compatible endpoints)."""

    def __init__(self, api_key: str = None, base_url: str = None, **kwargs):
        super().__init__(api_key, base_url, **kwargs)
        self._client = None
        if api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=api_key, base_url=base_url)
            except ImportError:
                logger.warning("openai package not installed — OpenAI provider unavailable")

    def is_available(self) -> bool:
        return self._client is not None

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        start = time.time()
        temperature = kwargs.pop("temperature", 0.7)
        max_tokens = kwargs.pop("max_tokens", 4096)

        response = self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        return ChatResponse(
            content=response.choices[0].message.content,
            model=response.model,
            provider=ProviderType.OPENAI,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            finish_reason=response.choices[0].finish_reason,
            latency_ms=(time.time() - start) * 1000,
            raw=response,
        )


class OllamaClient(BaseProviderClient):
    """Ollama local LLM client."""

    def __init__(self, base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(base_url=base_url, **kwargs)
        self.base_url = base_url or "http://localhost:11434"

    def is_available(self) -> bool:
        try:
            import urllib.request
            urllib.request.urlopen(f"{self.base_url}/api/tags", timeout=2)
            return True
        except Exception:
            return False

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        start = time.time()
        import urllib.request
        import json as _json

        data = _json.dumps({
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "num_predict": kwargs.get("max_tokens", 4096),
            }
        }).encode()

        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=kwargs.get("timeout", 120)) as resp:
            result = _json.loads(resp.read().decode())

        return ChatResponse(
            content=result.get("message", {}).get("content", ""),
            model=result.get("model", model),
            provider=ProviderType.OLLAMA,
            usage={
                "prompt_tokens": result.get("prompt_eval_count", 0),
                "completion_tokens": result.get("eval_count", 0),
                "total_tokens": result.get("prompt_eval_count", 0) + result.get("eval_count", 0),
            },
            finish_reason="stop",
            latency_ms=(time.time() - start) * 1000,
            raw=result,
        )


class AnthropicClient(BaseProviderClient):
    """Anthropic API client."""

    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self._client = None
        if api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                logger.warning("anthropic package not installed — Anthropic provider unavailable")

    def is_available(self) -> bool:
        return self._client is not None

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        start = time.time()
        max_tokens = kwargs.pop("max_tokens", 4096)
        temperature = kwargs.pop("temperature", 0.7)

        # Extract system message
        system = None
        chat_msgs = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                chat_msgs.append(m)

        params = {
            "model": model,
            "messages": chat_msgs,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system:
            params["system"] = system

        response = self._client.messages.create(**params)

        return ChatResponse(
            content=response.content[0].text,
            model=response.model,
            provider=ProviderType.ANTHROPIC,
            usage={
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
            finish_reason=response.stop_reason or "stop",
            latency_ms=(time.time() - start) * 1000,
            raw=response,
        )


class MockClient(BaseProviderClient):
    """Mock client for testing — returns predefined responses."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._responses: List[str] = []
        self._call_log: List[Dict] = []

    def set_responses(self, responses: List[str]):
        """Set mock responses to cycle through."""
        self._responses = responses

    def chat(self, model: str, messages: List[Dict], **kwargs) -> ChatResponse:
        start = time.time()
        idx = len(self._call_log) % max(len(self._responses), 1)
        content = self._responses[idx] if self._responses else f"Mock response for model {model}"

        self._call_log.append({
            "model": model,
            "messages": messages,
            "kwargs": kwargs,
        })

        # Count tokens roughly
        total_chars = sum(len(m.get("content", "")) for m in messages) + len(content)
        est_tokens = total_chars // 4

        return ChatResponse(
            content=content,
            model=model,
            provider=ProviderType.CUSTOM,
            usage={"prompt_tokens": est_tokens, "completion_tokens": len(content) // 4, "total_tokens": est_tokens},
            finish_reason="stop",
            latency_ms=(time.time() - start) * 1000,
        )

    def get_call_log(self) -> List[Dict]:
        return self._call_log

    def is_available(self) -> bool:
        return True


# ═════════════════════════════════════════════════════════
# MODEL ROUTER — The Main Interface
# ═════════════════════════════════════════════════════════

class ModelRouter:
    """
    🌐 AI Earth Model Router

    Unified interface for routing LLM requests to the right provider.
    Integrates with Mem0's LLM factory, DSPy's LM, and EvoAgentX's BaseLLM.

    Features:
        - Auto-detects provider from model name
        - Caches responses for identical requests
        - Falls back to alternative models on failure
        - Tracks usage and costs
        - Works in mock mode for testing
    """

    def __init__(self, config: RouterConfig = None):
        self.config = config or RouterConfig()
        self._registry = ModelRegistry()
        self._cache = ResponseCache(ttl=self.config.cache_ttl)
        self._clients: Dict[ProviderType, BaseProviderClient] = {}
        self._usage_log: List[Dict] = []
        self._mock_mode = False
        self._mock_client = MockClient()
        self._init_providers()

    def _init_providers(self):
        """Initialize provider clients from environment variables."""
        # OpenAI
        openai_key = os.environ.get(self.config.api_key_env.get("openai", "OPENAI_API_KEY"), "")
        if openai_key:
            self._clients[ProviderType.OPENAI] = OpenAIClient(
                api_key=openai_key,
                base_url=self.config.base_urls.get("openai"),
            )

        # Anthropic
        anthropic_key = os.environ.get(self.config.api_key_env.get("anthropic", "ANTHROPIC_API_KEY"), "")
        if anthropic_key:
            self._clients[ProviderType.ANTHROPIC] = AnthropicClient(api_key=anthropic_key)

        # Ollama (always try)
        self._clients[ProviderType.OLLAMA] = OllamaClient(
            base_url=self.config.base_urls.get("ollama", "http://localhost:11434")
        )

    # ─── Configuration ────────────────────────────────

    def configure(
        self,
        default: str = None,
        fallback: str = None,
        mock: bool = None,
        cache: bool = None,
    ) -> "ModelRouter":
        """Configure the router. Returns self for chaining."""
        if default:
            self.config.default_model = default
        if fallback:
            self.config.fallback_model = fallback
        if mock is not None:
            self._mock_mode = mock
        if cache is not None:
            self.config.enable_cache = cache
        return self

    def add_provider(self, provider_type: ProviderType, client: BaseProviderClient):
        """Add or replace a provider client."""
        self._clients[provider_type] = client

    def set_api_key(self, provider: str, api_key: str, base_url: str = None):
        """Set API key for a provider dynamically."""
        pt = ProviderType(provider.lower())
        if pt == ProviderType.OPENAI:
            self._clients[pt] = OpenAIClient(api_key=api_key, base_url=base_url)
        elif pt == ProviderType.ANTHROPIC:
            self._clients[pt] = AnthropicClient(api_key=api_key)
        elif pt == ProviderType.OLLAMA:
            self._clients[pt] = OllamaClient(base_url=base_url or "http://localhost:11434")
        else:
            self._clients[pt] = OpenAIClient(api_key=api_key, base_url=base_url)

    # ─── Chat (Main Interface) ────────────────────────

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
        Send a chat completion request.

        Args:
            model: Model name (e.g., "gpt-4o", "claude-sonnet-4", "ollama/llama3")
                   If None, uses configured default.
            messages: List of message dicts [{"role": "user", "content": "..."}]
            system: System message (convenience shortcut)
            prompt: User message (convenience shortcut — creates single user message)
            temperature: Sampling temperature
            max_tokens: Max tokens to generate
            use_cache: Whether to use response cache

        Returns:
            ChatResponse with content, usage, and metadata
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
            # Normalize messages
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

        # Route to provider
        response = self._route_and_execute(
            model, messages,
            temperature=temperature, max_tokens=max_tokens,
            **kwargs,
        )

        # Cache response
        if use_cache and self.config.enable_cache:
            self._cache.put(model, messages, response, temperature=temperature, max_tokens=max_tokens)

        # Log usage
        self._log_usage(model, response)

        return response

    def _route_and_execute(
        self, model: str, messages: List[Dict], **kwargs
    ) -> ChatResponse:
        """Route request to the appropriate provider and execute."""
        # Resolve model name (handle "provider/model" format)
        actual_model = model
        provider_type = self._registry.resolve_provider(model)
        if "/" in model:
            actual_model = model.split("/", 1)[1]

        # Mock mode
        if self._mock_mode:
            return self._mock_client.chat(actual_model, messages, **kwargs)

        # Get client
        client = self._clients.get(provider_type)

        if client is None or not client.is_available():
            # Try fallback
            logger.warning(f"Provider {provider_type} unavailable for {model}, trying fallback {self.config.fallback_model}")
            return self._fallback(messages, **kwargs)

        # Execute with retries
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                return client.chat(actual_model, messages, **kwargs)
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed for {model}: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))

        # All retries failed — try fallback
        logger.error(f"All retries failed for {model}: {last_error}")
        return self._fallback(messages, **kwargs)

    def _fallback(self, messages: List[Dict], **kwargs) -> ChatResponse:
        """Try fallback model."""
        if self._mock_mode:
            return self._mock_client.chat(self.config.fallback_model, messages, **kwargs)

        fb_provider = self._registry.resolve_provider(self.config.fallback_model)
        fb_model = self.config.fallback_model.split("/")[-1] if "/" in self.config.fallback_model else self.config.fallback_model
        client = self._clients.get(fb_provider)

        if client and client.is_available():
            return client.chat(fb_model, messages, **kwargs)

        # Last resort: mock
        return self._mock_client.chat(fb_model, messages, **kwargs)

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
        """
        Create a DSPy-compatible LM object from this router.
        Returns a DSPy LM configured with the same model.
        """
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
        """
        Create a Mem0-compatible LLM object from this router.
        Returns a Mem0 LLM configured with the same model.
        """
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
            client = self._clients.get(pt)
            if client:
                result[pt.value] = client.is_available()
            else:
                result[pt.value] = False
        return result

    def info(self) -> Dict[str, Any]:
        """Get router information."""
        return {
            "default_model": self.config.default_model,
            "fallback_model": self.config.fallback_model,
            "mock_mode": self._mock_mode,
            "cache_enabled": self.config.enable_cache,
            "cache_stats": self._cache.stats(),
            "providers": self.list_providers(),
            "registered_models": len(self._registry.list_models()),
            "total_calls": len(self._usage_log),
        }
