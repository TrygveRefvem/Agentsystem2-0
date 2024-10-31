from typing import List, Dict
from .base import BaseAgent
from app.services.openai import get_openai_response

class DynamicAgent(BaseAgent):
    def __init__(self, name: str, description: str, expertise: str, instructions: List[str]):
        super().__init__(name=name, description=description)
        self.expertise = expertise
        self.instructions = instructions

    async def respond(self, query: str, context: str = "") -> str:
        instructions_text = "\n".join(f"{i+1}. {instr}" for i, instr in enumerate(self.instructions))

        # Define the context input separately to avoid nested f-string
        context_input = f"Input fra andre eksperter:\n{context}" if context else ""

        # Use a standard f-string to build the prompt
        prompt = f"""Du er en ekspert på {self.expertise}.
        
OPPGAVE:
{self.description}

KONTEKST:
Spørsmål: {query}
{context_input}

INSTRUKSJONER:
{instructions_text}

Ditt svar:"""
        
        return await get_openai_response(prompt)

class AgentGenerator:
    async def analyze_question(self, query: str) -> List[Dict]:
        """Analyze the question and determine needed types of expertise"""
        prompt = f"""
Analyser følgende spørsmål og identifiser 2-4 ekspertroller som trengs for å gi et godt svar.
For hver ekspert, gi:
1. En presis tittel
2. En kort beskrivelse av deres ekspertise
3. Deres spesifikke fokusområde
4. 3-5 spesifikke instruksjoner for hvordan de skal svare

Spørsmål: {query}

Svar i følgende JSON-format:
{{
    "experts": [
        {{
            "name": "ekspertnavn",
            "description": "kort beskrivelse",
            "expertise": "spesifikt fokusområde",
            "instructions": ["instruks1", "instruks2", "instruks3"]
        }}
    ]
}}
"""
        
        response = await get_openai_response(prompt, temperature=0.1)
        try:
            import json
            result = json.loads(response)
            return result['experts']
        except Exception as e:
            print(f"Error parsing expert response: {e}")
            return []

    async def create_agents(self, query: str) -> List[DynamicAgent]:
        """Create dynamic agents based on question analysis"""
        expert_specs = await self.analyze_question(query)
        return [
            DynamicAgent(
                name=spec['name'],
                description=spec['description'],
                expertise=spec['expertise'],
                instructions=spec['instructions']
            )
            for spec in expert_specs
        ]

if __name__ == "__main__":
    import asyncio
    async def main():
        agent_generator = AgentGenerator()
        query = input("Enter your question: ")
        agents = await agent_generator.create_agents(query)
        for agent in agents:
            print(f"\nAgent: {agent.name}\nDescription: {agent.description}\nExpertise: {agent.expertise}\nInstructions: {agent.instructions}\n")
            response = await agent.respond(query)
            print(f"Response: {response}\n")

    asyncio.run(main())
