"""
🔑 AI Earth — LLM Key Pool & Real Provider System
═══════════════════════════════════════════════════════════
Smart key rotation with rate limiting, health tracking,
and automatic failover across multiple providers.

Providers:
    - OpenRouter (10 keys) — 200+ models via unified API
    - GitHub Models (1 key) — GPT-4o-mini, etc.
    - Google AI Studio (8 keys) — Gemini (when quota resets)
    - Serper — Web search integration

Architecture:
    KeyPool → rotate keys → pick healthy key → call API → track health
    RateLimiter → per-key cooldown → respect 429 headers → auto-retry
"""

from __future__ import annotations

import os
import time
import json
import random
import logging
import threading
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger("ai_earth.llm_pool")


# ═════════════════════════════════════════════════════════
# Provider Types
# ═════════════════════════════════════════════════════════

class ProviderType(str, Enum):
    OPENROUTER = "openrouter"
    GITHUB = "github"
    GOOGLE = "google"
    SERPER = "serper"
    OLLAMA = "ollama"
    NVIDIA = "nvidia"
    SILICONFLOW = "siliconflow"
    MISTRAL = "mistral"
    CLOUDFLARE = "cloudflare"
    FIRECRAWL = "firecrawl"
    TINKER = "tinker"
    LLM7 = "llm7"


# ═════════════════════════════════════════════════════════
# Key Health Tracking
# ═════════════════════════════════════════════════════════

@dataclass
class KeyHealth:
    """Track health and rate-limit state for a single API key."""
    key_id: str
    api_key: str
    provider: ProviderType
    account: str = ""
    
    # Health state
    healthy: bool = True
    consecutive_failures: int = 0
    last_used: float = 0.0
    last_failed: float = 0.0
    cooldown_until: float = 0.0
    
    # Stats
    total_calls: int = 0
    total_failures: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    
    # Rate limit info from headers
    requests_remaining: Optional[int] = None
    requests_limit: Optional[int] = None
    tokens_remaining: Optional[int] = None
    reset_at: Optional[float] = None

    def is_available(self) -> bool:
        """Check if this key is available for use."""
        if not self.healthy and self.consecutive_failures >= 5:
            return False
        if time.time() < self.cooldown_until:
            return False
        return True

    def record_success(self, tokens: int = 0, cost: float = 0.0):
        """Record a successful API call."""
        self.total_calls += 1
        self.total_tokens += tokens
        self.total_cost_usd += cost
        self.consecutive_failures = 0
        self.healthy = True
        self.last_used = time.time()

    def record_failure(self, status_code: int = 0, retry_after: float = 60.0):
        """Record a failed API call."""
        self.total_calls += 1
        self.total_failures += 1
        self.consecutive_failures += 1
        self.last_failed = time.time()

        if status_code == 429:
            # Rate limited — respect Retry-After or default cooldown
            self.cooldown_until = time.time() + min(retry_after, 120)
            logger.warning(f"Key {self.key_id} rate-limited, cooldown {retry_after:.0f}s")
        elif status_code >= 500:
            # Server error — short cooldown
            self.cooldown_until = time.time() + 5
        elif status_code == 401:
            # Auth failure — mark unhealthy permanently
            self.healthy = False
            logger.error(f"Key {self.key_id} auth failed — marking unhealthy")
        elif self.consecutive_failures >= 5:
            self.healthy = False
            logger.error(f"Key {self.key_id} too many failures — marking unhealthy")

    def update_from_headers(self, headers: Dict):
        """Update rate limit info from response headers."""
        # OpenRouter rate limit headers
        if 'x-ratelimit-remaining' in headers:
            try:
                self.requests_remaining = int(headers['x-ratelimit-remaining'])
            except (ValueError, TypeError):
                pass
        if 'x-ratelimit-limit' in headers:
            try:
                self.requests_limit = int(headers['x-ratelimit-limit'])
            except (ValueError, TypeError):
                pass
        if 'x-ratelimit-reset' in headers:
            try:
                reset_str = headers['x-ratelimit-reset']
                # Could be ISO timestamp or seconds
                self.reset_at = float(reset_str)
            except (ValueError, TypeError):
                pass


# ═════════════════════════════════════════════════════════
# Key Pool — Smart Rotation
# ═════════════════════════════════════════════════════════

