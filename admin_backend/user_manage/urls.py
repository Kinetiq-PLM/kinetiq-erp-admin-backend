from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RolePermissionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RolePermissionViewSet)

urlpatterns = [
    path('manage/', include(router.urls)),
]