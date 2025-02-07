"""
ASGI config for djangochat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chat import routing
from middleware import TokenAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangochat.settings')

asgi_application = get_asgi_application()


application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": AllowedHostsOriginValidator( 
                TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns)))
})
