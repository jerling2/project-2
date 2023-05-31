from channels.generic.websocket import AsyncWebsocketConsumer
from ..GrandExchange.grand_exchange import Component
import logging
import json
import asyncio

logger = logging.getLogger("project")

# Django uses python's built-in logging module to control server logs.

MESSAGE_BROKER_CHANNELS = ["a", "b"]

class UserMessageBroker(AsyncWebsocketConsumer, Component):
    def __init__(self):
        super(Component, self).__init__()
        super(AsyncWebsocketConsumer, self).__init__()
        super().__init__()
        # Component.__init__(self)
        # AsyncWebsocketConsumer.__init__(self)
        self.subscribe_to_channels()

    def __str__(self):
        return f"UserMessageBroker {self.scope['user']}"

    def subscribe_to_channels(self):
        for channel in MESSAGE_BROKER_CHANNELS:
            self.subscribe(channel)

    async def connect(self):
        """ 
        Usage: The 'connect' method is called by the user when they run the
               'connectToMessageBroker' function. 
        """
        await self.accept()
        await self.send("Hello from Server!")

    async def disconnect(self, close_code):
        # Clean up.
        for channel in MESSAGE_BROKER_CHANNELS:
            self.unsubscribe(channel)
        return None

    async def receive(self, text_data):
        """ 
        Usage: The recieve method is called when a user publishes a message. 
               Then, self.send() calls the notify function of the user.
        """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as e:
            err = malformed_json_str(text_data)
            await self.send(err)
            logger.warning(err)
            return None
        
        topic = data.get('topic')  # Use .get() to handle missing keys
        message = data.get('message')
            
        if topic is None or message is None:
            err = malformed_json_str(text_data)
            await self.send(err)
            logger.warning(err)
            return None

        self.publish(topic, message)
        await self.send("Server recieved your message.")



    def notify(self, topic: str, message: object):
        """ Do something when this component recieves a message. """
        msg = f"topic = `{topic}` message = `{message}` -- from GE"

        # This is necessary because we're calling an asynchronous function
        # within a synchronous scope. What we're doing here is defining a 
        # coroutine function that can be executed asyncasynchronously.
        async def run_relay():
            await self.send(msg)

        # Similar to promises, this schedules the asynchronous task for
        # execution at a later date.
        asyncio.create_task(run_relay())


# Warnings
def malformed_json_str(json_str):
    warn_msg = "!!!!!!!\n"
    warn_msg += "WARNING: UserMessageBroker : user sent "
    warn_msg += f"malformed JSON string: `{json_str}`\n"
    warn_msg += "!!!!!!!"
    return warn_msg