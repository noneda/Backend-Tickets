import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from core.channels import websocket_urlpatterns
from core.auth.middleware import OptionalTokenAuthMiddleware


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": OptionalTokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
