"""
🎨 AI Earth — Streamlit Web UI
═══════════════════════════════════════════════════════════
Interactive web interface for the AI Earth platform.

Pages:
    🏠 Dashboard     — Platform overview, stats, health
    🧬 Evolve        — Run self-evolution loop interactively
    🧱 LEGO Pieces   — Browse all extracted LEGO pieces
    🌐 API Explorer  — Test all REST API endpoints
    💬 Chat          — Chat with LLM via Model Router

Run:
    streamlit run ai_earth/ui.py --server.port 8501
"""

import sys
import os
import time
import json

# Ensure LEGO paths
_lego_path = os.path.join(os.path.dirname(__file__), 'lego')
_stubs_path = os.path.join(_lego_path, 'stubs')
if _stubs_path not in sys.path:
    sys.path.append(_stubs_path)
if _lego_path not in sys.path:
    sys.path.insert(0, _lego_path)

import streamlit as st

# ═════════════════════════════════════════════════════════
# Page Config
# ═════════════════════════════════════════════════════════

st.set_page_config(
    page_title="🌍 AI Earth",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════════════════
# Cached Resources
# ═════════════════════════════════════════════════════════

@st.cache_resource
def get_earth():
    from ai_earth.orchestrator import AIEarth
    return AIEarth()

@st.cache_resource
def get_evolve_core():
    from ai_earth.self_evolve import SelfEvolveCore
    return SelfEvolveCore()

@st.cache_resource
def get_router():
    from ai_earth.model_router import ModelRouter
    router = ModelRouter()
    router.configure()  # Uses real LLM via Key Pool
    return router

# ═════════════════════════════════════════════════════════
# Sidebar Navigation
# ═════════════════════════════════════════════════════════

st.sidebar.title("🌍 AI Earth")
st.sidebar.caption("The Living Intelligence Ecosystem v0.4.0")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "🧬 Evolve", "🔍 Research Discovery", "🧱 LEGO Pieces", "💬 Chat"],
    label_visibility="collapsed",
)

st.sidebar.divider()

# Quick stats in sidebar
try:
    core = get_evolve_core()
    st.sidebar.metric("Evolution Cycles", core.num_cycles())
    st.sidebar.metric("Best Score", f"{core.best_score():.3f}")
    st.sidebar.metric("Learnings", core.num_learnings())
except Exception:
    pass

st.sidebar.divider()
st.sidebar.caption("592 tests ✅ | 8 papers | 197K lines")
st.sidebar.caption("21 API Keys 🔑 | v0.4.0")

# ═════════════════════════════════════════════════════════
# Page: Dashboard
# ═════════════════════════════════════════════════════════

