"""
🔑 AI Earth — LLM Key Pool v2.5 (High-Density & Ultra-Resilient)
═══════════════════════════════════════════════════════════
Manages 30+ API keys across 10+ providers with intelligent 
cooldowns and recursive fallback logic.
"""

from __future__ import annotations
import os
import time
import json
import logging
import threading
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger("ai_earth.llm_pool")

class ProviderType(str, Enum):
    OPENROUTER = "openrouter"
    GITHUB = "github"
    GOOGLE = "google"
    SERPER = "serper"
    NVIDIA = "nvidia"
    SILICONFLOW = "siliconflow"
    FIRECRAWL = "firecrawl"
    MISTRAL = "mistral"
    TINKER = "tinker"
    LLM7 = "llm7"
    CLOUDFLARE = "cloudflare"
    AGNES = "agnes"

@dataclass
class KeyHealth:
    key_id: str
    api_key: str
    provider: ProviderType
    account: str = ""
    last_used: float = 0.0
    cooldown_until: float = 0.0
    failure_count: int = 0

    def is_available(self) -> bool:
        return time.time() >= self.cooldown_until

    def mark_failure(self, status_code: int):
        self.failure_count += 1
        # 402 = Payment required/Credits exhausted, 429 = Rate limited
        if status_code in [402, 429]:
            self.cooldown_until = time.time() + 3600 # 1 hour for exhausted credits
        else:
            self.cooldown_until = time.time() + 60 # 1 min for temporary errors

    def mark_success(self):
        self.failure_count = 0
        self.last_used = time.time()

