import os
import django


# * This must be in this part so that the server with uvicorn can manage the processes... this is FIRST
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from core.channels import websocket_urlpatterns
from core.auth.middleware import OptionalTokenAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": OptionalTokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
