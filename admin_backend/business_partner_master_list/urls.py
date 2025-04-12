from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessPartnerMasterViewSet, VendorViewSet

router = DefaultRouter()
router.register(r'partners', BusinessPartnerMasterViewSet)
router.register(r'vendors', VendorViewSet)

urlpatterns = [
    path('partner-master/', include(router.urls))
]