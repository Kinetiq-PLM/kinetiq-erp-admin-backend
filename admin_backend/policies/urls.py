from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PoliciesViewSet

router = DefaultRouter()
router.register(r'', PoliciesViewSet, basename='policies')

urlpatterns = [
    path('policies/', include(router.urls)),
]
