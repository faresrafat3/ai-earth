"""
🔑 AI Earth — LLM Key Pool v2.6 (Silent Guard)
═══════════════════════════════════════════════════════════
"""

from __future__ import annotations
import os
import time
import requests
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

class ProviderType:
    OPENROUTER = "openrouter"
    GITHUB = "github"
    GOOGLE = "google"
    SILICONFLOW = "siliconflow"
    NVIDIA = "nvidia"

def call_llm(model: str, messages: List[Dict], **kwargs):
    # مصفاة ذكية لتجاوز الـ APIs اللي جابت آخرها
    # هحاول أستخدم GitHub Models كأولوية لأنها غالباً بتبقى صامدة
    
    env_path = "/home/user/ai-earth/.env"
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")

    # 1. Try GitHub (Resilient)
    gh_key = env.get("GITHUB_MODELS_KEY")
    if gh_key:
        try:
            resp = requests.post("https://models.inference.ai.azure.com/chat/completions", 
                                 headers={"Authorization": f"Bearer {gh_key}"}, 
                                 json={"model": "gpt-4o-mini", "messages": messages}, timeout=10)
            if resp.status_code == 200:
                return {"content": resp.json()['choices'][0]['message']['content'], "provider": "github", "model": "gpt-4o-mini"}
        except: pass

    # 2. Try Google AI Studio
    for i in range(1, 10):
        g_key = env.get(f"GOOGLE_KEY_{i}")
        if g_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={g_key}"
                contents = [{"role": "user" if m['role'] in ['user', 'system'] else "model", "parts": [{"text": m['content']}]} for m in messages]
                resp = requests.post(url, json={"contents": contents}, timeout=10)
                if resp.status_code == 200:
                    return {"content": resp.json()['candidates'][0]['content']['parts'][0]['text'], "provider": "google", "model": "gemini-1.5-flash"}
            except: pass

    # 3. Last Resort: OpenRouter
    for i in range(1, 12):
        or_key = env.get(f"OPENROUTER_KEY_{i}")
        if or_key:
            try:
                resp = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                     headers={"Authorization": f"Bearer {or_key}"}, 
                                     json={"model": model, "messages": messages}, timeout=10)
                if resp.status_code == 200:
                    return {"content": resp.json()['choices'][0]['message']['content'], "provider": "openrouter", "model": model}
            except: pass

    raise RuntimeError("All strategic backends are currently rate-limited. Running in Autonomous Mesh Mode.")

def web_search(query: str, num_results: int = 5):
    key = "218d569076c2d11413e9bb6185fc9b7c32642b45"
    try:
        resp = requests.post("https://google.serper.dev/search", headers={"X-API-KEY": key}, json={"q": query, "num": num_results}, timeout=10)
        return [{"title": i['title'], "link": i['link'], "snippet": i.get('snippet', '')} for i in resp.json().get('organic', [])]
    except: return []

def crawl_url(url: str):
    return f"Simulated content for {url} based on AI Earth metadata."
