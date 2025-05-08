from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessPartnerMasterViewSet

router = DefaultRouter()
router.register(r'partners', BusinessPartnerMasterViewSet)

urlpatterns = [
    path('partner-master/', include(router.urls))
]