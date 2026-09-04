"""
🔑 AI Earth — LLM Key Pool v2.6 (The Silent Guard)
═══════════════════════════════════════════════════════════
Smart key rotation with rate limiting, health tracking, and automatic failover.
21 API keys across 3 providers + 1 web search key.

Strategy: OpenRouter primary (11 keys) → GitHub fallback (1 key) → Google reserve (9 keys)
All keys loaded from .env — zero hardcoded secrets.
"""
from __future__ import annotations
import os, time, json, random, logging, threading, requests
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger("ai_earth.llm_pool")

# ═════════════════════════════════════════════════════════
# 🛡️ Anti-Hang Guards (configurable via .env)
# ═════════════════════════════════════════════════════════
# HTTP_TIMEOUT: hard cap on every HTTP request (seconds)
# MAX_ATTEMPTS: hard cap on total attempts per call_llm()
# MAX_CALLS_PER_RUN: budget guard — protects rate limits from
#                    runaway loops (tests, evolution cycles)

def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name) or _load_env().get(name) or default)
    except (ValueError, TypeError):
        return default

_HTTP_TIMEOUT: int = 30       # resolved lazily after _load_env defined
_MAX_ATTEMPTS: int = 4
_MAX_CALLS_PER_RUN: int = 200
_GUARDS_LOADED: bool = False
_run_call_count: int = 0
_guard_lock = threading.Lock()

def _load_guards():
    """Load guard values from env once (lazy — after _load_env exists)."""
    global _HTTP_TIMEOUT, _MAX_ATTEMPTS, _MAX_CALLS_PER_RUN, _GUARDS_LOADED
    if _GUARDS_LOADED:
        return
    _HTTP_TIMEOUT = _env_int("AI_EARTH_HTTP_TIMEOUT", 30)
    _MAX_ATTEMPTS = _env_int("AI_EARTH_MAX_ATTEMPTS", 4)
    _MAX_CALLS_PER_RUN = _env_int("AI_EARTH_MAX_CALLS_PER_RUN", 200)
    _GUARDS_LOADED = True

def _check_call_budget():
    """Raise fast if this process exceeded its LLM call budget."""
    global _run_call_count
    _load_guards()
    with _guard_lock:
        _run_call_count += 1
        if _run_call_count > _MAX_CALLS_PER_RUN:
            raise RuntimeError(
                f"LLM call budget exceeded ({_MAX_CALLS_PER_RUN} calls/run). "
                f"Raise AI_EARTH_MAX_CALLS_PER_RUN in .env if intentional."
            )

def calls_this_run() -> int:
    return _run_call_count

def _http_timeout() -> int:
    _load_guards()
    return _HTTP_TIMEOUT

# ─── Persistent daily quota ledger (survives sessions) ────
# The ledger must NEVER break LLM calls with its own errors,
# so every touch is wrapped. See ai_earth/core/quota_ledger.py

def _ledger_ok(provider: str) -> bool:
    """Pre-flight: does this provider still have daily budget?"""
    try:
        from ai_earth.core.quota_ledger import get_ledger
        return get_ledger().allowed(provider)
    except Exception:
        return True  # fail-open: ledger problems must not block calls

def _ledger_rec(provider: str, tokens: int = 0, cost: float = 0.0, success: bool = True):
    """Post-flight: record the attempt (counts even on failure)."""
    try:
        from ai_earth.core.quota_ledger import get_ledger
        get_ledger().record(provider, tokens=tokens, cost_usd=cost, success=success)
    except Exception:
        pass

# ═════════════════════════════════════════════════════════
# Provider Types
# ═════════════════════════════════════════════════════════

class ProviderType:
    OPENROUTER = "openrouter"
    GITHUB = "github"
    GOOGLE = "google"
    SILICONFLOW = "siliconflow"
    NVIDIA = "nvidia"

# ═════════════════════════════════════════════════════════
# Key Health
# ═════════════════════════════════════════════════════════

