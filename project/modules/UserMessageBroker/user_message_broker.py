from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import json


# Django uses python's built-in logging module to control server logs.
# Get the logger for your Django app
logger = logging.getLogger('project')


class UserMessageBroker(AsyncWebsocketConsumer):
    async def connect(self):
        """ 
        Usage: The 'connect' method is called by the user when they run the
               'connectToMessageBroker' function. 
        """
        await self.accept()
        await self.send("Hello from Server!")

    async def disconnect(self, close_code):
        # Logic for handling disconnects can go here.
        pass

    async def receive(self, text_data):
        """ 
        Usage: The recieve method is called when a user publishes a message. 
               Then, self.send() calls the notify function of the user.
        """
        # Handle published
        logger.info("Recieved data:" + text_data)
        await self.send("Server recieved your message.")
