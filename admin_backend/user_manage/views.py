# user_manage/views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import User, RolePermission
from .serializers import UserSerializer, RolePermissionSerializer, RoleChoiceSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


# class StandardResultsSetPagination(PageNumberPagination):
#     """Customized pagination with larger page sizes for better performance"""
#     page_size = 50
#     page_size_query_param = 'page_size'
#     max_page_size = 200


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('role')  # Use select_related to reduce queries
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    # pagination_class = StandardResultsSetPagination
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user_id', 'first_name', 'last_name', 'email', 'employee_id', 'role__role_name', 'status']
    ordering_fields = ['user_id', 'first_name', 'last_name', 'email', 'employee_id', 'role__role_name', 'status', 'created_at', 'updated_at']
    ordering = ['-updated_at']  # Default ordering

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Return only active users with pagination"""
        active_users = self.get_queryset().filter(status='Active')
        
        page = self.paginate_queryset(active_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(active_users, many=True)
        return Response(serializer.data)
    
    
class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.exclude(role_name__startswith='ARCHIVED_')
    serializer_class = RolePermissionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    # pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['role_id', 'role_name', 'description']
    ordering_fields = ['role_name', 'description', 'role_id']
    ordering = ['role_name']  # Default ordering

    @action(detail=False, methods=['get'])
    def choices(self, request):
        """Return just role_id and role_name for dropdown menus - much lighter load"""
        roles = self.get_queryset().only('role_id', 'role_name')
        serializer = RoleChoiceSerializer(roles, many=True)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        # Check if already archived
        if not instance.role_name.startswith('ARCHIVED_'):
            User.objects.filter(role=instance).update(role=None)
            
            instance.role_name = f'ARCHIVED_{instance.role_name}'
            instance.save()

    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_roles = RolePermission.objects.filter(role_name__startswith='ARCHIVED_')

        # Apply filter backends manually
        for backend in list(self.filter_backends):
            archived_roles = backend().filter_queryset(self.request, archived_roles, self)

        page = self.paginate_queryset(archived_roles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(archived_roles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):
        role_id = pk
        role = get_object_or_404(RolePermission, role_id=role_id)

        if role.role_name.startswith('ARCHIVED_'):
            role.role_name = role.role_name[9:]  # Remove "ARCHIVED_" prefix
            role.save()

        serializer = self.get_serializer(role)
        return Response(serializer.data)