class KeyPool:
    """
    Manages a pool of API keys with smart rotation.
    
    Strategy:
        1. Filter to available (healthy + not in cooldown) keys
        2. Prefer key with most remaining requests
        3. Break ties by least recently used
        4. Random jitter to avoid thundering herd
    """

    def __init__(self):
        self._keys: Dict[str, KeyHealth] = {}
        self._by_provider: Dict[ProviderType, List[str]] = defaultdict(list)
        self._lock = threading.Lock()
        self._round_robin_idx: Dict[str, int] = defaultdict(int)

    def add_key(
        self,
        provider: ProviderType,
        api_key: str,
        account: str = "",
        key_id: str = None,
    ) -> str:
        """Register an API key. Returns the key_id."""
        key_id = key_id or f"{provider.value}_{len(self._by_provider[provider])}"
        health = KeyHealth(
            key_id=key_id,
            api_key=api_key,
            provider=provider,
            account=account,
        )
        with self._lock:
            self._keys[key_id] = health
            self._by_provider[provider].append(key_id)
        logger.info(f"Registered key {key_id} for {provider.value} ({account})")
        return key_id

    def get_key(self, provider: ProviderType) -> Optional[KeyHealth]:
        """Get the best available key for a provider."""
        with self._lock:
            available = [
                self._keys[kid]
                for kid in self._by_provider.get(provider, [])
                if self._keys[kid].is_available()
            ]

        if not available:
            # Try to recover keys past cooldown
            now = time.time()
            for kid in self._by_provider.get(provider, []):
                k = self._keys[kid]
                if k.consecutive_failures < 5 and now >= k.cooldown_until:
                    k.healthy = True
                    available.append(k)

        if not available:
            return None

        # Sort by: most remaining requests, then least recently used
        def sort_score(k: KeyHealth) -> Tuple:
            remaining = k.requests_remaining or 9999
            recency = k.last_used
            # Add small random jitter to spread load
            jitter = random.uniform(0, 0.1)
            return (-remaining, recency + jitter)

        available.sort(key=sort_score)
        return available[0]

    def get_any_key(self) -> Optional[KeyHealth]:
        """Get best available key from any provider (priority: openrouter > github > google)."""
        for provider in [ProviderType.OPENROUTER, ProviderType.GITHUB, ProviderType.GOOGLE]:
            key = self.get_key(provider)
            if key:
                return key
        return None

    def report_success(self, key_id: str, tokens: int = 0, cost: float = 0.0):
        """Report a successful call."""
        with self._lock:
            if key_id in self._keys:
                self._keys[key_id].record_success(tokens, cost)

    def report_failure(self, key_id: str, status_code: int = 0, retry_after: float = 60.0):
        """Report a failed call."""
        with self._lock:
            if key_id in self._keys:
                self._keys[key_id].record_failure(status_code, retry_after)

    def update_headers(self, key_id: str, headers: Dict):
        """Update rate limit info from response headers."""
        with self._lock:
            if key_id in self._keys:
                self._keys[key_id].update_from_headers(headers)

    def stats(self) -> Dict[str, Any]:
        """Get pool statistics."""
        with self._lock:
            total_calls = sum(k.total_calls for k in self._keys.values())
            total_failures = sum(k.total_failures for k in self._keys.values())
            total_cost = sum(k.total_cost_usd for k in self._keys.values())
            healthy = sum(1 for k in self._keys.values() if k.is_available())
            
            by_provider = {}
            for pt, kids in self._by_provider.items():
                pk = [self._keys[kid] for kid in kids]
                by_provider[pt.value] = {
                    "total_keys": len(pk),
                    "available": sum(1 for k in pk if k.is_available()),
                    "total_calls": sum(k.total_calls for k in pk),
                    "total_cost": round(sum(k.total_cost_usd for k in pk), 6),
                }
            
            return {
                "total_keys": len(self._keys),
                "available_keys": healthy,
                "total_calls": total_calls,
                "total_failures": total_failures,
                "total_cost_usd": round(total_cost, 6),
                "success_rate": round((total_calls - total_failures) / max(total_calls, 1), 3),
                "by_provider": by_provider,
            }

    def health_report(self) -> List[Dict]:
        """Get detailed health report for all keys."""
        with self._lock:
            return [
                {
                    "key_id": k.key_id,
                    "provider": k.provider.value,
                    "account": k.account,
                    "healthy": k.healthy,
                    "available": k.is_available(),
                    "calls": k.total_calls,
                    "failures": k.total_failures,
                    "cost": round(k.total_cost_usd, 6),
                    "cooldown_remaining": max(0, k.cooldown_until - time.time()),
                    "requests_remaining": k.requests_remaining,
                }
                for k in self._keys.values()
            ]


