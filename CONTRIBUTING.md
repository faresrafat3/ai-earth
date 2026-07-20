# Contributing to AI Earth

Welcome to **AI Earth**. This is NOT a standard AI Agent platform; it is an **Intelligence Aggregator**. Our goal is to extract logic verbatim from top-tier research papers and synthesize them into a unified "LEGO Library."

## 🧱 Adding a New "LEGO Piece" (Research Paper)

If you have found a new SOTA paper and want to add its logic to AI Earth, you must follow this exact methodology:

### 1. The Paper Analysis
Before writing code, open an Issue titled `[LEGO]: <Paper Title>` with:
- The arXiv/DOI link.
- A summary of the core cognitive mechanic (e.g., "Mutual reasoning via Monte Carlo Tree Search").
- Why it belongs in the Synapse Kernel.

### 2. Logic Extraction
- We do not use wrapper libraries like Langchain for core logic. You must extract the pure mathematical or logical flow described in the paper.
- The logic must be decoupled so it can communicate via **The Intelligence Bus**.

### 3. Database Schema
- If your agent logic requires tracking new types of metadata, ensure it writes to the `OmniLog Ledger v2` (`SQLite` + `JSONL`) without breaking existing tracking for other agents.

### 4. Resiliency 
- Any new node added MUST support the **Resilient Mesh** fallback mode. If the external LLM API fails, your logic should gracefully degrade and rely on historical data.

## 🐞 Reporting Bugs
If you find a cognitive loop failing or an API key exhaust loop, please use the Bug Report template and attach the relevant `OmniLog` trace.
