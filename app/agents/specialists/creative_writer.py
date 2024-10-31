from ..base import BaseAgent
from app.services.openai import get_openai_response

class CreativeWriter(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Kreativ Forfatter",
            description="Hjelper med karakterutvikling, plotstruktur og kreativ skriving."
        )

    async def respond(self, query: str, context: str = "") -> str:
        prompt = f"""Du er en erfaren forfatter og kreativ konsulent.
        Spørsmål: {query}
        {'Kontekst fra andre eksperter: ' + context if context else ''}
        Gi et kort, kreativt og konstruktivt svar på 2-3 setninger."""
        
        return await get_openai_response(prompt)
