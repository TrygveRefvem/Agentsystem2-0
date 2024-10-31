from ..base import BaseAgent
from app.services.openai import get_openai_response

class StoryAnalyst(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Historieanalytiker",
            description="Analyserer plotstruktur, karakterutvikling og narrative elementer."
        )

    async def respond(self, query: str, context: str = "") -> str:
        prompt = f"""Du er en ekspert på historieanalyse og narrativ struktur.
        Spørsmål: {query}
        {'Kontekst fra andre eksperter: ' + context if context else ''}
        Gi et kort, analytisk svar på 2-3 setninger."""
        
        return await get_openai_response(prompt)
