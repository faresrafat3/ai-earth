# AI Earth — Research Rebuild

> Evaluation-first, cost-aware, evidence-grounded AI systems research.

AI Earth is currently in a **deep discovery and research phase**.  
The goal is not to ship a hype demo, but to systematically discover a strong scientific/product thesis from advanced AI domains, current literature, real-world projects, market pain, and rigorous experiments.

## Current Research Thesis Direction

Across dozens of domains, a repeating pattern is emerging:

> **Evidence + Evaluation + Workflow + Governance + Cheap Routing + Data Flywheel**

The project is exploring how to build AI systems that are:

- **Evidence-grounded** — claims, actions, and decisions link back to sources/data.
- **Cost-aware** — cheapest sufficient method first; escalate only when needed.
- **Auditable** — every important step leaves a trace.
- **Evaluation-first** — measure quality, risk, cost, and failure modes before scaling.
- **Human-in-the-loop where necessary** — especially in high-stakes workflows.
- **Data-flywheel oriented** — failures, corrections, and outcomes improve the system.

## Repository Structure

Main research workspace:

[`ai-earth-rebuild/`](./ai-earth-rebuild)

Inside it you will find:

- experimental code and evaluation harnesses
- methodological audits
- real-model pilots
- resource management layer
- discovery protocol and synthesis notes
- 47 deep discovery rounds across AI domains

## Key Research Tracks

### 1. Evaluation & Cost-Aware AI Composition

Early experiments explored solver composition, self-consistency, verification, cost per correct answer, and real-model behavior.

Important lesson:

> More complex AI composition is not automatically better. Cost, topology of errors, and real-world model behavior matter.

### 2. Error Topology Experiments

EXP13 and related pilots investigate whether early answer distributions can predict when cheap self-consistency is sufficient and when escalation is needed.

Core idea:

> Route by evidence/error topology, not by blind model confidence.

### 3. Discovery Program

A broad domain discovery process is underway to identify the strongest project opportunity.  
Current discovery rounds cover AI for research, agents, RAG, evaluation, security, healthcare, finance, logistics, grid, telecom, property operations, EDA, privacy, and more.

See:

[`ai-earth-rebuild/DISCOVERY_INDEX.md`](./ai-earth-rebuild/DISCOVERY_INDEX.md)

## Strong Emerging Candidate Clusters

No final project decision has been made yet. However, repeated clusters are emerging:

1. **Evidence & Evaluation OS**
2. **Workflow / Policy / SOP-to-Action Compiler**
3. **Cheap Genius Runtime / Cost-to-Quality Router**
4. **Document Intelligence + Evidence Packs**
5. **Data Flywheel / Correction Capture Layer**
6. **Risk / Governance / Permission Layer**
7. **Agent Flight Recorder / AI Action Audit Log**
8. **Privacy-Aware AI Control Plane**

## Research Philosophy

AI Earth is being rebuilt around a simple principle:

> **No intelligence without evidence. No autonomy without audit. No scale without evaluation. No cost without value.**

This repository is intentionally research-heavy. It is designed to preserve reasoning, experiments, audits, and discovery notes before committing to a final product direction.

## Status

- Branch: `main` and `research/exp13-error-topology`
- Current phase: **Discovery + research synthesis**
- Final product idea: **not selected yet**
- Latest discovery coverage: **47 rounds**

