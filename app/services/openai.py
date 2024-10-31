from openai import AzureOpenAI
from ..core.config import get_settings
from ..core.logging import logger
import asyncio
from typing import Optional

settings = get_settings()
client = AzureOpenAI(
    api_key=settings.azure_openai_api_key,
    api_version="2024-02-15-preview",
    azure_endpoint=settings.azure_openai_endpoint
)

async def get_openai_response(prompt: str, temperature: float = 0.1) -> str:
    try:
        response = await asyncio.to_thread(
            lambda: client.chat.completions.create(
                model=settings.azure_openai_deployment,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=800
            )
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return "Beklager, jeg kunne ikke generere et svar akkurat nå."