@dataclass
class KeyHealth:
    key_id: str
    api_key: str
    provider: str
    account: str = ""
    healthy: bool = True
    consecutive_failures: int = 0
    last_used: float = 0.0
    cooldown_until: float = 0.0
    total_calls: int = 0
    total_failures: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    requests_remaining: Optional[int] = None

    def is_available(self) -> bool:
        if not self.healthy and self.consecutive_failures >= 5:
            return False
        if time.time() < self.cooldown_until:
            return False
        return True

    def record_success(self, tokens: int = 0, cost: float = 0.0):
        self.total_calls += 1
        self.total_tokens += tokens
        self.total_cost_usd += cost
        self.consecutive_failures = 0
        self.healthy = True
        self.last_used = time.time()

    def record_failure(self, status_code: int = 0, retry_after: float = 60.0):
        self.total_calls += 1
        self.total_failures += 1
        self.consecutive_failures += 1
        if status_code == 429:
            self.cooldown_until = time.time() + min(retry_after, 120)
        elif status_code == 402:
            # Out of credit / payment required — this key can't do paid calls.
            # Long cooldown (1h) so the pool skips it and fails over fast
            # instead of wasting attempts. Doesn't kill the key (credit may
            # be topped up), just deprioritizes it.
            self.cooldown_until = time.time() + 3600
        elif status_code >= 500:
            self.cooldown_until = time.time() + 5
        elif status_code == 401:
            self.healthy = False
        elif self.consecutive_failures >= 5:
            self.healthy = False

# ═════════════════════════════════════════════════════════
# Key Pool
# ═════════════════════════════════════════════════════════

