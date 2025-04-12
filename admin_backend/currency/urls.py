from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet

router = DefaultRouter()
router.register(r'', CurrencyViewSet, basename='currencies')

urlpatterns = [
    path('currencies/', include(router.urls)),
]