# ═════════════════════════════════════════════════════════

# ═════════════════════════════════════════════════════════
# Global Key Pool — Loads keys from .env file
# ═════════════════════════════════════════════════════════

_global_pool: Optional[KeyPool] = None


def _load_env_file() -> Dict[str, str]:
    """Load environment variables from .env file."""
    env_vars = {}
    
    # Try multiple .env locations
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'),
        os.path.join(os.getcwd(), '.env'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),
    ]
    
    for env_path in candidates:
        env_path = os.path.normpath(env_path)
        if os.path.exists(env_path):
            logger.info(f"Loading API keys from {env_path}")
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, _, value = line.partition('=')
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if value and value != f"{key.lower()}-your-key-here":
                            env_vars[key] = value
            break
    else:
        logger.warning("No .env file found — checking environment variables")
    
    # Also check actual environment variables (override .env)
    for key, value in os.environ.items():
        if key.startswith(('OPENROUTER_KEY_', 'GOOGLE_KEY_', 'GITHUB_MODELS_KEY', 'SERPER_KEY')):
            env_vars[key] = value
    
    return env_vars


def get_key_pool() -> KeyPool:
    """Get the global key pool, initializing from .env if needed."""
    global _global_pool
    if _global_pool is not None:
        return _global_pool

    pool = KeyPool()
    env = _load_env_file()

    # ─── OpenRouter Keys ────────────────────────────────
    accounts_str = env.get('OPENROUTER_ACCOUNTS', '')
    accounts = [a.strip() for a in accounts_str.split(',') if a.strip()]
    
    or_idx = 0
    while True:
        or_idx += 1
        key_val = env.get(f'OPENROUTER_KEY_{or_idx}')
        if not key_val:
            break
        account = accounts[or_idx - 1] if or_idx - 1 < len(accounts) else f"account_{or_idx}"
        pool.add_key(ProviderType.OPENROUTER, key_val, account=account)

    # ─── GitHub Models Key ──────────────────────────────
    github_key = env.get('GITHUB_MODELS_KEY', '')
    if github_key:
        github_account = env.get('GITHUB_MODELS_ACCOUNT', 'github')
        pool.add_key(ProviderType.GITHUB, github_key, account=github_account)

    # ─── Google AI Studio Keys ──────────────────────────
    google_accounts_str = env.get('GOOGLE_ACCOUNTS', '')
    google_accounts = [a.strip() for a in google_accounts_str.split(',') if a.strip()]
    
    g_idx = 0
    while True:
        g_idx += 1
        key_val = env.get(f'GOOGLE_KEY_{g_idx}')
        if not key_val:
            break
        account = google_accounts[g_idx - 1] if g_idx - 1 < len(google_accounts) else f"gaccount_{g_idx}"
        pool.add_key(ProviderType.GOOGLE, key_val, account=account)

    # ─── New Providers ──────────────────────────────────
    
    # Nvidia NIM
    nvidia_key = env.get('NVIDIA_NIM_KEY')
    if nvidia_key:
        pool.add_key(ProviderType.NVIDIA, nvidia_key, account="nvidia_main")

    # Silicon Flow
    sf_key = env.get('SILICON_FLOW_KEY')
    if sf_key:
        pool.add_key(ProviderType.SILICONFLOW, sf_key, account="sf_main")

    # Mistral
    mistral_key = env.get('MISTRAL_KEY')
    if mistral_key:
        pool.add_key(ProviderType.MISTRAL, mistral_key, account="mistral_main")

    # Cloudflare
    cf_token = env.get('CLOUDFLARE_TOKEN')
    if cf_token:
        pool.add_key(ProviderType.CLOUDFLARE, cf_token, account="cloudflare_main")

    # Firecrawl
    fc_key = env.get('FIRECRAWL_KEY')
    if fc_key:
        pool.add_key(ProviderType.FIRECRAWL, fc_key, account="firecrawl_main")

    # Tinker
    tink_key = env.get('TINKER_KEY')
    if tink_key:
        pool.add_key(ProviderType.TINKER, tink_key, account="tink_main")

    # LLM7
    llm7_key = env.get('LLM7_KEY')
    if llm7_key:
        pool.add_key(ProviderType.LLM7, llm7_key, account="llm7_main")

    logger.info(
        f"Key Pool initialized: "
        f"{len(pool._by_provider.get(ProviderType.OPENROUTER, []))} OpenRouter, "
        f"{len(pool._by_provider.get(ProviderType.GITHUB, []))} GitHub, "
        f"{len(pool._by_provider.get(ProviderType.GOOGLE, []))} Google keys"
    )

    _global_pool = pool
    return pool