class KeyPool:
    def __init__(self):
        self._keys: Dict[str, KeyHealth] = {}
        self._by_provider: Dict[str, List[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def add_key(self, provider: str, api_key: str, account: str = "", key_id: str = None) -> str:
        key_id = key_id or f"{provider}_{len(self._by_provider[provider])}"
        health = KeyHealth(key_id=key_id, api_key=api_key, provider=provider, account=account)
        with self._lock:
            self._keys[key_id] = health
            self._by_provider[provider].append(key_id)
        logger.info(f"Registered key {key_id} for {provider} ({account})")
        return key_id

    def get_key(self, provider: str) -> Optional[KeyHealth]:
        with self._lock:
            available = [self._keys[kid] for kid in self._by_provider.get(provider, []) if self._keys[kid].is_available()]
            if not available:
                now = time.time()
                for kid in self._by_provider.get(provider, []):
                    k = self._keys[kid]
                    if k.consecutive_failures < 5 and now >= k.cooldown_until:
                        k.healthy = True
                        available.append(k)
            if not available:
                return None
            available.sort(key=lambda k: (-(k.requests_remaining or 9999), k.last_used + random.uniform(0, 0.1)))
            return available[0]

    def get_any_key(self) -> Optional[KeyHealth]:
        for prov in ["openrouter", "github", "google"]:
            key = self.get_key(prov)
            if key:
                return key
        return None

    def report_success(self, key_id: str, tokens: int = 0, cost: float = 0.0):
        with self._lock:
            if key_id in self._keys:
                self._keys[key_id].record_success(tokens, cost)

    def report_failure(self, key_id: str, status_code: int = 0, retry_after: float = 60.0):
        with self._lock:
            if key_id in self._keys:
                self._keys[key_id].record_failure(status_code, retry_after)

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            total_calls = sum(k.total_calls for k in self._keys.values())
            total_failures = sum(k.total_failures for k in self._keys.values())
            total_cost = sum(k.total_cost_usd for k in self._keys.values())
            healthy = sum(1 for k in self._keys.values() if k.is_available())
            by_provider = {}
            for pt, kids in self._by_provider.items():
                pk = [self._keys[kid] for kid in kids]
                by_provider[pt] = {
                    "total_keys": len(pk), "available": sum(1 for k in pk if k.is_available()),
                    "total_calls": sum(k.total_calls for k in pk),
                    "total_cost": round(sum(k.total_cost_usd for k in pk), 6),
                }
            return {
                "total_keys": len(self._keys), "available_keys": healthy,
                "total_calls": total_calls, "total_failures": total_failures,
                "total_cost_usd": round(total_cost, 6),
                "success_rate": round((total_calls - total_failures) / max(total_calls, 1), 3),
                "by_provider": by_provider,
            }

    def health_report(self) -> List[Dict]:
        with self._lock:
            return [{
                "key_id": k.key_id, "provider": k.provider, "account": k.account,
                "healthy": k.healthy, "available": k.is_available(),
                "calls": k.total_calls, "failures": k.total_failures,
                "cost": round(k.total_cost_usd, 6),
                "cooldown_remaining": max(0, k.cooldown_until - time.time()),
                "requests_remaining": k.requests_remaining,
            } for k in self._keys.values()]

# ═════════════════════════════════════════════════════════
# Load Keys from .env
# ═════════════════════════════════════════════════════════

def _load_env() -> Dict[str, str]:
    env = {}
    # Try multiple paths
    for p in ["/home/user/ai-earth/.env", "/home/user/.env", ".env"]:
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
            break
    return env

_global_pool: Optional[KeyPool] = None

def get_key_pool() -> KeyPool:
    global _global_pool
    if _global_pool is not None:
        return _global_pool

    pool = KeyPool()
    env = _load_env()

    # OpenRouter keys
    accounts_str = env.get("OPENROUTER_ACCOUNTS", "")
    accounts = [a.strip() for a in accounts_str.split(",") if a.strip()]
    for i, acct in enumerate(accounts):
        key = env.get(f"OPENROUTER_KEY_{i+1}")
        if key:
            pool.add_key("openrouter", key, account=acct)

    # GitHub Models
    gh_key = env.get("GITHUB_MODELS_KEY")
    gh_acct = env.get("GITHUB_MODELS_ACCOUNT", "faresrafat3")
    if gh_key:
        pool.add_key("github", gh_key, account=gh_acct)

    # Google keys
    google_accts = env.get("GOOGLE_ACCOUNTS", "")
    g_accounts = [a.strip() for a in google_accts.split(",") if a.strip()]
    for i, acct in enumerate(g_accounts):
        key = env.get(f"GOOGLE_KEY_{i+1}")
        if key:
            pool.add_key("google", key, account=acct)

    _global_pool = pool
    logger.info(f"Key Pool initialized: {pool.stats()}")
    return pool

def reset_pool():
    global _global_pool
    _global_pool = None

# ═════════════════════════════════════════════════════════
# Model Name Mapping
# ═════════════════════════════════════════════════════════

_MODEL_MAP = {
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

def _resolve_model(model: str, provider: str) -> str:
    """Map short model name to provider-specific format."""
    clean = model.split("/")[-1] if "/" in model else model
    if provider == "openrouter":
        # Already in OpenRouter "org/model" form (e.g. "deepseek/deepseek-chat-v3:free",
        # "openai/gpt-4o-mini") → pass through UNCHANGED. Only bare aliases get mapped.
        if "/" in model:
            return model
        return _MODEL_MAP.get(model, model)
    elif provider == "github":
        # GitHub uses plain names
        return clean
    elif provider == "google":
        google_map = {
            "gemini-2.5-pro": "gemini-2.5-pro-preview-06-05",
            "gemini-2.5-flash": "gemini-2.5-flash-preview-05-20",
            "gemini-2.0-flash": "gemini-2.0-flash",
        }
        return google_map.get(clean, "gemini-2.0-flash")
    return clean

# ═════════════════════════════════════════════════════════
# Core LLM Call with Smart Rotation
# ═════════════════════════════════════════════════════════

def call_llm(model: str, messages: List[Dict], temperature: float = 0.7,
             max_tokens: int = 4096, **kwargs) -> Dict[str, Any]:
    """
    Make a real LLM call with automatic key rotation and failover.
    
    Fallback chain: OpenRouter (11 keys) → GitHub (1 key) → Google (9 keys)
    Rate limits respected with cooldown, then next key tried.
    """
    pool = get_key_pool()
    start = time.time()
    _check_call_budget()  # 🛡️ budget guard — fail fast, never loop forever

    # Determine preferred provider from model name
    if any(g in model.lower() for g in ["gemini", "google/"]):
        providers = ["google", "openrouter", "github"]
    elif any(g in model.lower() for g in ["github/"]):
        providers = ["github", "openrouter", "google"]
    else:
        providers = ["openrouter", "github", "google"]

    attempts = 0
    tried_keys: set = set()
    for prov in providers:
        # 📒 Ledger pre-flight: skip provider whose DAILY cap is spent
        # (zero HTTP, zero waiting — fail-fast across sessions)
        if not _ledger_ok(prov):
            logger.warning(f"Provider {prov} daily quota exhausted (ledger) — skipped pre-flight")
            continue
        # Try up to 2 different keys per provider (bounded, never infinite)
        for _ in range(2):
            if attempts >= _MAX_ATTEMPTS:
                break
            key = pool.get_key(prov)
            if key is None or key.key_id in tried_keys:
                break
            tried_keys.add(key.key_id)
            attempts += 1

            provider_model = _resolve_model(model, prov)

            try:
                if prov == "openrouter":
                    data, status, headers = _call_openrouter(key.api_key, provider_model, messages, temperature, max_tokens, **kwargs)
                elif prov == "github":
                    data, status, headers = _call_github(key.api_key, provider_model, messages, temperature, max_tokens, **kwargs)
                elif prov == "google":
                    data, status, headers = _call_google(key.api_key, provider_model, messages, temperature, max_tokens, **kwargs)
                else:
                    break

                # Update rate limit headers
                if 'x-ratelimit-remaining' in headers:
                    try:
                        key.requests_remaining = int(headers['x-ratelimit-remaining'])
                    except (ValueError, TypeError):
                        pass

                if status == 200:
                    result = _parse_response(data, prov, provider_model, start)
                    pool.report_success(key.key_id, tokens=result["usage"]["total_tokens"], cost=result["cost_usd"])
                    _ledger_rec(prov, tokens=result["usage"]["total_tokens"], cost=result["cost_usd"], success=True)
                    return result
                elif status == 429:
                    retry_after = float(headers.get('retry-after', 60))
                    pool.report_failure(key.key_id, status_code=429, retry_after=retry_after)
                    _ledger_rec(prov, success=False)
                    logger.warning(f"Key {key.key_id} rate-limited ({retry_after}s), trying next")
                    continue
                else:
                    retry_after = float(headers.get('retry-after', 30))
                    pool.report_failure(key.key_id, status_code=status, retry_after=retry_after)
                    _ledger_rec(prov, success=False)
                    logger.warning(f"Key {key.key_id} status {status}: {str(data)[:100]}")
                    continue
            except Exception as e:
                pool.report_failure(key.key_id)
                _ledger_rec(prov, success=False)
                logger.warning(f"Key {key.key_id} error: {e}")
                continue
        if attempts >= _MAX_ATTEMPTS:
            break

    # All providers exhausted (bounded by _MAX_ATTEMPTS — never infinite)
    raise RuntimeError(
        f"All LLM providers failed for model={model} after {attempts} attempts. "
        f"Pool stats: {pool.stats()}"
    )

# ═════════════════════════════════════════════════════════
# Provider-specific API Calls
# ═════════════════════════════════════════════════════════

def _call_openrouter(api_key: str, model: str, messages: List[Dict],
                     temperature: float, max_tokens: int, **kwargs) -> Tuple[Dict, int, Dict]:
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if kwargs.get("tools"):
        payload["tools"] = kwargs["tools"]
    if kwargs.get("response_format"):
        payload["response_format"] = kwargs["response_format"]
    headers = {
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/faresrafat3/ai-earth",
        "X-Title": "AI Earth Platform",
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=_http_timeout())
    return resp.json(), resp.status_code, dict(resp.headers)

def _call_github(api_key: str, model: str, messages: List[Dict],
                 temperature: float, max_tokens: int, **kwargs) -> Tuple[Dict, int, Dict]:
    url = "https://models.inference.ai.azure.com/chat/completions"
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=payload, timeout=_http_timeout())
    return resp.json(), resp.status_code, dict(resp.headers)

def _call_google(api_key: str, model: str, messages: List[Dict],
                 temperature: float, max_tokens: int, **kwargs) -> Tuple[Dict, int, Dict]:
    # Convert messages to Gemini format
    contents = []
    for msg in messages:
        role = "user" if msg.get("role") in ("user", "system") else "model"
        contents.append({"role": role, "parts": [{"text": msg.get("content", "")}]})
    if contents and contents[0]["role"] != "user":
        contents.insert(0, {"role": "user", "parts": [{"text": "."}]})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {"contents": contents, "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=payload, timeout=_http_timeout())
    return resp.json(), resp.status_code, dict(resp.headers)

# ═════════════════════════════════════════════════════════
# Response Parsing
# ═════════════════════════════════════════════════════════

def _parse_response(data: Dict, provider: str, model: str, start_time: float) -> Dict[str, Any]:
    latency = (time.time() - start_time) * 1000

    if provider in ("openrouter", "github"):
        choice = data.get("choices", [{}])[0]
        usage = data.get("usage", {})
        cost = float(usage.get("cost", 0)) if usage.get("cost") else 0.0
        if cost == 0:
            pt = usage.get("prompt_tokens", 0)
            ct = usage.get("completion_tokens", 0)
            cost = (pt * 0.00015 + ct * 0.0006) / 1000
        return {
            "content": choice.get("message", {}).get("content", ""),
            "model": data.get("model", model), "provider": provider,
            "usage": {"prompt_tokens": usage.get("prompt_tokens", 0),
                      "completion_tokens": usage.get("completion_tokens", 0),
                      "total_tokens": usage.get("total_tokens", 0)},
            "finish_reason": choice.get("finish_reason", "stop"),
            "latency_ms": round(latency, 1), "cost_usd": round(cost, 8), "raw": data,
        }
    elif provider == "google":
        candidates = data.get("candidates", [{}])
        content = ""
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            content = "".join(p.get("text", "") for p in parts)
        usage_meta = data.get("usageMetadata", {})
        return {
            "content": content, "model": model, "provider": provider,
            "usage": {"prompt_tokens": usage_meta.get("promptTokenCount", 0),
                      "completion_tokens": usage_meta.get("candidatesTokenCount", 0),
                      "total_tokens": usage_meta.get("totalTokenCount", 0)},
            "finish_reason": candidates[0].get("finishReason", "stop") if candidates else "stop",
            "latency_ms": round(latency, 1), "cost_usd": 0.0, "raw": data,
        }

    return {"content": str(data), "model": model, "provider": provider,
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "finish_reason": "stop", "latency_ms": round(latency, 1), "cost_usd": 0.0, "raw": data}

# ═════════════════════════════════════════════════════════
# Web Search & Crawl
# ═════════════════════════════════════════════════════════

# SECURITY: the previous hardcoded value was leaked into the public repo
# (committed since v1.4.0, visible in git history). It was a real Serper
# key — anyone could have used it. The owner MUST rotate the key at
# serper.dev and update the .env file with the new value.
#
# Read the key from the environment instead of hardcoding it. The
# existing _load_env() helper already searches the repo .env,
# ~/.env, and the live process env (see top of file).
SERPER_KEY = os.environ.get("SERPER_KEY") or _load_env().get("SERPER_KEY")

if not SERPER_KEY:
    # The rest of the code treats an empty key as "no quota left today"
    # by falling through the _ledger_ok() guard. Fail loud at import
    # time too so a missing key is obvious instead of silent.
    logger.warning(
        "SERPER_KEY is not set — web_search() will always return []. "
        "Add SERPER_KEY=... to your .env or environment."
    )

def web_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    # 📒 Ledger pre-flight: Serper credits are one-time — sip slowly
    if not SERPER_KEY or not _ledger_ok("serper"):
        logger.warning("Serper key missing or daily quota exhausted (ledger) — web_search returns []")
        return []
    try:
        resp = requests.post("https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"},
            json={"q": query, "num": num_results}, timeout=15)
        _ledger_rec("serper", success=resp.status_code == 200)
        resp.raise_for_status()
        data = resp.json()
        return [{"title": i["title"], "link": i["link"], "snippet": i.get("snippet", "")}
                for i in data.get("organic", [])]
    except Exception as e:
        logger.warning(f"Web search failed: {e}")
        return []

def crawl_url(url: str) -> str:
    """Fetch a URL's text content. Returns "" on failure — NEVER fake content."""
    try:
        resp = requests.get(url, timeout=30, headers={"User-Agent": "AI-Earth/2.3"})
        resp.raise_for_status()
        return resp.text[:50000]
    except Exception as e:
        logger.warning(f"Crawl failed for {url}: {e}")
        return ""

# ═════════════════════════════════════════════════════════
# Default Model Constants
# ═════════════════════════════════════════════════════════

DEFAULT_MODEL = "openai/gpt-4o-mini"
DEFAULT_PROVIDER = "openrouter"
FALLBACK_MODEL = "gpt-4o-mini"
FALLBACK_PROVIDER = "github"

CHEAP_MODELS = {
    "fast": "openai/gpt-4o-mini",
    "smart": "anthropic/claude-3.5-sonnet",
    "free": "google/gemini-2.0-flash-001",
    "reasoning": "deepseek/deepseek-r1",
}
