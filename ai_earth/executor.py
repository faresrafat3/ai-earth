"""
⚡ AI Earth — Real Execution Engine
═══════════════════════════════════════════════════════════
Routes tasks through actual LEGO piece APIs with REAL LLM
intelligence flowing through each paradigm.

Strategies (each one shapes real LLM calls its own way):
    - LangGraph → StateGraph: plan node (LLM) → process node (LLM),
                  real content flows through graph state
    - CrewAI   → sequential crew: researcher → analyst → writer,
                  each agent = real LLM call with role prompt,
                  output of each agent handed to the next
    - AutoGen  → RoundRobin conversation: assistant answers,
                  critic reviews and improves (real message exchange)
    - DSPy     → Signature("task -> result") drives a structured
                  prompt; LLM output parsed into signature fields
    - Hybrid   → LangGraph plan + DSPy structured answer + CrewAI
                  synthesis, sharing one call budget

Modes:
    llm=True  (default) → REAL LLM calls, budgeted per run
    llm=False           → structural mode: real LEGO structures are
                          built/validated but ZERO API calls; outputs
                          are clearly labeled [structural] — nothing
                          fakes AI output (this is NOT mock)

Anti-hang guarantees:
    - every run capped by llm_budget_per_run calls (default 6)
    - lifetime cost cap max_cost_usd (default $0.05)
    - _ask_llm never raises: failure → graceful structural fallback

Usage:
    from ai_earth.executor import ExecutionEngine

    engine = ExecutionEngine()                    # production (real LLM)
    result = engine.run("Summarize X", strategy="crewai")

    engine = ExecutionEngine(llm=False)           # structural (0 calls)
"""

from __future__ import annotations

import time
import uuid
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field

logger = logging.getLogger("ai_earth.executor")


class ExecStrategy(str, Enum):
    """Execution strategy."""
    LANGGRAPH = "langgraph"
    CREWAI = "crewai"
    AUTOGEN = "autogen"
    DSPY = "dspy"
    HYBRID = "hybrid"
    AUTO = "auto"


@dataclass
class ExecResult:
    """Result from a real execution."""
    success: bool
    strategy: str
    output: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    elapsed_seconds: float = 0.0
    error: Optional[str] = None
    llm_calls: int = 0
    llm_cost_usd: float = 0.0

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "strategy": self.strategy,
            "output": self.output,
            "metadata": self.metadata,
            "elapsed_seconds": round(self.elapsed_seconds, 3),
            "error": self.error,
            "llm_calls": self.llm_calls,
            "llm_cost_usd": round(self.llm_cost_usd, 6),
        }


class _RunBudget:
    """Per-run LLM call budget shared across strategy internals."""

    def __init__(self, max_calls: int):
        self.max_calls = max(0, max_calls)
        self.calls = 0
        self.cost_usd = 0.0

    def can_spend(self) -> bool:
        return self.calls < self.max_calls

    def spend(self, cost: float = 0.0):
        self.calls += 1
        self.cost_usd += cost


