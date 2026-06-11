"""
🔑 AI Earth — LLM Key Pool v2.2 (Ultra-Fallback)
═══════════════════════════════════════════════════════════
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

@dataclass
class KeyHealth:
    key_id: str
    api_key: str
    provider: ProviderType
    last_used: float = 0.0
    cooldown_until: float = 0.0

    def is_available(self) -> bool:
        return time.time() >= self.cooldown_until

class KeyPool:
    def __init__(self):
        self._keys: Dict[str, KeyHealth] = {}
        self._by_provider: Dict[ProviderType, List[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def add_key(self, provider: ProviderType, api_key: str):
        if not api_key or "your-key" in api_key: return
        key_id = f"{provider.value}_{len(self._keys)}"
        with self._lock:
            self._keys[key_id] = KeyHealth(key_id, api_key, provider)
            self._by_provider[provider].append(key_id)

    def get_key(self, provider: ProviderType) -> Optional[KeyHealth]:
        with self._lock:
            kids = self._by_provider.get(provider, [])
            available = [self._keys[kid] for kid in kids if self._keys[kid].is_available()]
            if not available: return None
            available.sort(key=lambda k: k.last_used)
            return available[0]

_pool: Optional[KeyPool] = None

def get_key_pool() -> KeyPool:
    global _pool
    if _pool: return _pool
    p = KeyPool()
    env_vars = {}
    paths = ["/home/user/ai-earth/.env", "./.env", "../.env", ".env"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            k, v = parts
                            env_vars[k.strip()] = v.strip().strip('"').strip("'")
            break

    def g(k): return env_vars.get(k) or os.environ.get(k)

    for i in range(1, 12):
        k = g(f"OPENROUTER_KEY_{i}")
        if k: p.add_key(ProviderType.OPENROUTER, k)
    
    for i in range(1, 10):
        k = g(f"GOOGLE_KEY_{i}")
        if k: p.add_key(ProviderType.GOOGLE, k)

    p.add_key(ProviderType.GITHUB, g("GITHUB_MODELS_KEY"))
    p.add_key(ProviderType.SERPER, g("SERPER_KEY"))
    p.add_key(ProviderType.NVIDIA, g("NVIDIA_NIM_KEY"))
    p.add_key(ProviderType.SILICONFLOW, g("SILICON_FLOW_KEY"))
    p.add_key(ProviderType.FIRECRAWL, g("FIRECRAWL_KEY"))
    
    _pool = p
    return p

def call_llm(model: str, messages: List[Dict], **kwargs):
    pool = get_key_pool()
    # Priority: GitHub -> Google -> OpenRouter
    for p_type in [ProviderType.GITHUB, ProviderType.GOOGLE, ProviderType.OPENROUTER]:
        key = pool.get_key(p_type)
        if not key: continue
        
        import requests
        url = ""
        headers = {"Content-Type": "application/json"}
        payload = {}

        if key.provider == ProviderType.GITHUB:
            url = "https://models.inference.ai.azure.com/chat/completions"
            headers["Authorization"] = f"Bearer {key.api_key}"
            # GitHub uses specific model names
            payload = {"model": "gpt-4o-mini", "messages": messages, **kwargs}
        
        elif key.provider == ProviderType.GOOGLE:
            # Gemini API
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key.api_key}"
            # Convert messages to Gemini format
            contents = []
            for m in messages:
                role = "user" if m['role'] in ['user', 'system'] else "model"
                contents.append({"role": role, "parts": [{"text": m['content']}]})
            payload = {"contents": contents}
            # Remove OpenAI params if present
            if 'model' in kwargs: del kwargs['model']
        
        elif key.provider == ProviderType.OPENROUTER:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers["Authorization"] = f"Bearer {key.api_key}"
            payload = {"model": model, "messages": messages, **kwargs}

        key.last_used = time.time()
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                if key.provider == ProviderType.GOOGLE:
                    content = data['candidates'][0]['content']['parts'][0]['text']
                    return {"content": content, "usage": {}, "provider": "google", "model": "gemini-1.5-flash"}
                else:
                    return {"content": data['choices'][0]['message']['content'], "usage": data.get('usage', {}), "provider": key.provider.value, "model": model}
            else:
                print(f"DEBUG: {key.provider} failed ({resp.status_code})")
                key.cooldown_until = time.time() + 120
                continue # Try next key in loop
        except:
            key.cooldown_until = time.time() + 60
            continue

    raise RuntimeError("All providers (GitHub, Google, OpenRouter) exhausted or failed.")

def web_search(query: str, num_results: int = 5):
    import requests
    key = os.environ.get("SERPER_KEY") or get_key_pool().get_key(ProviderType.SERPER).api_key
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