def reset_pool():
    """Reset the global pool (for testing)."""
    global _global_pool
    _global_pool = None

# Real API Callers
# ═════════════════════════════════════════════════════════

def _call_openrouter(
    api_key: str,
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4096,
    **kwargs,
) -> Tuple[Dict, int, Dict]:
    """
    Call OpenRouter API. Returns (response_data, status_code, headers).
    OpenRouter is OpenAI-compatible.
    """
    import requests as req

    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if kwargs.get("tools"):
        payload["tools"] = kwargs["tools"]
    if kwargs.get("response_format"):
        payload["response_format"] = kwargs["response_format"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/faresrafat3/ai-earth",
        "X-Title": "AI Earth Platform",
    }

    resp = req.post(url, headers=headers, json=payload, timeout=60)
    return resp.json(), resp.status_code, dict(resp.headers)


def _call_github_models(
    api_key: str,
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4096,
    **kwargs,
) -> Tuple[Dict, int, Dict]:
    """
    Call GitHub Models API. OpenAI-compatible via Azure inference.
    """
    import requests as req

    url = "https://models.inference.ai.azure.com/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    resp = req.post(url, headers=headers, json=payload, timeout=60)
    return resp.json(), resp.status_code, dict(resp.headers)


def _call_google(
    api_key: str,
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4096,
    **kwargs,
) -> Tuple[Dict, int, Dict]:
    """
    Call Google AI Studio (Gemini) API.
    """
    import requests as req

    # Convert OpenAI-style messages to Gemini format
    contents = []
    for msg in messages:
        role = "user" if msg["role"] in ("user", "system") else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    # Ensure first message is from user
    if contents and contents[0]["role"] != "user":
        contents.insert(0, {"role": "user", "parts": [{"text": "."}]})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        }
    }

    headers = {"Content-Type": "application/json"}
    resp = req.post(url, headers=headers, json=payload, timeout=60)
    return resp.json(), resp.status_code, dict(resp.headers)


def _call_nvidia(
    api_key: str,
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4096,
    **kwargs,
) -> Tuple[Dict, int, Dict]:
    """Call Nvidia NIM API (OpenAI-compatible)."""
    import requests as req
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = req.post(url, headers=headers, json=payload, timeout=60)
    return resp.json(), resp.status_code, dict(resp.headers)


def _call_siliconflow(
    api_key: str,
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4096,
    **kwargs,
) -> Tuple[Dict, int, Dict]:
    """Call Silicon Flow API (OpenAI-compatible)."""
    import requests as req
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = req.post(url, headers=headers, json=payload, timeout=60)
    return resp.json(), resp.status_code, dict(resp.headers)


def _call_mistral(
    api_key: str,
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4096,
    **kwargs,
) -> Tuple[Dict, int, Dict]:
    """Call Mistral API (OpenAI-compatible)."""
    import requests as req
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = req.post(url, headers=headers, json=payload, timeout=60)
    return resp.json(), resp.status_code, dict(resp.headers)


def _call_llm7(
    api_key: str,
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4096,
    **kwargs,
) -> Tuple[Dict, int, Dict]:
    """Call LLM7.io API."""
    import requests as req
    # LLM7 uses a different structure usually, but let's assume OpenAI-compatible for now
    # If it fails, we'll refine.
    url = "https://api.llm7.io/v1/chat/completions"
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = req.post(url, headers=headers, json=payload, timeout=60)
    return resp.json(), resp.status_code, dict(resp.headers)


