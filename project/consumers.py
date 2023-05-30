"""
Author: Ryan
Consume and initate requests from the client side
"""

import json
import project.modules.rmp_db_manager as db
from channels.generic.websocket import AsyncWebsocketConsumer

class ProfessorsPageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': db.getDB()
        }
        ))