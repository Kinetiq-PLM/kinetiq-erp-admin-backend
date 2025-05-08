from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VendorViewSet, 
    ItemMasterDataViewSet
)

router = DefaultRouter()
router.register(r'item-master', ItemMasterDataViewSet)
router.register(r'vendor', VendorViewSet)

urlpatterns = [
    path('item-master/', include(router.urls)),
]