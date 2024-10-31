from ..base import BaseAgent
from ...services.openai import get_openai_response

class TaxExpert(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Skatteekspert",
            description="Gir innsikt i skattesystemets formål og hvordan det finansierer offentlige tjenester."
        )

    async def respond(self, query: str, context: str = "") -> str:
        prompt = f"""Du er en skatteekspert.
        Spørsmål: {query}
        {'Kontekst fra andre eksperter: ' + context if context else ''}
        Gi et kort, presist svar på 2-3 setninger med fokus på skattens formål og funksjon."""
        
        return await get_openai_response(prompt)
