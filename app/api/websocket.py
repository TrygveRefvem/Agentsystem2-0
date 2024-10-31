from fastapi import WebSocket
from typing import List, Dict, Optional
import json
from app.services.dialogue import DialogueManager
from app.core.logging import logger

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.dialogue_manager = DialogueManager()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Client connected")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info("Client disconnected")

    async def process_message(self, websocket: WebSocket, data: dict):
        try:
            if data.get('type') == 'continue_dialogue':
                logger.info("Processing continue_dialogue request")
                await self.handle_dialogue(
                    websocket,
                    data.get('agents', []),
                    data.get('query', '')
                )
            else:
                logger.info("Processing initial query")
                await self.analyze_query(websocket, data.get('query', ''))
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "message": "En feil oppstod under behandlingen av forespørselen"
            })

    async def analyze_query(self, websocket: WebSocket, query: str):
        agents = await self.dialogue_manager.agent_selector.suggest_agents(query, {})
        await websocket.send_json({
            "type": "suggested_agents",
            "agents": agents
        })

    async def handle_dialogue(self, websocket: WebSocket, selected_agents: List[str], query: str):
        logger.info(f"Starting dialogue with agents: {selected_agents}")
        dialogue_state = []
        
        try:
            # Initial responses
            for agent in selected_agents:
                response = await self.dialogue_manager.get_agent_response(agent, query)
                dialogue_state.append({
                    "type": "initial-response",
                    "agent": agent,
                    "content": response
                })
                await websocket.send_json({
                    "type": "dialogue_update",
                    "data": dialogue_state
                })

            # Cross-responses
            for agent in selected_agents:
                other_responses = [d for d in dialogue_state if d["agent"] != agent]
                context = "\n".join([f"{r['agent']}: {r['content']}" for r in other_responses])
                response = await self.dialogue_manager.get_agent_response(agent, query, context)
                dialogue_state.append({
                    "type": "response-to-response",
                    "agent": agent,
                    "content": response
                })
                await websocket.send_json({
                    "type": "dialogue_update",
                    "data": dialogue_state
                })

            # Build consensus
            consensus = await self.dialogue_manager.build_consensus(
                [d for d in dialogue_state if d["type"] == "response-to-response"],
                query
            )
            dialogue_state.append({
                "type": "consensus",
                "agent": "Konsensus",
                "content": consensus
            })
            await websocket.send_json({
                "type": "dialogue_update",
                "data": dialogue_state
            })

        except Exception as e:
            logger.error(f"Error in dialogue: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "message": "En feil oppstod under agent-dialogen"
            })
