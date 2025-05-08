from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationsViewSet

router = DefaultRouter()
router.register(r'', NotificationsViewSet, basename='notifications')

urlpatterns = [
    path('notifications/', include(router.urls)),
]