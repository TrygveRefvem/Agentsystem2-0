from ..base import BaseAgent
from ...services.openai import get_openai_response

class Economist(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Økonom",
            description="Forklarer hvordan skatt påvirker inntektsfordeling og økonomisk stabilitet."
        )

    async def respond(self, query: str, context: str = "") -> str:
        prompt = f"""Du er en økonom.
        Spørsmål: {query}
        {'Kontekst fra andre eksperter: ' + context if context else ''}
        Gi et kort, presist svar på 2-3 setninger med fokus på økonomiske aspekter."""
        
        return await get_openai_response(prompt)
