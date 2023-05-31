"""
    This file routes the websocket's url to the AsyncWebsocketConsumer classes.
"""

from django.urls import re_path
from . import user_message_broker

websocket_urlpatterns = [
    re_path(r'ws/messagebroker/$', user_message_broker.UserMessageBroker.as_asgi()),
]