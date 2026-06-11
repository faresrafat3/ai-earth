"""
🕸️ The Intelligence Graph Engine (v1.1.0)
═══════════════════════════════════════════════════════════
The Meta-Structure that maps relationships between research papers
to allow for Transitive Reasoning and Cross-Paper Logic.
"""

import logging
import networkx as nx
import json
import os
from typing import List, Dict, Any

logger = logging.getLogger("ai_earth.core.graph")

class IntelligenceGraph:
    def __init__(self, db_path="/home/user/ai-earth/data/intelligence_mesh.json"):
        self.db_path = db_path
        self.graph = nx.DiGraph()
        self._load()

    def add_paper(self, name: str, dna: Dict[str, Any]):
        """تضيف بحث كعقدة (Node) وتستنتج روابطها مع الأبحاث الحالية"""
        self.graph.add_node(name, **dna)
        
        # استنتاج روابط تلقائية (Heuristic Linking)
        for node in self.graph.nodes():
            if node == name: continue
            
            # ربط بناءً على الكلمات المفتاحية أو الأنماط
            node_data = self.graph.nodes[node]
            if str(dna.get('logic')).lower() in str(node_data.get('logic')).lower():
                self.graph.add_edge(name, node, relation="Logic_Extension")
                
        self._save()

    def find_cross_logic_path(self, start_node: str, end_node: str) -> List[str]:
        """تبحث عن طريق تفكير يربط بين بحثين مختلفين تماماً"""
        try:
            return nx.shortest_path(self.graph, start_node, end_node)
        except:
            return []

    def _save(self):
        data = nx.node_link_data(self.graph)
        with open(self.db_path, "w") as f:
            json.dump(data, f)

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                data = json.load(f)
                self.graph = nx.node_link_graph(data)

# Global Graph Instance
earth_graph = IntelligenceGraph()
