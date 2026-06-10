"""
🔍 Research Discovery Tool
═══════════════════════════════════════════════════════════
Discovers and aggregates AI research from the web.
Uses Serper for search and Firecrawl for scraping.
"""

from typing import List, Dict, Any
import logging
from ai_earth.model_router import ModelRouter

logger = logging.getLogger("ai_earth.research_discovery")

class ResearchDiscovery:
    def __init__(self, router: ModelRouter = None):
        self.router = router or ModelRouter()

    def discover_papers(self, topic: str, count: int = 5) -> List[Dict[str, Any]]:
        """Search for papers on a given topic."""
        query = f"latest AI research papers on {topic} site:arxiv.org OR site:openreview.net"
        search_results = self.router.web_search(query, num_results=count)
        
        papers = []
        for res in search_results:
            paper = {
                "title": res["title"],
                "url": res["link"],
                "snippet": res["snippet"],
                "source": "web_search"
            }
            papers.append(paper)
        return papers

    def summarize_paper(self, url: str) -> str:
        """Crawl a paper and summarize it."""
        content = self.router.crawl(url)
        if len(content) < 100:
            return "Failed to extract meaningful content from the paper."
        
        prompt = f"Summarize the following AI research paper content in a concise way, highlighting the key contributions and methodology:\n\n{content[:8000]}"
        summary = self.router.ask(prompt, model="gpt-4o-mini")
        return summary

    def aggregate_intelligence(self, topic: str) -> Dict[str, Any]:
        """Aggregate intelligence on a topic: discover, crawl, and summarize."""
        papers = self.discover_papers(topic, count=3)
        aggregated = []
        
        for paper in papers:
            logger.info(f"Summarizing: {paper['title']}")
            summary = self.summarize_paper(paper['url'])
            paper['summary'] = summary
            aggregated.append(paper)
            
        return {
            "topic": topic,
            "intelligence_pieces": aggregated,
            "total_papers": len(aggregated)
        }
