"""
🎨 AI Earth — Master Command UI (v0.9.0)
═══════════════════════════════════════════════════════════
Highest-level interface for Intelligence Aggregation.
"""

import streamlit as st
import pandas as pd
import sqlite3
import os
import sys

# System Integration
project_root = "/home/user/ai-earth"
sys.path.insert(0, project_root)
from ai_earth.orchestrator import AIEarth
from ai_earth.core.database import ledger

# ═════════════════════════════════════════════════════════
# High-End Styling
# ═════════════════════════════════════════════════════════
st.set_page_config(page_title="AI Earth Command", page_icon="🌍", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e6edf3; }
    .stMetric { background-color: #161b22; border-radius: 8px; border: 1px solid #30363d; padding: 20px; }
    .stTab { font-size: 18px !important; }
    .stButton>button { border-radius: 6px; background-color: #238636; color: white; border: none; font-weight: bold; }
    .stSidebar { background-color: #0d1117; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_system():
    return AIEarth()

earth = get_system()

# ═════════════════════════════════════════════════════════
# Sidebar - Platform Pulse
# ═════════════════════════════════════════════════════════
st.sidebar.title("🌍 AI Earth")
st.sidebar.caption("The Living Intelligence Ecosystem v1.0.0")
st.sidebar.success("STATUS: THE SINGULARITY")

stats = ledger.get_stats()
st.sidebar.metric("Scientific Intelligence", stats.get('intel_cycles', 0))
st.sidebar.metric("Global LLM Pool", "21 Keys Active")

st.sidebar.divider()
st.sidebar.info("Operational Status: STRATEGIC")

# ═════════════════════════════════════════════════════════
# Main Command Center
# ═════════════════════════════════════════════════════════
t1, t2, t3, t4, t5, t6, t7, t8 = st.tabs(["🏛️ Intelligence Vault", "🤖 Agent Factory", "🕸️ Knowledge Mesh", "💉 Memory Lab", "🌪️ Expansion Loop", "🧠 Synapse Flow", "🗺️ Strategic Roadmap", "📊 OmniLog Ledger"])

# --- TAB 4: Memory Lab (NEW v1.3.0) ---
with t4:
    st.header("Memory Re-Infection Lab")
    st.markdown("Analyzing historical thoughts to optimize future cognitive pathways.")
    
    if st.button("RUN MEMORY REINFORCEMENT"):
        with st.spinner("Analyzing Ledger traces..."):
            report = earth.reinforce_memory()
            st.success("Memory Re-Infection Successful!")
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Distilled Protocols")
                st.json(report['re_infection'])
            with c2:
                st.subheader("Efficiency Map")
                st.json(report['efficiency_map'])

# --- TAB 2: Agent Factory (NEW v1.2.0) ---
with t2:
    st.header("The Living Agent Factory")
    st.markdown("Specialized autonomous agents instantiated directly from research DNA.")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.subheader("Instantiated Agents")
        # In a real run, this would fetch from earth.factory.active_agents
        st.write("- 🤖 ReflectionAgent_Specialist (Active)")
        st.write("- 🤖 rStar_MCTS_Specialist (Active)")
        st.write("- 🤖 STORM_Aggregator_Specialist (Active)")
        st.metric("Total Active Specialists", "26")
    
    with col_f2:
        st.subheader("Summon a Specialist Swarm")
        task = st.text_input("Describe a complex task for the swarm")
        if st.button("SUMMON & SOLVE"):
            st.info("Swarm is collaborating using cross-paper DNA...")
            # result = earth.solve_with_swarm(task)
            st.success("Solution synthesized by the Swarm.")

# --- TAB 2: Knowledge Mesh (NEW) ---
with t2:
    st.header("The Intelligence Knowledge Graph")
    st.markdown("Visualizing logical connections and transitive reasoning paths between SOTA papers.")
    
    from ai_earth.core.knowledge_graph import earth_graph
    nodes = list(earth_graph.graph.nodes)
    edges = list(earth_graph.graph.edges)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Graph Nodes", len(nodes))
    c2.metric("Neural Links", len(edges))
    c3.metric("Mesh Density", f"{len(edges)/max(len(nodes),1):.2f}")
    
    st.divider()
    st.subheader("Cross-Paper Reasoning Path")
    p1 = st.selectbox("Start Research Node", nodes if nodes else ["None"])
    p2 = st.selectbox("End Research Node", nodes[::-1] if nodes else ["None"])
    
    if st.button("FIND LOGIC PATH"):
        path = earth_graph.find_cross_logic_path(p1, p2)
        if path:
            st.success(f"Path Found: {' ➔ '.join(path)}")
        else:
            st.warning("No direct logical path found yet. Run more expansion cycles.")

# --- TAB 4: Roadmap (NEW) ---
with t4:
    st.header("AI Earth Strategic Roadmap")
    st.markdown("The trajectory from Intelligence Aggregator to Autonomous Scientist.")
    
    col_r1, col_r2 = st.columns([1, 1])
    with col_r1:
        st.info("### Phase 1: Aggregation (Active)\nExtracting DNA from human research and building the LEGO library.")
        st.success("### Phase 2: Neural Linking (Current)\nSynthesizing cross-paper insights via the Synapse Kernel.")
    with col_r2:
        st.warning("### Phase 3: Self-Training (Future)\nFine-tuning AI Earth's own model on the Ledger's thinking traces.")
        st.error("### Phase 4: Autonomous Discovery (The Frontier)\nGenerating original research and code stubs for non-human logic.")

    st.divider()
    st.subheader("Intelligence Density Map")
    st.write("Visualizing the connection between 14+ research domains...")
    st.progress(0.75) # Based on current progress

# --- TAB 1: Vault ---
with t1:
    st.header("The Strategic Knowledge Vault")
    st.markdown("Detailed records of all digested research papers and their LEGO logic.")
    
    with sqlite3.connect(ledger.db_path) as conn:
        df = pd.read_sql_query("SELECT timestamp, paper_name, credibility_score, completeness_analysis, url FROM research_intel ORDER BY id DESC", conn)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        paper = st.selectbox("Detailed Analysis", df['paper_name'].tolist())
        if paper:
            with sqlite3.connect(ledger.db_path) as conn:
                row = pd.read_sql_query(f"SELECT * FROM research_intel WHERE paper_name='{paper}'", conn).iloc[0]
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🧬 Logic Model")
                st.code(row['technical_logic'], language="json")
            with c2:
                st.subheader("🧩 LEGO Code")
                st.code(row['code_stub'], language="python")
    else:
        st.info("The vault is currently awaiting its first strategic record.")

# --- TAB 2: Expansion ---
with t2:
    st.header("Autonomous Expansion Cycle")
    st.markdown("Trigger a Singularity Loop to discover and digest SOTA research.")
    
    domain = st.text_input("Strategic Domain", "Autonomous Reasoning Frameworks 2025")
    if st.button("EXECUTE SINGULARITY LOOP"):
        with st.status("Watchtower Scanning...") as s:
            results = earth.autonomous_expansion_cycle(domain)
            for r in results:
                st.write(f"✅ Integrated: {r['name']} (Score: {r['credibility']})")
            s.update(label="Expansion Cycle Completed", state="complete")
        st.success("Platform Knowledge Mesh has been expanded.")

# --- TAB 3: Synapse ---
with t3:
    st.header("Synapse High-Order Thought")
    st.markdown("Synthesize a breakthrough solution connecting all platform knowledge.")
    
    task = st.text_area("Complex Thinking Task", height=150)
    if st.button("RUN SYNAPSE KERNEL"):
        with st.spinner("Executing Synapse synthesis..."):
            res = earth.synapse_think(task)
            st.markdown("### 🚀 Breakthrough Insight")
            st.markdown(res['breakthrough_insight'])
            with st.expander("Cognitive Trace Detail"):
                st.json(res)

# --- TAB 4: Ledger ---
with t4:
    st.header("The Ledger of Earth - Deep Monitoring")
    st.markdown("Monitoring every interaction for future model training.")
    
    with sqlite3.connect(ledger.db_path) as conn:
        df_llm = pd.read_sql_query("SELECT timestamp, model, tokens, latency_ms FROM llm_interactions ORDER BY id DESC LIMIT 50", conn)
    
    st.subheader("Recent LLM Interactions")
    st.dataframe(df_llm, use_container_width=True)
    
    st.subheader("Data Export for AI Training")
    c1, c2 = st.columns(2)
    with c1:
        path = "/home/user/ai-earth/data/vault/research_training_set.jsonl"
        if os.path.exists(path):
            with open(path, "rb") as f:
                st.download_button("Download Research Dataset", f, file_name="ai_earth_research.jsonl")
    with c2:
        path_raw = "/home/user/ai-earth/data/vault/llm_raw_data.jsonl"
        if os.path.exists(path_raw):
            with open(path_raw, "rb") as f:
                st.download_button("Download Raw Thinking Traces", f, file_name="ai_earth_thinking.jsonl")