if page == "🏠 Dashboard":
    st.title("🌍 AI Earth — Dashboard")
    st.markdown("Intelligence Aggregation Platform built from **8 LEGO pieces** extracted verbatim from research papers.")
    
    # Top metrics
    earth = get_earth()
    info = earth.platform_info()
    totals = info["totals"]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Papers/LEGO", totals["papers"])
    col2.metric("📁 Files", totals["files"])
    col3.metric("📝 Lines", f"{totals['lines']:,}")
    col4.metric("✅ Tests", totals["tests"])
    
    st.divider()
    
    # LEGO Pieces Table
    st.subheader("🧱 LEGO Pieces (Extracted Research)")
    
    pieces_data = []
    for name, p in info["lego_pieces"].items():
        pieces_data.append({
            "Piece": name.upper(),
            "Source": p["source"].split("(")[0].strip(),
            "Files": p["files"],
            "Lines": f"{p['lines']:,}",
            "Tests": p["tests"],
            "Components": p["components"],
        })
    
    st.dataframe(
        pieces_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Piece": st.column_config.TextColumn("Piece", width="small"),
            "Source": st.column_config.TextColumn("Source", width="medium"),
            "Components": st.column_config.TextColumn("Components", width="large"),
        },
    )
    
    st.divider()
    
    # Architecture
    st.subheader("🏗️ Architecture")
    
    col_arch1, col_arch2 = st.columns(2)
    
    with col_arch1:
        st.markdown("""
        **🧬 Self-Evolving Core**
        ```
        Observe → Plan → Execute → Evaluate → Reflect → Evolve → Remember
           ↓         ↓        ↓         ↓         ↓        ↓        ↓
         Mem0    DSPy/LG   CrewAI    DSPy     Self     EvoAgentX   Mem0
        ```
        
        **6 Strategies:**
        - `prompt_optimize` — DSPy MIPRO/EvoPrompt
        - `workflow_evolve` — EvoAgentX SEW/AFlow
        - `agent_refine` — CrewAI agent tuning
        - `memory_augment` — Mem0 context enrichment
        - `graph_restructure` — LangGraph topology
        - `hybrid` — Combine multiple
        """)
    
    with col_arch2:
        st.markdown("""
        **🔗 LEGO Pieces**
        - **EvoAgentX** — Workflow Engine + 6 Optimizers
        - **DSPy** — Signatures + Predictors
        - **Mem0** — Memory + Embeddings
        - **Model Router** — Unified LLM (12 providers)
        - **LangGraph** — Graph Engine
        - **CrewAI** — Multi-Agent Crews
        - **AutoGen** — Event-Driven Runtime
        - **Research Discovery** — Aggregator
        - **ActiveSymbolic** — Category Theory Logic
        - **STORM** — Deep Multi-Perspective Research
        
        **🌐 API:** 20 REST endpoints (FastAPI)
        """)
    
    # Platform stats
    st.divider()
    st.subheader("📊 Platform Stats")
    st.code(earth.platform_stats(), language=None)


# ═════════════════════════════════════════════════════════
# Page: Research Discovery
# ═════════════════════════════════════════════════════════

elif page == "🔍 Research Discovery":
    st.title("🔍 Intelligence Aggregator")
    st.markdown("Discover and aggregate AI research from **Arxiv**, **OpenReview**, and the web.")
    
    col_res1, col_res2 = st.columns([2, 1])
    
    with col_res1:
        topic = st.text_input("🔍 Topic to Research", "Large Language Model Agents 2025")
        count = st.slider("Count", 1, 10, 3)
    
    with col_res2:
        st.info("Uses **Serper** for search and **Firecrawl** for scraping real research papers.")

    if st.button("🚀 Discover & Aggregate", type="primary", use_container_width=True):
        with st.spinner(f"Searching and aggregating intelligence on '{topic}'..."):
            try:
                earth = get_earth()
                result = earth.discover_intelligence(topic)
                
                st.divider()
                st.success(f"Aggregated {result['total_papers']} intelligence pieces!")
                
                for i, piece in enumerate(result["intelligence_pieces"]):
                    with st.expander(f"📄 {piece['title']}", expanded=(i==0)):
                        st.markdown(f"**Source:** {piece['url']}")
                        st.markdown("---")
                        st.markdown("**Summary:**")
                        st.markdown(piece["summary"])
                        st.caption(f"Extraction method: {piece['source']}")
            except Exception as e:
                st.error(f"Discovery failed: {e}")

    st.divider()
    st.subheader("🧬 LEGO DNA Extractor (Digester)")
    st.markdown("Enter a paper URL to extract its structural logic and generate LEGO code.")
    
    col_dig1, col_dig2 = st.columns([2, 1])
    with col_dig1:
        paper_url = st.text_input("Paper URL (Arxiv/OpenReview)", "https://arxiv.org/html/2501.12941v1")
    with col_dig2:
        lego_name = st.text_input("LEGO Piece Name", "NewResearchPiece")

    if st.button("🧪 Digest Paper & Generate LEGO", type="secondary", use_container_width=True):
        with st.spinner("Digesting research... this may take up to 2 minutes."):
            try:
                earth = get_earth()
                result = earth.digest_research(paper_url, lego_name)
                
                st.success(f"Successfully digested {lego_name}!")
                
                tab1, tab2 = st.tabs(["🧬 Agentic DNA", "🐍 Generated LEGO Code"])
                with tab1:
                    st.json(result["dna"])
                with tab2:
                    st.code(result["lego_stub"], language="python")
            except Exception as e:
                st.error(f"Digestion failed: {e}")


