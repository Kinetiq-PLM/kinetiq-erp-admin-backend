from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssetsViewSet, PoliciesViewSet, VendorViewSet, 
    ProductsViewSet, RawMaterialsViewSet, ItemMasterDataViewSet
)

router = DefaultRouter()
router.register(r'assets', AssetsViewSet)
router.register(r'products', ProductsViewSet)
router.register(r'raw-materials', RawMaterialsViewSet)
router.register(r'item-master', ItemMasterDataViewSet)

urlpatterns = [
    path('item-master/', include(router.urls)),
]