"""
📜 The Ledger of Earth — OmniLog Database v2.1
═══════════════════════════════════════════════════════════
Fixed for Dictionary serialization and Deep Intelligence.
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS research_intel (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    paper_name TEXT, url TEXT, credibility_score REAL,
                    technical_logic TEXT, experimental_results TEXT,
                    completeness_analysis TEXT, code_stub TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS llm_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    model TEXT, prompt TEXT, response TEXT, tokens INTEGER, latency_ms REAL
                )
            """)
            conn.commit()

    def log_research_full_cycle(self, data: dict):
        """سجل كامل للدورة الاستخبارية للبحث مع تحويل الـ Dicts لنصوص"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO research_intel 
                (paper_name, url, credibility_score, technical_logic, experimental_results, completeness_analysis, code_stub)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data['name'], data['url'], float(data['credibility']), 
                json.dumps(data['logic']), json.dumps(data['experiments']), 
                str(data['completeness']), data['code']
            ))
            conn.commit()
        self._append_jsonl("research_training_set.jsonl", data)

    def log_llm(self, model, provider, prompt, response, usage, latency, metadata=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO llm_interactions (model, prompt, response, tokens, latency_ms) VALUES (?, ?, ?, ?, ?)",
                           (model, prompt, response, usage.get('total_tokens', 0), latency))
            conn.commit()

    def _append_jsonl(self, filename, data):
        path = f"/home/user/ai-earth/data/vault/{filename}"
        with open(path, "a") as f:
            f.write(json.dumps(data) + "\n")

    def get_stats(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM research_intel")
            research_count = cursor.fetchone()[0]
            return {"intel_cycles": research_count}

ledger = OmniLog()