def call_llm(
    model: str,
    messages: List[Dict],
    temperature: float = 0.7,
    max_tokens: int = 4096,
    preferred_provider: ProviderType = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Make a real LLM API call with automatic key rotation and failover.
    
    Returns a normalized response dict:
        {
            "content": str,
            "model": str,
            "provider": str,
            "usage": {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int},
            "finish_reason": str,
            "latency_ms": float,
            "cost_usd": float,
            "key_id": str,
            "cached": False,
        }
    """
    pool = get_key_pool()
    start_time = time.time()

    # Determine provider from model name
    provider = preferred_provider or _resolve_provider(model)

    # Map model names for different providers
    actual_model = _map_model(model, provider)

    # Try preferred provider first, then fallback chain
    provider_chain = _get_provider_chain(provider)

    for prov in provider_chain:
        key = pool.get_key(prov)
        if key is None:
            continue

        try:
            provider_model = _map_model(model, prov)

            if prov == ProviderType.OPENROUTER:
                data, status, resp_headers = _call_openrouter(
                    key.api_key, provider_model, messages,
                    temperature=temperature, max_tokens=max_tokens, **kwargs,
                )
            elif prov == ProviderType.GITHUB:
                data, status, resp_headers = _call_github_models(
                    key.api_key, provider_model, messages,
                    temperature=temperature, max_tokens=max_tokens, **kwargs,
                )
            elif prov == ProviderType.GOOGLE:
                data, status, resp_headers = _call_google(
                    key.api_key, provider_model, messages,
                    temperature=temperature, max_tokens=max_tokens, **kwargs,
                )
            elif prov == ProviderType.NVIDIA:
                data, status, resp_headers = _call_nvidia(
                    key.api_key, provider_model, messages,
                    temperature=temperature, max_tokens=max_tokens, **kwargs,
                )
            elif prov == ProviderType.SILICONFLOW:
                data, status, resp_headers = _call_siliconflow(
                    key.api_key, provider_model, messages,
                    temperature=temperature, max_tokens=max_tokens, **kwargs,
                )
            elif prov == ProviderType.MISTRAL:
                data, status, resp_headers = _call_mistral(
                    key.api_key, provider_model, messages,
                    temperature=temperature, max_tokens=max_tokens, **kwargs,
                )
            elif prov == ProviderType.LLM7:
                data, status, resp_headers = _call_llm7(
                    key.api_key, provider_model, messages,
                    temperature=temperature, max_tokens=max_tokens, **kwargs,
                )
            else:
                continue

            # Update rate limit info from headers
            pool.update_headers(key.key_id, resp_headers)

            if status == 200:
                # Parse response
                result = _parse_response(data, prov, provider_model, start_time)
                result["key_id"] = key.key_id
                pool.report_success(key.key_id, tokens=result["usage"]["total_tokens"], cost=result["cost_usd"])
                return result
            elif status == 429:
                # Rate limited — get retry-after
                retry_after = 60.0
                if 'retry-after' in resp_headers:
                    try:
                        retry_after = float(resp_headers['retry-after'])
                    except (ValueError, TypeError):
                        pass
                pool.report_failure(key.key_id, status_code=429, retry_after=retry_after)
                logger.warning(f"Key {key.key_id} rate limited, trying next")
                continue
            else:
                retry_after = float(resp_headers.get('retry-after', 30))
                pool.report_failure(key.key_id, status_code=status, retry_after=retry_after)
                logger.warning(f"Key {key.key_id} got status {status}: {str(data)[:100]}")
                continue

        except Exception as e:
            pool.report_failure(key.key_id)
            logger.warning(f"Key {key.key_id} error: {e}")
            continue

    # All providers failed
    raise RuntimeError(
        f"All LLM providers failed for model={model}. "
        f"Pool stats: {pool.stats()}"
    )


def _resolve_provider(model: str) -> ProviderType:
    """Guess the best provider for a model name."""
    model_lower = model.lower()

    # Check for explicit prefix
    if model_lower.startswith("github/"):
        return ProviderType.GITHUB
    if model_lower.startswith("google/"):
        return ProviderType.GOOGLE
    if model_lower.startswith("nvidia/"):
        return ProviderType.NVIDIA
    if model_lower.startswith("mistral/"):
        return ProviderType.MISTRAL
    if model_lower.startswith("sf/"):
        return ProviderType.SILICONFLOW
    if model_lower.startswith("llm7/"):
        return ProviderType.LLM7
    if model_lower.startswith("ollama/"):
        return ProviderType.OLLAMA

    # Google models
    if "gemini" in model_lower:
        return ProviderType.OPENROUTER  # OpenRouter supports Gemini

    # Mistral models
    if "mistral" in model_lower or "mixtral" in model_lower:
        return ProviderType.MISTRAL

    # Everything else goes through OpenRouter
    return ProviderType.OPENROUTER


def _get_provider_chain(primary: ProviderType) -> List[ProviderType]:
    """Get the fallback chain for a provider."""
    chains = {
        ProviderType.OPENROUTER: [ProviderType.OPENROUTER, ProviderType.GITHUB, ProviderType.GOOGLE, ProviderType.NVIDIA, ProviderType.SILICONFLOW, ProviderType.MISTRAL],
        ProviderType.GITHUB: [ProviderType.GITHUB, ProviderType.OPENROUTER, ProviderType.GOOGLE],
        ProviderType.GOOGLE: [ProviderType.GOOGLE, ProviderType.OPENROUTER, ProviderType.GITHUB],
        ProviderType.NVIDIA: [ProviderType.NVIDIA, ProviderType.OPENROUTER, ProviderType.GITHUB],
        ProviderType.SILICONFLOW: [ProviderType.SILICONFLOW, ProviderType.OPENROUTER, ProviderType.GITHUB],
        ProviderType.MISTRAL: [ProviderType.MISTRAL, ProviderType.OPENROUTER, ProviderType.GITHUB],
        ProviderType.LLM7: [ProviderType.LLM7, ProviderType.OPENROUTER, ProviderType.GITHUB],
        ProviderType.OLLAMA: [ProviderType.OLLAMA],
        ProviderType.SERPER: [ProviderType.SERPER],
    }
    return chains.get(primary, [ProviderType.OPENROUTER, ProviderType.GITHUB])


def _map_model(model: str, provider: ProviderType) -> str:
    """Map model name to provider-specific format."""
    # Remove provider prefix if present
    clean = model.split("/", 1)[-1] if "/" in model else model

    if provider == ProviderType.OPENROUTER:
        # OpenRouter uses "org/model" format
        mapping = {
            "gpt-4o": "openai/gpt-4o",
            "gpt-4o-mini": "openai/gpt-4o-mini",
            "gpt-4-turbo": "openai/gpt-4-turbo",
            "o1": "openai/o1",
            "o1-mini": "openai/o1-mini",
            "o3": "openai/o3",
            "o3-mini": "openai/o3-mini",
            "claude-sonnet-4-20250514": "anthropic/claude-sonnet-4-20250514",
            "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
            "claude-3.5-haiku": "anthropic/claude-3.5-haiku",
            "gemini-2.5-pro": "google/gemini-2.5-pro-preview",
            "gemini-2.5-flash": "google/gemini-2.5-flash-preview",
            "gemini-2.0-flash": "google/gemini-2.0-flash-001",
            "llama3": "meta-llama/llama-3-8b-instruct",
            "llama3.1": "meta-llama/llama-3.1-8b-instruct",
            "deepseek-chat": "deepseek/deepseek-chat",
            "deepseek-reasoner": "deepseek/deepseek-r1",
            "qwen2.5": "qwen/qwen-2.5-7b-instruct",
        }
        return mapping.get(clean, clean)  # fallback to original if not in mapping

    elif provider == ProviderType.GITHUB:
        # GitHub Models uses plain model names
        github_models = {
            "gpt-4o": "gpt-4o",
            "gpt-4o-mini": "gpt-4o-mini",
            "gpt-4-turbo": "gpt-4-turbo",
            "claude-3.5-sonnet": "claude-3.5-sonnet",
        }
        return github_models.get(clean, "gpt-4o-mini")

    elif provider == ProviderType.GOOGLE:
        # Google AI Studio model names
        google_models = {
            "gemini-2.5-pro": "gemini-2.5-pro-preview-06-05",
            "gemini-2.5-flash": "gemini-2.5-flash-preview-05-20",
            "gemini-2.0-flash": "gemini-2.0-flash",
        }
        return google_models.get(clean, "gemini-2.0-flash")

    return clean


def _parse_response(data: Dict, provider: ProviderType, model: str, start_time: float) -> Dict:
    """Parse API response into normalized format."""
    latency = (time.time() - start_time) * 1000

    if provider in (ProviderType.OPENROUTER, ProviderType.GITHUB):
        choice = data.get("choices", [{}])[0]
        usage = data.get("usage", {})
        cost = float(usage.get("cost", 0)) if usage.get("cost") else 0.0
        # Estimate cost if not provided
        if cost == 0:
            prompt_t = usage.get("prompt_tokens", 0)
            comp_t = usage.get("completion_tokens", 0)
            cost = (prompt_t * 0.00015 + comp_t * 0.0006) / 1000  # gpt-4o-mini pricing

        return {
            "content": choice.get("message", {}).get("content", ""),
            "model": data.get("model", model),
            "provider": provider.value,
            "usage": {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            "finish_reason": choice.get("finish_reason", "stop"),
            "latency_ms": round(latency, 1),
            "cost_usd": round(cost, 8),
            "raw": data,
        }

    elif provider == ProviderType.GOOGLE:
        candidates = data.get("candidates", [{}])
        content = ""
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            content = "".join(p.get("text", "") for p in parts)

        usage_meta = data.get("usageMetadata", {})
        return {
            "content": content,
            "model": model,
            "provider": provider.value,
            "usage": {
                "prompt_tokens": usage_meta.get("promptTokenCount", 0),
                "completion_tokens": usage_meta.get("candidatesTokenCount", 0),
                "total_tokens": usage_meta.get("totalTokenCount", 0),
            },
            "finish_reason": candidates[0].get("finishReason", "stop") if candidates else "stop",
            "latency_ms": round(latency, 1),
            "cost_usd": 0.0,  # Free tier
            "raw": data,
        }

    return {
        "content": str(data),
        "model": model,
        "provider": provider.value,
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "finish_reason": "stop",
        "latency_ms": round(latency, 1),
        "cost_usd": 0.0,
        "raw": data,
    }


# ═════════════════════════════════════════════════════════
# Web Search & Crawling Tools
# ═════════════════════════════════════════════════════════

SERPER_KEY = os.environ.get("SERPER_KEY", "") or _load_env_file().get("SERPER_KEY", "")
FIRECRAWL_KEY = os.environ.get("FIRECRAWL_KEY", "") or _load_env_file().get("FIRECRAWL_KEY", "")


def web_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web using Serper API.
    Returns list of {title, link, snippet}.
    """
    import requests as req

    resp = req.post(
        "https://google.serper.dev/search",
        headers={
            "X-API-KEY": SERPER_KEY,
            "Content-Type": "application/json",
        },
        json={"q": query, "num": num_results},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("organic", []):
        results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })
    return results


