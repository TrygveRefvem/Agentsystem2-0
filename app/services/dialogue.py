from typing import List, Dict
from ..agents.selector import AgentSelector
from ..core.logging import logger
from .openai import get_openai_response

class DialogueManager:
    def __init__(self):
        self.agent_selector = AgentSelector()

    async def get_agent_response(self, agent_name: str, query: str, context: str = "") -> str:
        logger.info(f"Getting response from {agent_name}")
        agent = self.agent_selector.get_agent(agent_name)
        if not agent:
            return f"Agent {agent_name} not found"
        return await agent.respond(query, context)

    async def build_consensus(self, responses: List[Dict], query: str) -> str:
        responses_text = "\n".join([f"{r['agent']}: {r['content']}" for r in responses])
        prompt = f"""
        Basert på følgende ekspertuttalelser, lag en kort konsensus på 2-3 setninger:
        
        Spørsmål: {query}
        
        Ekspertuttalelser:
        {responses_text}
        
        Gi en kort og presis oppsummering som representerer en felles forståelse.
        """
        logger.info("Building consensus")
        return await get_openai_response(prompt, temperature=0.1)
