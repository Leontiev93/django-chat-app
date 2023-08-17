"""
ASGI config for djangochat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangochat.settings')

asgi_application = get_asgi_application() #new

import chat.routing #new

application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": URLRouter(chat.routing.websocket_urlpatterns) 
                       })