class KeyPool:
    def __init__(self):
        self._keys: Dict[str, KeyHealth] = {}
        self._by_provider: Dict[ProviderType, List[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def add_key(self, provider: ProviderType, api_key: str, account: str = ""):
        if not api_key or "your-key" in api_key or len(api_key) < 5: return
        key_id = f"{provider.value}_{len(self._keys)}"
        with self._lock:
            self._keys[key_id] = KeyHealth(key_id, api_key, provider, account)
            self._by_provider[provider].append(key_id)

    def get_key(self, provider: ProviderType) -> Optional[KeyHealth]:
        with self._lock:
            kids = self._by_provider.get(provider, [])
            available = [self._keys[kid] for kid in kids if self._keys[kid].is_available()]
            if not available: return None
            # Round-robin by last_used
            available.sort(key=lambda k: k.last_used)
            return available[0]

    def get_any_healthy_key(self) -> Optional[KeyHealth]:
        """Try providers in priority order."""
        for p in [ProviderType.OPENROUTER, ProviderType.SILICONFLOW, ProviderType.AGNES, 
                  ProviderType.MISTRAL, ProviderType.NVIDIA, ProviderType.GITHUB, ProviderType.GOOGLE]:
            k = self.get_key(p)
            if k: return k
        return None

_pool: Optional[KeyPool] = None

def get_key_pool() -> KeyPool:
    global _pool
    if _pool: return _pool
    
    p = KeyPool()
    env_data = {}
    env_path = "/home/user/ai-earth/.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env_data[k.strip()] = v.strip().strip('"').strip("'")
    
    def g(k): return env_data.get(k) or os.environ.get(k)

    # 11 OpenRouter Keys
    for i in range(1, 12):
        k = g(f"OPENROUTER_KEY_{i}")
        if k: p.add_key(ProviderType.OPENROUTER, k, f"OR_acc_{i}")
    
    # 9 Google Keys
    for i in range(1, 10):
        k = g(f"GOOGLE_KEY_{i}")
        if k: p.add_key(ProviderType.GOOGLE, k, f"G_acc_{i}")

    # Others
    p.add_key(ProviderType.GITHUB, g("GITHUB_MODELS_KEY"), "fares")
    p.add_key(ProviderType.SERPER, g("SERPER_KEY"), "main")
    p.add_key(ProviderType.NVIDIA, g("NVIDIA_NIM_KEY"), "main")
    p.add_key(ProviderType.SILICONFLOW, g("SILICON_FLOW_KEY"), "main")
    p.add_key(ProviderType.FIRECRAWL, g("FIRECRAWL_KEY"), "main")
    p.add_key(ProviderType.MISTRAL, g("MISTRAL_KEY"), "main")
    p.add_key(ProviderType.TINKER, g("TINKER_KEY"), "main")
    p.add_key(ProviderType.LLM7, g("LLM7_KEY"), "main")
    p.add_key(ProviderType.CLOUDFLARE, g("CLOUDFLARE_TOKEN"), "main")
    p.add_key(ProviderType.AGNES, g("AGNES_AI_KEY"), "fares")

    _pool = p
    return p

def call_llm(model: str, messages: List[Dict], **kwargs):
    pool = get_key_pool()
    key = pool.get_any_healthy_key()
    if not key: raise RuntimeError("FATAL: All 30+ keys in the pool are exhausted or in cooldown.")
    
    import requests
    # Set Endpoint based on provider
    url = "https://openrouter.ai/api/v1/chat/completions"
    if key.provider == ProviderType.SILICONFLOW: url = "https://api.siliconflow.cn/v1/chat/completions"
    elif key.provider == ProviderType.NVIDIA: url = "https://integrate.api.nvidia.com/v1/chat/completions"
    elif key.provider == ProviderType.MISTRAL: url = "https://api.mistral.ai/v1/chat/completions"
    elif key.provider == ProviderType.GITHUB: url = "https://models.inference.ai.azure.com/chat/completions"
    elif key.provider == ProviderType.GOOGLE: url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key.api_key}"
    elif key.provider == ProviderType.AGNES: url = "https://api.agnes.ai/v1/chat/completions" # Assuming OpenAI compatible

    headers = {"Authorization": f"Bearer {key.api_key}", "Content-Type": "application/json"}
    
    # Provider-specific payload handling
    if key.provider == ProviderType.GOOGLE:
        contents = []
        for m in messages:
            role = "user" if m['role'] in ['user', 'system'] else "model"
            contents.append({"role": role, "parts": [{"text": m['content']}]})
        payload = {"contents": contents}
    else:
        # Standard OpenAI-like
        actual_model = model
        if key.provider == ProviderType.GITHUB: actual_model = "gpt-4o-mini"
        if key.provider == ProviderType.SILICONFLOW: actual_model = "deepseek-ai/DeepSeek-V3"
        payload = {"model": actual_model, "messages": messages, **kwargs}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            key.mark_success()
            data = resp.json()
            if key.provider == ProviderType.GOOGLE:
                content = data['candidates'][0]['content']['parts'][0]['text']
                usage = data.get('usageMetadata', {})
            else:
                content = data['choices'][0]['message']['content']
                usage = data.get('usage', {})
            return {"content": content, "usage": usage, "provider": key.provider.value, "model": model}
        else:
            print(f"DEBUG: Key {key.key_id} ({key.provider}) failed with status {resp.status_code}")
            key.mark_failure(resp.status_code)
            return call_llm(model, messages, **kwargs) # Recursive retry
    except Exception as e:
        key.mark_failure(500)
        return call_llm(model, messages, **kwargs)

def web_search(query: str, num_results: int = 5):
    import requests
    key = os.environ.get("SERPER_KEY") or "218d569076c2d11413e9bb6185fc9b7c32642b45"
    resp = requests.post("https://google.serper.dev/search", headers={"X-API-KEY": key}, json={"q": query, "num": num_results})
    return [{"title": i['title'], "link": i['link'], "snippet": i.get('snippet', '')} for i in resp.json().get('organic', [])]

def crawl_url(url: str):
    import requests
    key = os.environ.get("FIRECRAWL_KEY") or "fc-30e1fa56152b4046a0b0d886f1cc2f5e"
    try:
        resp = requests.post("https://api.firecrawl.dev/v1/scrape", headers={"Authorization": f"Bearer {key}"}, json={"url": url, "formats": ["markdown"]})
        return resp.json().get('data', {}).get('markdown', 'Crawl failed')
    except:
        return f"Failed to crawl {url}"
