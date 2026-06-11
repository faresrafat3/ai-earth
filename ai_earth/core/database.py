"""
📜 The Ledger of Earth — OmniLog Database
═══════════════════════════════════════════════════════════
Centralized logging and data collection system for all platform 
activities. Designed for AI training and evolution tracking.
"""

import sqlite3
import json
import time
import os
from typing import Any, Dict, Optional

class OmniLog:
    def __init__(self, db_path="/home/user/ai-earth/data/earth_ledger.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Table for LLM Interactions (Training Data Goldmine)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS llm_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    model TEXT,
                    provider TEXT,
                    prompt TEXT,
                    response TEXT,
                    tokens INTEGER,
                    cost REAL,
                    latency_ms REAL,
                    context_metadata TEXT
                )
            """)
            # Table for Evolution Cycles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evolution_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    task TEXT,
                    iteration INTEGER,
                    phase TEXT,
                    observation TEXT,
                    plan TEXT,
                    result TEXT,
                    score REAL
                )
            """)
            # Table for Synapse Thinking (High-Order Logic)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS synapse_thoughts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    task TEXT,
                    thought_process TEXT,
                    breakthrough_insight TEXT
                )
            """)
            conn.commit()

    def log_llm(self, model: str, provider: str, prompt: str, response: str, usage: dict, latency: float, metadata: dict = None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO llm_interactions (model, provider, prompt, response, tokens, cost, latency_ms, context_metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (model, provider, prompt, response, usage.get('total_tokens', 0), 0.0, latency, json.dumps(metadata or {})))
            conn.commit()
        # Also save to JSONL for easy AI training export
        self._append_jsonl("llm_training_data.jsonl", {
            "prompt": prompt,
            "completion": response,
            "metadata": metadata
        })

    def log_evolution(self, task: str, iteration: int, phase: str, observation: str, plan: str, result: str, score: float):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO evolution_logs (task, iteration, phase, observation, plan, result, score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (task, iteration, phase, observation, plan, result, score))
            conn.commit()

    def log_synapse(self, task: str, process: str, insight: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO synapse_thoughts (task, thought_process, breakthrough_insight)
                VALUES (?, ?, ?)
            """, (task, process, insight))
            conn.commit()

    def _append_jsonl(self, filename: str, data: dict):
        path = f"/home/user/ai-earth/data/vault/{filename}"
        with open(path, "a") as f:
            f.write(json.dumps(data) + "\n")

    def get_stats(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM llm_interactions")
            llm_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM evolution_logs")
            evo_count = cursor.fetchone()[0]
            return {"total_llm_calls": llm_count, "total_evolution_steps": evo_count}

# Global singleton
ledger = OmniLog()
