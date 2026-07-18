"""
📜 The Ledger of Earth — OmniLog Database v2.2 (Unified)
═══════════════════════════════════════════════════════════
"""

import sqlite3
import json
import time
import os

class OmniLog:
    def __init__(self, db_path="/home/user/ai-earth/data/earth_ledger.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS synapse_thoughts (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, thought_process TEXT, breakthrough_insight TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS llm_interactions (id INTEGER PRIMARY KEY AUTOINCREMENT, model TEXT, prompt TEXT, response TEXT, tokens INTEGER, latency_ms REAL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS research_intel (id INTEGER PRIMARY KEY AUTOINCREMENT, paper_name TEXT, credibility_score REAL, technical_logic TEXT, code_stub TEXT)")
            conn.commit()

    def log_synapse(self, task, process, insight):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO synapse_thoughts (task, thought_process, breakthrough_insight) VALUES (?, ?, ?)", (task, process, insight))
            conn.commit()

    def log_llm(self, model, provider, prompt, response, usage, latency):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO llm_interactions (model, prompt, response, tokens, latency_ms) VALUES (?, ?, ?, ?, ?)",
                           (model, prompt, response, usage.get('total_tokens', 0), latency))
            conn.commit()

    def log_research_full_cycle(self, data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO research_intel (paper_name, credibility_score, technical_logic, code_stub) VALUES (?, ?, ?, ?)",
                           (data['name'], data['credibility'], json.dumps(data['logic']), data['code']))
            conn.commit()

    def log_evolution(self, task, iteration, phase, input_data, plan, output, score):
        """Log an evolution cycle."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS evolution_log (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, iteration INTEGER, phase TEXT, input_data TEXT, plan TEXT, output TEXT, score REAL, timestamp TEXT)")
                cursor.execute(
                    "INSERT INTO evolution_log (task, iteration, phase, input_data, plan, output, score, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))",
                    (str(task)[:100], iteration, phase, str(input_data)[:200], str(plan)[:200], str(output)[:200], float(score))
                )
                conn.commit()
        except Exception as e:
            print(f"Ledger evolution log error: {e}")

    def get_stats(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM llm_interactions")
            llm = cursor.fetchone()[0]
            cursor.execute("SELECT SUM(tokens) FROM llm_interactions")
            tokens = cursor.fetchone()[0] or 0
            return {"total_calls": llm, "total_tokens": tokens}

ledger = OmniLog()
