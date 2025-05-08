from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Notifications, NotificationsStatusEnum
from .serializers import NotificationsSerializer
from rest_framework.filters import BaseFilterBackend

class ToUserIdFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        to_user_id = request.query_params.get('to_user_id')
        if to_user_id:
            return queryset.filter(to_user_id=to_user_id)
        return queryset

class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, ToUserIdFilter]
    search_fields = ['notifications_id', 'module', 'to_user_id', 'message', 'notifications_status']
    ordering_fields = ['created_at', 'notifications_id', 'module', 'to_user_id', 'notifications_status', 'message']
    ordering = ['-created_at']  # Default ordering by created_at descending