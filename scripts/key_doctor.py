#!/usr/bin/env python3
"""
🩺 AI Earth — Key Doctor
═══════════════════════════════════════════════════════════
Repeatable health + credit audit for every API key in the pool.
Read-only (no token cost for OpenRouter/GitHub metadata; a tiny
smoke call is optional). Use it any time you add/rotate keys.

    python3 scripts/key_doctor.py            # full audit
    python3 scripts/key_doctor.py --smoke    # + 1 live call per provider
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import requests
from ai_earth.llm_pool import get_key_pool, ProviderType, call_llm

TIMEOUT = 15


def audit_openrouter(pool):
    print("\n══════ OPENROUTER (paid models; :free blocked without deposit) ══════")
    usable = 0
    for kid in pool._by_provider.get(ProviderType.OPENROUTER, []):
        kh = pool._keys[kid]
        try:
            r = requests.get(
                "https://openrouter.ai/api/v1/credits",
                headers={"Authorization": "Bearer " + kh.api_key},
                timeout=TIMEOUT,
            )
            if r.status_code == 200:
                d = r.json().get("data", {})
                bal = round(d.get("total_credits", 0) - d.get("total_usage", 0), 4)
                flag = "💰 usable" if bal > 0.001 else "🪫 empty"
                if bal > 0.001:
                    usable += 1
                print(f"  {kh.account:<16} balance=${bal:<9} {flag}")
            elif r.status_code == 401:
                print(f"  {kh.account:<16} ❌ INVALID/REVOKED (401)")
            else:
                print(f"  {kh.account:<16} ⚠️ status {r.status_code}")
        except Exception as e:
            print(f"  {kh.account:<16} ⚠️ {str(e)[:40]}")
    print(f"  → usable OpenRouter keys (balance>0): {usable}/"
          f"{len(pool._by_provider.get(ProviderType.OPENROUTER, []))}")


def audit_github(pool):
    print("\n══════ GITHUB MODELS (free, most reliable fallback) ══════")
    for kid in pool._by_provider.get(ProviderType.GITHUB, []):
        kh = pool._keys[kid]
        try:
            r = requests.post(
                "https://models.inference.ai.azure.com/chat/completions",
                headers={"Authorization": "Bearer " + kh.api_key,
                         "Content-Type": "application/json"},
                json={"model": "gpt-4o-mini",
                      "messages": [{"role": "user", "content": "ok"}],
                      "max_tokens": 5},
                timeout=TIMEOUT,
            )
            ok = r.status_code == 200
            print(f"  {kh.account:<16} {'✅ working' if ok else f'⚠️ status {r.status_code}'}")
        except Exception as e:
            print(f"  {kh.account:<16} ⚠️ {str(e)[:40]}")


def audit_google(pool):
    print("\n══════ GOOGLE AI STUDIO (Gemini; daily free quota, resets) ══════")
    for kid in pool._by_provider.get(ProviderType.GOOGLE, []):
        kh = pool._keys[kid]
        try:
            r = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"gemini-2.0-flash:generateContent?key={kh.api_key}",
                headers={"Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": "ok"}]}],
                      "generationConfig": {"maxOutputTokens": 5}},
                timeout=TIMEOUT,
            )
            if r.status_code == 200:
                print(f"  {kh.account:<16} ✅ working")
            elif r.status_code == 429:
                print(f"  {kh.account:<16} 🕒 quota exhausted (resets daily)")
            else:
                print(f"  {kh.account:<16} ⚠️ status {r.status_code}")
        except Exception as e:
            print(f"  {kh.account:<16} ⚠️ {str(e)[:40]}")


def main():
    pool = get_key_pool()
    s = pool.stats()
    print("🩺 AI EARTH KEY DOCTOR")
    print(f"Total keys: {s['total_keys']} | providers: {list(s['by_provider'].keys())}")

    audit_openrouter(pool)
    audit_github(pool)
    audit_google(pool)

    if "--smoke" in sys.argv:
        print("\n══════ LIVE SMOKE (1 real call through the pool) ══════")
        try:
            r = call_llm(model="gpt-4o-mini",
                         messages=[{"role": "user", "content": "Reply one word: ok"}],
                         max_tokens=8, temperature=0)
            print(f"  ✅ {r['provider']} / {r['model']} -> {r['content']!r}  (${r['cost_usd']:.6f})")
        except Exception as e:
            print(f"  ❌ pool exhausted: {str(e)[:80]}")

    print("\n💡 Recommendation:")
    print("   • GitHub Models is the reliable free workhorse right now.")
    print("   • OpenRouter free accounts are near-empty; a one-time $10 deposit")
    print("     on ONE account unlocks generous :free model daily limits.")
    print("   • Google keys work when their daily quota resets.")


if __name__ == "__main__":
    main()
