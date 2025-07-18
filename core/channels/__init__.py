from django.urls import re_path
from core.consumers import TicketConsumer

websocket_urlpatterns = [
    re_path(r"ws/private/$", TicketConsumer.as_asgi()),
]
    