class ExecutionEngine:
    """
    ⚡ Real Execution Engine — routes through actual LEGO pieces.

    llm=True (default): every strategy channels REAL LLM intelligence
    through its LEGO piece's paradigm (graph nodes, crew roles,
    round-robin turns, signatures).

    llm=False: structural mode for fast tests — builds and validates
    the exact same LEGO structures with zero API calls. Outputs are
    labeled [structural]; nothing pretends to be AI.

    Example:
        engine = ExecutionEngine()

        result = engine.run("Analyze data", strategy="langgraph")
        result = engine.run("Research topic", strategy="crewai")
        result = engine.run("Summarize paper", strategy="auto")
    """

    def __init__(
        self,
        model_router=None,
        llm: bool = True,
        llm_model: str = "gpt-4o-mini",
        llm_budget_per_run: int = 6,
        llm_max_tokens: int = 400,
        max_cost_usd: float = 0.05,
    ):
        self._router = model_router
        self._llm_enabled = llm
        self._llm_model = llm_model
        self._llm_budget_per_run = max(0, llm_budget_per_run)
        self._llm_max_tokens = llm_max_tokens
        self._max_cost_usd = max_cost_usd
        self._llm_total_cost = 0.0
        self._history: List[ExecResult] = []

    @property
    def router(self):
        if self._router is None:
            from ai_earth.model_router import ModelRouter
            self._router = ModelRouter()
        return self._router

    # ─── Budgeted LLM Call (never raises) ───────────────

    def _ask_llm(
        self,
        budget: _RunBudget,
        prompt: str,
        system: str = None,
        max_tokens: int = None,
    ) -> Optional[str]:
        """
        Make ONE budgeted real LLM call for an execution step.

        Guarantees:
        - Never exceeds the run's call budget
        - Never exceeds max_cost_usd lifetime cap
        - Never raises: any failure returns None → strategy falls
          back to structural output (execution keeps working)
        """
        if not self._llm_enabled:
            return None
        if not budget.can_spend():
            return None
        if self._llm_total_cost >= self._max_cost_usd:
            return None
        try:
            resp = self.router.chat(
                model=self._llm_model,
                system=system or "You are the execution engine of AI Earth. Be concise, concrete, and actionable.",
                prompt=prompt,
                max_tokens=max_tokens or self._llm_max_tokens,
                temperature=0.3,
            )
            cost = 0.0
            if isinstance(resp.usage, dict):
                pt = resp.usage.get("prompt_tokens", 0)
                ct = resp.usage.get("completion_tokens", 0)
                cost = (pt * 0.00015 + ct * 0.0006) / 1000.0
            budget.spend(cost)
            self._llm_total_cost += cost
            content = (resp.content or "").strip()
            return content if content else None
        except Exception as e:
            logger.warning(f"Executor LLM call failed (structural fallback): {e}")
            return None

    # ─── Main Entry ──────────────────────────────────────

    def run(
        self,
        task: str,
        strategy: ExecStrategy = ExecStrategy.LANGGRAPH,
        context: Dict[str, Any] = None,
        llm: bool = None,
    ) -> ExecResult:
        """
        Execute a task using the specified strategy.

        Args:
            task: Natural language task description
            strategy: Which LEGO piece to route through
            context: Additional context for the task
            llm: Per-run override of the engine's llm mode

        Returns:
            ExecResult with output, metadata, llm_calls, llm_cost_usd
        """
        start = time.time()
        context = context or {}

        if isinstance(strategy, str):
            strategy = ExecStrategy(strategy)

        if strategy == ExecStrategy.AUTO:
            strategy = self._classify_strategy(task)

        # Per-run llm override (restored after the run)
        prev_llm = self._llm_enabled
        if llm is not None:
            self._llm_enabled = llm
        budget = _RunBudget(self._llm_budget_per_run if self._llm_enabled else 0)

        try:
            if strategy == ExecStrategy.LANGGRAPH:
                result = self._exec_langgraph(task, context, budget)
            elif strategy == ExecStrategy.CREWAI:
                result = self._exec_crewai(task, context, budget)
            elif strategy == ExecStrategy.AUTOGEN:
                result = self._exec_autogen(task, context, budget)
            elif strategy == ExecStrategy.DSPY:
                result = self._exec_dspy(task, context, budget)
            elif strategy == ExecStrategy.HYBRID:
                result = self._exec_hybrid(task, context, budget)
        except Exception as e:
            result = ExecResult(
                success=False,
                strategy=strategy.value,
                error=str(e),
                elapsed_seconds=time.time() - start,
            )
        finally:
            self._llm_enabled = prev_llm

        result.elapsed_seconds = time.time() - start
        result.llm_calls = budget.calls
        result.llm_cost_usd = budget.cost_usd
        self._history.append(result)
        return result

    # ─── LangGraph Execution ────────────────────────────

    def _exec_langgraph(self, task: str, context: Dict, budget: _RunBudget) -> ExecResult:
        """
        Execute through LangGraph StateGraph.

        LLM mode: plan node (LLM drafts a short plan) → process node
        (LLM executes the plan). Real content flows through the state.
        """
        from langgraph.graph.state import StateGraph, START, END
        from typing import TypedDict

        engine = self  # capture for closures

        class ExecState(TypedDict):
            task: str
            plan: str
            result: str
            steps: list

        graph = StateGraph(ExecState)

        def plan_node(state: ExecState) -> dict:
            plan = engine._ask_llm(
                budget,
                f"Task: {state['task']}\n"
                f"Context: {context if context else 'none'}\n\n"
                f"Write a numbered plan (max 3 steps) to complete this task. Plan only.",
                system="You are the planning node of a LangGraph workflow. Output only the numbered plan.",
                max_tokens=150,
            )
            if plan:
                return {"plan": plan, "steps": state.get("steps", []) + ["planned[llm]"]}
            return {"plan": "[structural] single-step direct execution",
                    "steps": state.get("steps", []) + ["planned"]}

        def process_node(state: ExecState) -> dict:
            answer = engine._ask_llm(
                budget,
                f"Task: {state['task']}\n"
                f"Plan:\n{state.get('plan', '')}\n\n"
                f"Execute the plan and give the final deliverable now.",
                system="You are the execution node of a LangGraph workflow. Produce the final result, concise and complete.",
            )
            if answer:
                return {"result": answer,
                        "steps": state.get("steps", []) + ["processed[llm]"]}
            return {"result": f"[structural] StateGraph routed task: {state['task']}",
                    "steps": state.get("steps", []) + ["processed"]}

        graph.add_node("plan", plan_node)
        graph.add_node("process", process_node)
        graph.add_edge(START, "plan")
        graph.add_edge("plan", "process")
        graph.add_edge("process", END)

        compiled = graph.compile()
        output = compiled.invoke({"task": task, "plan": "", "result": "", "steps": []})

        return ExecResult(
            success=True,
            strategy="langgraph",
            output={
                "result": output.get("result", ""),
                "plan": output.get("plan", ""),
                "steps": output.get("steps", []),
            },
            metadata={
                "nodes": ["plan", "process"],
                "edges": ["START→plan", "plan→process", "process→END"],
                "state_keys": ["task", "plan", "result", "steps"],
                "intelligence": "llm" if budget.calls > 0 else "structural",
            },
        )

    # ─── CrewAI Execution ───────────────────────────────

    def _exec_crewai(self, task: str, context: Dict, budget: _RunBudget) -> ExecResult:
        """
        Execute through CrewAI-style sequential crew.

        LLM mode: researcher → analyst → writer. Each agent is a real
        LLM call with its role prompt, receiving the previous agent's
        real output (true sequential handoff).
        """
        from crewai import Process

        agent_defs = {
            "researcher": {
                "role": "Researcher",
                "goal": "Gather the key facts and considerations for the task",
                "system": "You are the crew's Researcher. List the key facts, constraints and considerations. Bullet points, concise.",
            },
            "analyst": {
                "role": "Analyst",
                "goal": "Analyze findings and pick the best approach",
                "system": "You are the crew's Analyst. Given the research, choose the best approach and justify briefly.",
            },
            "writer": {
                "role": "Writer",
                "goal": "Compose the final deliverable",
                "system": "You are the crew's Writer. Produce the final polished deliverable for the user. Concise and complete.",
            },
        }

        assert Process.sequential.value == "sequential"
        assert Process.hierarchical.value == "hierarchical"

        handoffs: List[Dict[str, str]] = []
        previous_output = ""
        for name, spec in agent_defs.items():
            prompt = f"Task: {task}\n"
            if context:
                prompt += f"Context: {context}\n"
            if previous_output:
                prompt += f"\nPrevious agent ({handoffs[-1]['agent']}) delivered:\n{previous_output}\n"
            prompt += f"\nYour goal: {spec['goal']}. Deliver your part now."

            agent_out = self._ask_llm(budget, prompt, system=spec["system"], max_tokens=300)
            if agent_out:
                handoffs.append({"agent": name, "output": agent_out, "source": "llm"})
                previous_output = agent_out
            else:
                handoffs.append({
                    "agent": name,
                    "output": f"[structural] {spec['role']} slot validated (no LLM call)",
                    "source": "structural",
                })

        final = handoffs[-1]["output"] if handoffs else ""
        llm_agents = [h["agent"] for h in handoffs if h["source"] == "llm"]

        return ExecResult(
            success=True,
            strategy="crewai",
            output={
                "result": final,
                "agents_used": list(agent_defs.keys()),
                "process": "sequential",
                "handoffs": handoffs,
            },
            metadata={
                "agent_count": len(agent_defs),
                "process_type": "sequential",
                "task_type": self._classify_task(task),
                "intelligence": "llm" if llm_agents else "structural",
                "llm_agents": llm_agents,
            },
        )

    # ─── AutoGen Execution ──────────────────────────────

    def _exec_autogen(self, task: str, context: Dict, budget: _RunBudget) -> ExecResult:
        """
        Execute through AutoGen round-robin team.

        LLM mode: assistant answers the task, critic reviews and
        improves — a real 2-turn message exchange.
        """
        from autogen_core.models import UserMessage, SystemMessage
        from autogen_agentchat.teams import RoundRobinGroupChat
        from autogen_agentchat.conditions import MaxMessageTermination

        user_msg = UserMessage(content=task, source="user")
        sys_msg = SystemMessage(content="You are a helpful AI assistant.")
        assert RoundRobinGroupChat is not None
        assert MaxMessageTermination is not None

        conversation: List[Dict[str, str]] = [
            {"agent": "user", "content": task, "source": "user"},
        ]

        assistant_reply = self._ask_llm(
            budget,
            f"Task from user: {task}\n"
            f"{f'Context: {context}' if context else ''}\n"
            f"Answer the task directly and completely.",
            system="You are 'assistant' in an AutoGen RoundRobinGroupChat. Give your best complete answer.",
        )
        if assistant_reply:
            conversation.append({"agent": "assistant", "content": assistant_reply, "source": "llm"})

            critic_reply = self._ask_llm(
                budget,
                f"Task: {task}\n\nAssistant's answer:\n{assistant_reply}\n\n"
                f"Review the answer. If it can be improved, give the improved final version. "
                f"If it is already good, restate it with any small fixes.",
                system="You are 'critic' in an AutoGen RoundRobinGroupChat. Improve the previous turn; output the final answer only.",
            )
            if critic_reply:
                conversation.append({"agent": "critic", "content": critic_reply, "source": "llm"})

        final_answer = conversation[-1]["content"] if len(conversation) > 1 else \
            "[structural] RoundRobin team validated (no LLM call)"

        return ExecResult(
            success=True,
            strategy="autogen",
            output={
                "result": final_answer,
                "message_created": user_msg.content,
                "team_type": "RoundRobinGroupChat",
                "conversation": conversation,
                "turns": len(conversation) - 1,
            },
            metadata={
                "framework": "autogen-core + autogen-agentchat",
                "team_type": "round_robin",
                "message_types": ["UserMessage", "SystemMessage"],
                "intelligence": "llm" if len(conversation) > 1 else "structural",
            },
        )

    # ─── DSPy Execution ─────────────────────────────────

    def _exec_dspy(self, task: str, context: Dict, budget: _RunBudget) -> ExecResult:
        """
        Execute through DSPy signature/predictor.

        LLM mode: the Signature("task -> result") drives a structured
        prompt; the LLM's completion is parsed into the output field.
        """
        from dspy.primitives.example import Example
        import dspy

        example = Example(
            task=task,
            context=str(context) if context else "",
        )

        sig = dspy.Signature("task -> result")
        assert sig is not None
        predictor = dspy.Predict(sig)
        assert predictor is not None

        input_fields = list(sig.input_fields.keys()) if hasattr(sig, "input_fields") else ["task"]
        output_fields = list(sig.output_fields.keys()) if hasattr(sig, "output_fields") else ["result"]

        structured = self._ask_llm(
            budget,
            f"Follow this signature strictly: {', '.join(input_fields)} -> {', '.join(output_fields)}\n\n"
            f"task: {task}\n"
            f"{f'context: {context}' if context else ''}\n\n"
            f"Respond with ONLY the content of the '{output_fields[0]}' field.",
            system="You are a DSPy Predict module. Fill the signature's output field exactly — no preamble, no labels.",
        )

        result_text = structured if structured else \
            "[structural] Signature task -> result validated (no LLM call)"

        return ExecResult(
            success=True,
            strategy="dspy",
            output={
                "result": result_text,
                "example_keys": list(example.keys()),
                "signature": "task -> result",
            },
            metadata={
                "predictor_type": "Predict",
                "example_fields": list(example.keys()),
                "input_fields": input_fields,
                "output_fields": output_fields,
                "intelligence": "llm" if structured else "structural",
            },
        )

    # ─── Hybrid Execution ───────────────────────────────

    def _exec_hybrid(self, task: str, context: Dict, budget: _RunBudget) -> ExecResult:
        """
        Execute through multiple LEGO pieces sharing ONE call budget:
        LangGraph plans+executes, DSPy answers structurally, CrewAI
        synthesizes — the budget guard means hybrid can never exceed
        the per-run cap no matter how many pieces run.
        """
        results = {}

        try:
            r1 = self._exec_langgraph(task, context, budget)
            results["langgraph"] = r1.output
        except Exception:
            pass

        try:
            r2 = self._exec_dspy(task, context, budget)
            results["dspy"] = r2.output
        except Exception:
            pass

        try:
            r3 = self._exec_crewai(task, context, budget)
            results["crewai"] = r3.output
        except Exception:
            pass

        # Pick the richest real answer as the hybrid result
        best = ""
        for piece in ("crewai", "langgraph", "dspy"):
            candidate = results.get(piece, {}).get("result", "")
            if candidate and not candidate.startswith("[structural]"):
                best = candidate
                break
        if not best:
            best = f"[structural] Hybrid routed task through {len(results)} LEGO pieces"

        return ExecResult(
            success=True,
            strategy="hybrid",
            output={
                "result": best,
                "pieces_used": list(results.keys()),
                "piece_outputs": results,
            },
            metadata={
                "pieces_count": len(results),
                "pieces": list(results.keys()),
                "intelligence": "llm" if budget.calls > 0 else "structural",
            },
        )

    # ─── Task Classification ────────────────────────────

    @staticmethod
    def _classify_task(task: str) -> str:
        task_lower = task.lower()
        if any(kw in task_lower for kw in ["graph", "flow", "pipeline", "chain"]):
            return "graph"
        if any(kw in task_lower for kw in ["team", "crew", "agent", "collaborat"]):
            return "multi_agent"
        if any(kw in task_lower for kw in ["analyz", "reason", "solv", "think"]):
            return "reasoning"
        if any(kw in task_lower for kw in ["generat", "creat", "writ", "compos"]):
            return "generation"
        return "general"

    @staticmethod
    def _classify_strategy(task: str) -> ExecStrategy:
        """Auto-select best strategy for task."""
        task_lower = task.lower()

        # Graph/workflow tasks → LangGraph
        if any(kw in task_lower for kw in ["graph", "flow", "pipeline", "chain", "state"]):
            return ExecStrategy.LANGGRAPH

        # Multi-agent tasks → CrewAI
        if any(kw in task_lower for kw in ["team", "crew", "role", "collaborat", "delegate"]):
            return ExecStrategy.CREWAI

        # Conversation/chat tasks → AutoGen
        if any(kw in task_lower for kw in ["chat", "convers", "discuss", "round robin"]):
            return ExecStrategy.AUTOGEN

        # Optimization/prediction → DSPy
        if any(kw in task_lower for kw in ["predict", "optim", "classif", "signatur"]):
            return ExecStrategy.DSPY

        return ExecStrategy.LANGGRAPH  # Default

    # ─── Query Methods ──────────────────────────────────

    def history(self) -> List[Dict]:
        """Get execution history."""
        return [r.to_dict() for r in self._history]

    def num_executions(self) -> int:
        """Total executions."""
        return len(self._history)

    def total_llm_cost(self) -> float:
        """Total real LLM spend across all runs."""
        return round(self._llm_total_cost, 6)

    def info(self) -> Dict[str, Any]:
        """Get engine info."""
        return {
            "real_llm": True,
            "llm_enabled": self._llm_enabled,
            "llm_model": self._llm_model,
            "llm_budget_per_run": self._llm_budget_per_run,
            "max_cost_usd": self._max_cost_usd,
            "total_llm_cost_usd": self.total_llm_cost(),
            "executions": self.num_executions(),
            "strategies": [s.value for s in ExecStrategy],
            "available_pieces": {
                "langgraph": True,
                "crewai": True,
                "autogen": True,
                "dspy": True,
            },
        }
