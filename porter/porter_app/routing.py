# porter_app/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r'^ws/porter/user/booking/confirm/(?P<order_id>\d+)/(?P<distance>[\d.]+)/(?P<amount>[\d.]+)/(?P<time>[\d.]+)/$',
        consumers.BookingStatusConsumer.as_asgi()
    ),
]