# ═════════════════════════════════════════════════════════
# Page: Evolve
# ═════════════════════════════════════════════════════════

elif page == "🧬 Evolve":
    st.title("🧬 Self-Evolving Agent Core")
    st.markdown("Run the **7-phase evolution loop** to solve tasks using all LEGO pieces.")
    
    # Configuration
    col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
    
    with col_cfg1:
        task = st.text_area(
            "📝 Task Description",
            value="Analyze research papers about AI agents and generate a summary",
            height=100,
        )
    
    with col_cfg2:
        strategy = st.selectbox(
            "🎯 Strategy",
            ["hybrid", "prompt_optimize", "workflow_evolve", "agent_refine",
             "memory_augment", "graph_restructure"],
            index=0,
        )
        
        max_iterations = st.slider("🔄 Max Iterations", 1, 10, 3)
        quality_threshold = st.slider("📈 Quality Threshold", 0.0, 1.0, 0.8, 0.05)
    
    with col_cfg3:
        st.markdown("**Phases:**")
        phases = ["👁️ Observe", "📋 Plan", "⚡ Execute", "📊 Evaluate",
                   "🪞 Reflect", "🧬 Evolve", "💾 Remember"]
        for p in phases:
            st.markdown(f"- {p}")
    
    # Run button
    if st.button("🚀 Run Evolution", type="primary", use_container_width=True):
        core = get_evolve_core()
        core._quality_threshold = quality_threshold
        
        # Progress tracking
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        phase_names = {
            "observe": "👁️ Observing",
            "plan": "📋 Planning",
            "execute": "⚡ Executing",
            "evaluate": "📊 Evaluating",
            "reflect": "🪞 Reflecting",
            "evolve": "🧬 Evolving",
            "remember": "💾 Remembering",
        }
        
        phase_tracker = []
        
        def callback(phase, cycle):
            phase_tracker.append(phase.value)
            progress_text.text(
                f"Iteration {cycle.iteration}/{max_iterations} — "
                f"{phase_names.get(phase.value, phase.value)}"
            )
            total_phases = max_iterations * 7
            progress_bar.progress(min(len(phase_tracker) / total_phases, 1.0))
        
        result = core.evolve(
            task=task,
            max_iterations=max_iterations,
            strategy=strategy,
            callback=callback,
        )
        
        progress_bar.progress(1.0)
        progress_text.text("✅ Evolution complete!")
        
        # Results
        st.divider()
        st.subheader("📊 Results")
        
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        col_r1.metric("Iterations", result.iterations)
        col_r2.metric("Final Score", f"{result.final_metrics.overall_score():.4f}")
        col_r3.metric("Success", "✅" if result.success else "❌")
        col_r4.metric("Time", f"{result.total_elapsed:.2f}s")
        
        # Score progression
        st.subheader("📈 Score Progression")
        history = result.history
        if history:
            scores = [h["metrics"]["overall_score"] for h in history]
            iterations = [h["iteration"] for h in history]
            st.line_chart({"Score": scores}, use_container_width=True)
        
        # History details
        st.subheader("📜 Evolution History")
        for h in history:
            with st.expander(f"Iteration {h['iteration']} — Score: {h['metrics']['overall_score']:.4f}"):
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    st.json(h["metrics"])
                with col_h2:
                    st.caption(f"Phase: {h['phase']} | Strategy: {h['strategy']}")
    
    # Evolution core info
    st.divider()
    core = get_evolve_core()
    col_ei1, col_ei2 = st.columns(2)
    
    with col_ei1:
        st.subheader("🧠 Learned Strategies")
        strategies = core.learned_strategies()
        if strategies:
            st.json(strategies)
        else:
            st.info("No strategies learned yet. Run an evolution to start learning!")
    
    with col_ei2:
        st.subheader("ℹ️ Core Info")
        st.json(core.info())


