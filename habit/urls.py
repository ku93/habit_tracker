from django.urls import include, path
from rest_framework import routers

from .views import (HabitViewSet, PublicHabitViewSet, TelegramConnectView,
                    TelegramWebhookView)

router = routers.DefaultRouter()
router.register(r"habit", HabitViewSet)
router.register(r"public-habits", PublicHabitViewSet, basename="public-habits")

urlpatterns = [
    path("", include(router.urls)),
    path("connect/", TelegramConnectView.as_view(), name="telegram-connect"),
    path("webhook/", TelegramWebhookView.as_view(), name="telegram-webhook"),
]
