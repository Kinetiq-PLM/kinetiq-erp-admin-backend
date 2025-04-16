# user_manage/views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import User, RolePermission
from .serializers import UserSerializer, RolePermissionSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user_id', 'first_name', 'last_name', 'email', 'employee_id']
    ordering_fields = ['created_at', 'first_name', 'last_name', 'email', 'status', 'type']
    ordering = ['first_name']  # Default ordering
    
    def perform_create(self, serializer):
        serializer.save()
            
    def perform_update(self, serializer):
        serializer.save()

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.exclude(role_name__startswith='ARCHIVED_')
    serializer_class = RolePermissionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['role_name', 'description']
    ordering_fields = ['role_name', 'permissions']
    ordering = ['role_name']  # Default ordering

    
    def perform_create(self, serializer):
            serializer.save()
            
    def perform_update(self, serializer):
            serializer.save()
            
    def perform_destroy(self, instance):
        # Check if already archived
        if not instance.role_name.startswith('ARCHIVED_'):
            User.objects.filter(role=instance).update(role=None)
            
            instance.role_name = f'ARCHIVED_{instance.role_name}'
            instance.save()

# Add an endpoint to view archived roles
    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_roles = RolePermission.objects.filter(role_name__startswith='ARCHIVED_')
        page = self.paginate_queryset(archived_roles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived_roles, many=True)
        return Response(serializer.data)
    
    # Add an endpoint to restore archived roles
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):
        role_id = pk
        role = get_object_or_404(RolePermission, role_id=role_id)

        if role.role_name.startswith('ARCHIVED_'):

                role.role_name = role.role_name[9:]  # Remove "ARCHIVED_" prefix
                role.save()

        serializer = self.get_serializer(role)
        return Response(serializer.data)