# ═════════════════════════════════════════════════════════
# Page: LEGO Pieces
# ═════════════════════════════════════════════════════════

elif page == "🧱 LEGO Pieces":
    st.title("🧱 LEGO Pieces")
    st.markdown("Browse all **7 research papers** extracted into composable LEGO pieces.")
    
    earth = get_earth()
    info = earth.platform_info()
    
    # Piece selector
    piece_names = list(info["lego_pieces"].keys())
    selected = st.selectbox("Select LEGO Piece", piece_names, format_func=lambda x: x.upper())
    
    piece = info["lego_pieces"][selected]
    
    # Piece details
    st.divider()
    
    col_pd1, col_pd2, col_pd3 = st.columns(3)
    col_pd1.metric("📁 Files", piece["files"])
    col_pd2.metric("📝 Lines", f"{piece['lines']:,}")
    col_pd3.metric("✅ Tests", piece["tests"])
    
    st.markdown(f"**Source:** {piece['source']}")
    st.markdown(f"**Components:** {piece['components']}")
    
    # Source code browser
    st.divider()
    st.subheader("📂 Source Files")
    
    lego_base = os.path.join(os.path.dirname(__file__), 'ai_earth', 'lego')
    
    # Map piece names to directories
    dir_map = {
        "evoagentx": "evoagentx",
        "dspy": "dspy",
        "mem0": "mem0",
        "model_router": None,  # Single file
        "langgraph": "langgraph_src",
        "crewai": "crewai_src",
        "autogen": "autogen_src",
    }
    
    if selected == "model_router":
        router_path = os.path.join(os.path.dirname(__file__), 'model_router.py')
        if os.path.exists(router_path):
            with open(router_path) as f:
                st.code(f.read(), language="python")
    else:
        piece_dir = os.path.join(lego_base, dir_map.get(selected, selected))
        if os.path.exists(piece_dir):
            # Find Python files
            py_files = []
            for root, dirs, files in os.walk(piece_dir):
                # Skip __pycache__
                dirs[:] = [d for d in dirs if d != '__pycache__']
                for f in files:
                    if f.endswith('.py'):
                        rel_path = os.path.relpath(os.path.join(root, f), piece_dir)
                        py_files.append(rel_path)
            
            py_files.sort()
            
            if py_files:
                selected_file = st.selectbox("Browse files", py_files[:50])
                file_path = os.path.join(piece_dir, selected_file)
                
                if os.path.exists(file_path):
                    with open(file_path) as f:
                        content = f.read()
                    
                    line_count = len(content.split('\n'))
                    st.caption(f"{selected_file} — {line_count} lines")
                    st.code(content, language="python")


# ═════════════════════════════════════════════════════════
# Page: Chat
# ═════════════════════════════════════════════════════════

elif page == "💬 Chat":
    st.title("💬 LLM Chat")
    st.markdown("Chat with a real LLM via the **Model Router** (powered by OpenRouter + Key Pool).")
    
    router = get_router()
    
    # Model selection
    col_m1, col_m2 = st.columns([1, 3])
    
    with col_m1:
        models = router.list_models()
        model_names = [m["name"] for m in models]
        selected_model = st.selectbox("Model", model_names, index=0)
        
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 256, 8192, 2048, 256)
        
        st.divider()
        
        # Provider info
        providers = router.list_providers()
        st.subheader("Providers")
        for p, available in providers.items():
            icon = "🟢" if available else "🔴"
            st.markdown(f"{icon} **{p}**")
    
    with col_m2:
        # Chat interface
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Input
        if prompt := st.chat_input("Type your message..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = router.chat(
                            model=selected_model,
                            prompt=prompt,
                            temperature=temperature,
                            max_tokens=max_tokens,
                        )
                        st.markdown(response.content)
                        st.caption(
                            f"Model: {response.model} | "
                            f"Provider: {response.provider.value} | "
                            f"Latency: {response.latency_ms:.1f}ms | "
                            f"{'Cached ⚡' if response.cached else 'Live'}"
                        )
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": response.content}
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        # Clear button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