def crawl_url(url: str) -> str:
    """
    Crawl a URL using Firecrawl API.
    Returns the markdown content.
    """
    import requests as req
    
    if not FIRECRAWL_KEY:
        return "Firecrawl API key not configured."

    headers = {
        "Authorization": f"Bearer {FIRECRAWL_KEY}",
        "Content-Type": "application/json"
    }
    
    # Try Firecrawl scrape endpoint
    try:
        resp = req.post(
            "https://api.firecrawl.dev/v1/scrape",
            headers=headers,
            json={"url": url, "formats": ["markdown"]},
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            return data.get("data", {}).get("markdown", "")
        return f"Firecrawl error: {data.get('error')}"
    except Exception as e:
        return f"Crawl failed: {str(e)}"


# ═════════════════════════════════════════════════════════
# Default Model Configuration
# ═════════════════════════════════════════════════════════

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_PROVIDER = ProviderType.OPENROUTER
FALLBACK_MODEL = "gpt-4o-mini"
FALLBACK_PROVIDER = ProviderType.GITHUB

# Budget-friendly models for different use cases
CHEAP_MODELS = {
    "fast": "openai/gpt-4o-mini",      # Fast & cheap
    "smart": "anthropic/claude-3.5-sonnet",  # Smart but more expensive
    "free": "google/gemini-2.0-flash-001",   # Free via OpenRouter
    "reasoning": "deepseek/deepseek-r1",     # Reasoning
}
