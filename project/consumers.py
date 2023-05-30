"""
Author: Ryan
Consume and initate requests from the client side
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProfessorsPageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }
        ))
