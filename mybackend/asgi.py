import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import E_commerce.routing  # Import your app's routing.py

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mybackend.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            E_commerce.routing.websocket_urlpatterns  # Match WebSocket routes
        )
    ),
})
