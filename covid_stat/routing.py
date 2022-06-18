from django.urls import re_path
from . import consumers
from chat_app.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/covid/(?P<room_name>\w+)/$', consumers.CovidStatsConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]
