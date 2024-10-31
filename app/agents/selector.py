from typing import List, Dict
from app.core.logging import logger
from .specialists.tax_expert import TaxExpert
from .specialists.economist import Economist
from .specialists.creative_writer import CreativeWriter
from .specialists.story_analyst import StoryAnalyst
from app.services.openai import get_openai_response

class AgentSelector:
    def __init__(self):
        self.available_agents = {
            "Skatteekspert": TaxExpert(),
            "Økonom": Economist(),
            "Kreativ Forfatter": CreativeWriter(),
            "Historieanalytiker": StoryAnalyst(),
        }

    async def analyze_query_type(self, query: str) -> List[str]:
        prompt = f"""
        Analyser dette spørsmålet og returner en liste over de mest relevante ekspertene fra følgende alternativer:
        - Skatteekspert (for spørsmål om skatt og offentlig finansiering)
        - Økonom (for økonomiske spørsmål)
        - Kreativ Forfatter (for spørsmål om skriving og kreativt innhold)
        - Historieanalytiker (for spørsmål om plot og narrativ)

        Spørsmål: {query}

        Velg kun de 2-3 mest relevante ekspertene for dette spørsmålet. Svar i følgende format:
        ekspert1|ekspert2|ekspert3
        """
        response = await get_openai_response(prompt, temperature=0.1)
        return [expert.strip() for expert in response.split('|')]

    async def suggest_agents(self, query: str, analysis: Dict) -> List[Dict]:
        logger.info(f"Finding relevant agents for query: {query}")
        relevant_experts = await self.analyze_query_type(query)
        
        return [
            {"role": agent.name, "description": agent.description}
            for name, agent in self.available_agents.items()
            if agent.name in relevant_experts
        ]

    def get_agent(self, name: str):
        for agent in self.available_agents.values():
            if agent.name == name:
                return agent
        logger.warning(f"Agent not found: {name}")
        return None
