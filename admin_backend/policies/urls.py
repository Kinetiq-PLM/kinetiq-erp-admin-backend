from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PoliciesViewSet

router = DefaultRouter()
router.register(r'', PoliciesViewSet, basename='policies')

urlpatterns = [
    path('policies/', include(router.urls)),
    path('debug-file/<str:filename>/', PoliciesViewSet.debug_file_path, name='debug_file_path'),
]
