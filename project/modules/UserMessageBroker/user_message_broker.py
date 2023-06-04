"""
    Title: The User's Message Broker
    Brief: This module establishes a connection between the user's interface and
           the internal system using websockets. The User's Message Broker can
           communicate to each user privately, and also broadcast user messages
           into the Grand Exchange.
    Author: Joseph.
"""
# ------------------------------ Module Imports ------------------------------ #
from channels.generic.websocket import AsyncWebsocketConsumer
from ..GrandExchange.grand_exchange import Component
import json  
import asyncio  # provides support for asynchronous tasks.


# ------------------------------ Logging Config ------------------------------ #
import logging
logger = logging.getLogger("project")


# --------------------------- Listening on Channels -------------------------- #
MESSAGE_BROKER_CHANNELS = ["a", "b"] 


# --------------------------- User's Message Broker -------------------------- #
class UserMessageBroker(AsyncWebsocketConsumer, Component):
    """
        Brief: The User's Message Broker establishes a websocket connection with
               users. When a user connects, a new instance of the User Message
               Broker is created. This enables the User Message Broker to send
               private messages to each connected client. The User Message Broker
               is connected to the Grand Exchange. As such, the User Message Broker
               can publish messages and receive notifications from the Grand Exchange.
    """
    def __init__(self):
        super(Component, self).__init__()
        super(AsyncWebsocketConsumer, self).__init__()
        super().__init__()
        self.subscribe_to_channels()

    def __str__(self):
        """ Print the UserMessageBroker more concisely """
        return f"UserMessageBroker {self.scope['user']}"

    def subscribe_to_channels(self):
        """ This is called upon initialization """
        for channel in MESSAGE_BROKER_CHANNELS:
            self.subscribe(channel)

    async def connect(self):
        """ This is called when the user runs 'connectToMessageBroker' """ 
        await self.accept()
        await self.send("Hello from Server!")

    async def disconnect(self, close_code):
        """ Remove reference to self from the Grand Exchange """
        for channel in MESSAGE_BROKER_CHANNELS:
            self.unsubscribe(channel)
        return None

    async def receive(self, text_data):
        """ This is called when the user publishes a message. """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as e:
             # Error: failed when trying to load the json string.
            err = malformed_json_str(text_data)
            await self.send(err)
            logger.warning(err)
            return None
        # The json string was successfully loaded.
        topic = data.get('topic')  # Use .get() to handle missing keys
        message = data.get('message')
        if topic is None or message is None:
            # Error: could not retrieve the topic and message.
            err = malformed_json_str(text_data)
            await self.send(err)
            logger.warning(err)
            return None
        # The json string was well-formed.
        # Publish topic and message to the Grand Exchange.
        self.publish(topic, message)  
        # Send a confirmation message back to the user (for debugging).
        await self.send("Server recieved your message.")

    def notify(self, topic: str, message: object):
        """ Do something when this component recieves a message. """
        message = f"topic = `{topic}` message = `{message}` -- from GE"

        # This is necessary because we're calling an asynchronous function
        # within a synchronous scope. What we're doing here is defining a 
        # coroutine function that can be executed asyncasynchronously.
        async def run_relay():
            await self.send(message)

        # Similar to promises, this schedules the asynchronous task for
        # execution at a later date.
        asyncio.create_task(run_relay())


# --------------------------------- Warnings --------------------------------- #
def malformed_json_str(json_str):
    warn_msg = "!!!!!!!\n"
    warn_msg += "WARNING: UserMessageBroker : user sent "
    warn_msg += f"malformed JSON string: `{json_str}`\n"
    warn_msg += "!!!!!!!"
    return warn_msg