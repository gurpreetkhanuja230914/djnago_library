import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import porter_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'porter.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
           porter_app.routing.websocket_urlpatterns
        )
    ),
})
