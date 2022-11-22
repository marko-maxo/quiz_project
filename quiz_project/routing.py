from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack, CookieMiddleware
from django.core.asgi import get_asgi_application

import ChatApp.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        CookieMiddleware(
            URLRouter(
                ChatApp.routing.urlpatterns
            )
        )
    )
})
