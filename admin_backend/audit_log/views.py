# views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import AuditLog
from .serializers import AuditLogSerializer
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


class LargeTablePagination(PageNumberPagination):
    """Custom pagination class optimized for large datasets"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    http_method_names = ['get']
    # pagination_class = LargeTablePagination
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['log_id', 'action', 'ip_address', 'user__username']
    ordering_fields = ['timestamp', 'log_id', 'user_id', 'action', 'ip_address']
    ordering = ['-timestamp']  # Default ordering by timestamp descending

    def get_queryset(self):
        """Optimize queryset based on filters"""
        queryset = super().get_queryset()

        params = self.request.query_params

        # Filter by start_date
        start_date = params.get('start_date')
        if start_date:
            try:
                queryset = queryset.filter(timestamp__gte=start_date)
            except ValueError:
                pass  # Invalid date format

        # Filter by end_date
        end_date = params.get('end_date')
        if end_date:
            try:
                queryset = queryset.filter(timestamp__lte=end_date)
            except ValueError:
                pass  # Invalid date format

        # Filter by user_id
        user_id = params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        # Filter by action_type
        action_type = params.get('action_type')
        if action_type:
            queryset = queryset.filter(action__icontains=action_type)

        # If no filters applied, default to last 7 days
        if not any([start_date, end_date, user_id, action_type]):
            seven_days_ago = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(timestamp__gte=seven_days_ago)

        return queryset
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Return only most recent logs (last 24 hours)"""
        one_day_ago = timezone.now() - timedelta(days=1)
        recent_logs = self.get_queryset().filter(timestamp__gte=one_day_ago)
        
        page = self.paginate_queryset(recent_logs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(recent_logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Return total count of audit logs in the last 30 days"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) AS total_count
                FROM "admin"."audit_log"
                WHERE timestamp >= %s
            """, [thirty_days_ago])
            
            row = cursor.fetchone()
            result = {
                'total_count': row[0]
            }
            
        return Response(result)