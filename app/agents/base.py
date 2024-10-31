from typing import List, Dict, Any
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.context: List[Dict[str, str]] = []

    @abstractmethod
    async def respond(self, query: str, context: str = "") -> str:
        pass

    def add_to_context(self, message: Dict[str, str]):
        self.context.append(message)

    def clear_context(self):
        self.context = []
