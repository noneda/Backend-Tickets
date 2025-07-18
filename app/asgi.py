import os
import django


# * This must be in this part so that the server with uvicorn can manage the processes... this is FIRST

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

django_asgi_application = get_asgi_application()

from core.channels import websocket_urlpatterns
from core.auth.middleware import OptionalTokenAuthMiddleware

application = ProtocolTypeRouter(
    {
        # * Http Protocol... This is a default App
        "http": django_asgi_application,
        # * WebSocket Protocol... There had a Channels
        "websocket": OptionalTokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
