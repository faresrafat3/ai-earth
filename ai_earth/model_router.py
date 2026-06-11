"""
🌐 AI Earth — Model Router v0.9.0
═══════════════════════════════════════════════════════════
Unified LLM interface with Ledger v2 integration.
"""

from __future__ import annotations
import time
import logging
from typing import Any, Dict, List, Optional, Union
from ai_earth.llm_pool import call_llm, web_search, crawl_url

logger = logging.getLogger("ai_earth.model_router")

class ChatResponse:
    def __init__(self, content, model, provider, usage, latency_ms):
        self.content = content
        self.model = model
        self.provider = provider
        self.usage = usage
        self.latency_ms = latency_ms

class ModelRouter:
    def __init__(self):
        self.default_model = "openai/gpt-4o-mini"

    def chat(self, model: str = None, prompt: str = None, messages: List[Dict] = None, **kwargs) -> ChatResponse:
        model = model or self.default_model
        if not messages:
            messages = [{"role": "user", "content": prompt}]
        
        start = time.time()
        res = call_llm(model, messages, **kwargs)
        latency = (time.time() - start) * 1000
        
        # Log to Ledger
        try:
            from ai_earth.core.database import ledger
            ledger.log_llm(model, res['provider'], str(messages), res['content'], res['usage'], latency)
        except Exception as e:
            logger.warning(f"Ledger logging failed: {e}")
            
        return ChatResponse(res['content'], res['model'], res['provider'], res['usage'], latency)

    def ask(self, prompt: str, model: str = None, **kwargs) -> str:
        res = self.chat(model=model, prompt=prompt, **kwargs)
        return res.content

    def web_search(self, query: str, num_results: int = 5):
        return web_search(query, num_results)

    def crawl(self, url: str):
        return crawl_url(url)

    def list_models(self, provider=None):
        return [{"name": "gpt-4o", "provider": "openai"}, {"name": "claude-3-sonnet", "provider": "anthropic"}]

    def list_providers(self):
        return {"openrouter": True, "google": True, "github": True}

    def info(self):
        return {"version": "0.9.0", "engine": "KeyPool v2"}
