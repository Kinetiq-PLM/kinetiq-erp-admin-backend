from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, RolePermission, UserForm, RolePermissionForm
from .serializers import UserSerializer, RolePermissionSerializer
from django.db import connection
from django.utils import timezone
import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

# Web views (unchanged)
@login_required
def dashboard(request):
    """Main dashboard view that displays users by default"""
    return redirect('user_manage:user_list')

@login_required
def user_list(request):
    """View to display all users in a table format"""
    search_query = request.GET.get('search', '')
    
    sort_field = request.GET.get('sort', 'first_name')
    sort_direction = request.GET.get('direction', 'asc')
    
    # Base queryset
    users = User.objects.all()
    
    # Apply search if provided
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(employee_id__icontains=search_query)
        )
    
    # Apply sorting
    order_by = sort_field
    if sort_direction == 'desc':
        order_by = f'-{sort_field}'
    
    # Handle special case for name sorting (uses first_name)
    if sort_field == 'name':
        order_by = 'first_name' if sort_direction == 'asc' else '-first_name'
    elif sort_field == 'role':
        order_by = 'role__role_name' if sort_direction == 'asc' else '-role__role_name'
    elif sort_field == 'status':
        if sort_direction == 'asc':
            order_by = ['status', 'first_name']
        else:
            order_by = ['-status', 'first_name']
    
    users = users.order_by(*order_by) if isinstance(order_by, list) else users.order_by(order_by)
    
    return render(request, 'user_manage/user_list.html', {
        'users': users,
        'active_tab': 'users',
        'active_app': 'user_manage',
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_direction': sort_direction
    })

@login_required
def role_list(request):
    """View to display all roles in a table format"""
    search_query = request.GET.get('search', '')
    sort_field = request.GET.get('sort', 'role_name')
    sort_direction = request.GET.get('direction', 'asc')
    
    # Base queryset
    roles = RolePermission.objects.all()
    
    # Apply search if provided
    if search_query:
        roles = roles.filter(
            Q(role_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Apply sorting
    order_by = sort_field
    if sort_direction == 'desc':
        order_by = f'-{sort_field}'

    if sort_field == 'access_level':
        if sort_direction == 'asc':
            order_by = ['access_level', 'role_name']
        else:
            order_by = ['-access_level', 'role_name']
    
    roles = roles.order_by(*order_by) if isinstance(order_by, list) else roles.order_by(order_by)
    
    return render(request, 'user_manage/role_list.html', {
        'roles': roles,
        'active_tab': 'roles',
        'active_app': 'user_manage',
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_direction': sort_direction
    })

@login_required
def add_user(request):
    """View to add a new user"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create a user instance but don't save to DB yet
            user = form.save(commit=False)
            
            # Create serializer to validate the data
            serializer = UserSerializer(data={
                'employee_id': user.employee_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password,
                'role': user.role.role_id if user.role else None,
                'status': user.status,
                'type': user.type
            })
            
            if serializer.is_valid():
                # Generate a temporary ID for the user object
                user.user_id = str(uuid.uuid4())
                
                # Use raw SQL for inserting
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO admin.users 
                        (employee_id, first_name, last_name, email, password, role_id, status, type, created_at, updated_at) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        RETURNING user_id
                        """,
                        [
                            user.employee_id, user.first_name, user.last_name, user.email, user.password,
                            user.role_id if user.role else None, user.status, user.type,
                            timezone.now(), timezone.now()
                        ]
                    )
                    # Get the generated ID
                    user.user_id = cursor.fetchone()[0]
                
                messages.success(request, f'User {user.first_name} {user.last_name} has been added successfully.')
                return redirect('user_manage:user_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = UserForm()
    
    return render(request, 'user_manage/user_form.html', {
        'form': form,
        'title': 'Add New User',
        'active_tab': 'users',
        'active_app': 'user_manage'  # Add this line
    })

@login_required
def edit_user(request, user_id):
    """View to edit an existing user"""
    user = get_object_or_404(User, user_id=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            # Update user fields but don't save to DB yet
            user = form.save(commit=False)
            
            # Validate with serializer
            serializer = UserSerializer(user, data={
                'employee_id': user.employee_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password,
                'role': user.role.role_id if user.role else None,
                'status': user.status,
                'type': user.type
            }, partial=True)
            
            if serializer.is_valid():
                # Use raw SQL for updating
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE admin.users SET 
                        employee_id = %s, first_name = %s, last_name = %s, email = %s, 
                        password = %s, role_id = %s, status = %s, type = %s, updated_at = %s
                        WHERE user_id = %s
                        """,
                        [
                            user.employee_id, user.first_name, user.last_name, user.email, user.password,
                            user.role_id if user.role else None, user.status, user.type, timezone.now(),
                            user.user_id
                        ]
                    )
                
                messages.success(request, f'User {user.first_name} {user.last_name} has been updated successfully.')
                return redirect('user_manage:user_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = UserForm(instance=user)
    
    return render(request, 'user_manage/user_form.html', {
        'form': form,
        'title': 'Edit User',
        'active_tab': 'users',
        'active_app': 'user_manage'  # Add this line
    })

@login_required
def add_role(request):
    """View to add a new role"""
    if request.method == 'POST':
        form = RolePermissionForm(request.POST)
        if form.is_valid():
            # Create a role instance but don't save to DB yet
            role = form.save(commit=False)
            
            # Validate with serializer
            serializer = RolePermissionSerializer(data={
                'role_name': role.role_name,
                'description': role.description,
                'permissions': role.permissions,
                'access_level': role.access_level
            })
            
            if serializer.is_valid():
                # Generate a temporary ID for the role object
                role.role_id = str(uuid.uuid4())
                
                # Use raw SQL for inserting
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO admin.roles_permission (role_name, description, permissions, access_level) VALUES (%s, %s, %s, %s) RETURNING role_id",
                        [role.role_name, role.description, role.permissions, role.access_level]
                    )
                    # Get the generated ID
                    role.role_id = cursor.fetchone()[0]
                
                messages.success(request, f'Role {role.role_name} has been added successfully.')
                return redirect('user_manage:role_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = RolePermissionForm()
    
    return render(request, 'user_manage/role_form.html', {
        'form': form,
        'title': 'Add New Role',
        'active_tab': 'roles',
        'active_app': 'user_manage'  # Add this line
    })

@login_required
def edit_role(request, role_id):
    """View to edit an existing role"""
    role = get_object_or_404(RolePermission, role_id=role_id)
    
    if request.method == 'POST':
        form = RolePermissionForm(request.POST, instance=role)
        if form.is_valid():
            # Update role fields but don't save to DB yet
            role = form.save(commit=False)
            
            # Validate with serializer
            serializer = RolePermissionSerializer(role, data={
                'role_name': role.role_name,
                'description': role.description,
                'permissions': role.permissions,
                'access_level': role.access_level
            }, partial=True)
            
            if serializer.is_valid():
                # Use raw SQL for updating
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE admin.roles_permission SET role_name = %s, description = %s, permissions = %s, access_level = %s WHERE role_id = %s",
                        [role.role_name, role.description, role.permissions, role.access_level, role.role_id]
                    )
                
                messages.success(request, f'Role {role.role_name} has been updated successfully.')
                return redirect('user_manage:role_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = RolePermissionForm(instance=role)
    
    return render(request, 'user_manage/role_form.html', {
        'form': form,
        'title': 'Edit Role',
        'active_tab': 'roles',
        'active_app': 'user_manage'  # Add this line
    })

@login_required
def delete_role(request, role_id):
    """View to delete a role"""
    role = get_object_or_404(RolePermission, role_id=role_id)
    
    if request.method == 'POST':
        role_name = role.role_name
        
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM admin.roles_permission WHERE role_id = %s", [role_id])
        
        messages.success(request, f'Role {role_name} has been deleted successfully.')
        return redirect('user_manage:role_list')
    
    return render(request, 'user_manage/role_confirm_delete.html', {
        'role': role,
        'active_tab': 'roles',
        'active_app': 'user_manage'  # Add this line
    })

# API Views (new)
@api_view(['GET', 'POST'])
def api_user_list(request):
    """API view to list all users or create a new one"""
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User(**serializer.validated_data)
            user.user_id = str(uuid.uuid4())
            
            # Use raw SQL for inserting
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO admin.users 
                    (employee_id, first_name, last_name, email, password, role_id, status, type, created_at, updated_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    RETURNING user_id
                    """,
                    [
                        user.employee_id, user.first_name, user.last_name, user.email, user.password,
                        user.role.role_id if hasattr(user, 'role') and user.role else None, 
                        user.status, user.type,
                        timezone.now(), timezone.now()
                    ]
                )
                # Get the generated ID
                user.user_id = cursor.fetchone()[0]
            
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def api_user_detail(request, user_id):
    """API view to retrieve, update or delete a user"""
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()  # This calls update() but doesn't persist to DB
            
            # Use raw SQL for updating
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE admin.users SET 
                    employee_id = %s, first_name = %s, last_name = %s, email = %s, 
                    password = %s, role_id = %s, status = %s, type = %s, updated_at = %s
                    WHERE user_id = %s
                    """,
                    [
                        user.employee_id, user.first_name, user.last_name, user.email, user.password,
                        user.role.role_id if hasattr(user, 'role') and user.role else None, 
                        user.status, user.type, timezone.now(),
                        user.user_id
                    ]
                )
            
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # We're not implementing DELETE for users as mentioned in your requirements

@api_view(['GET', 'POST'])
def api_role_list(request):
    """API view to list all roles or create a new one"""
    if request.method == 'GET':
        roles = RolePermission.objects.all()
        serializer = RolePermissionSerializer(roles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RolePermissionSerializer(data=request.data)
        if serializer.is_valid():
            role = RolePermission(**serializer.validated_data)
            role.role_id = str(uuid.uuid4())
            
            # Use raw SQL for inserting
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO admin.roles_permission (role_name, description, permissions, access_level) VALUES (%s, %s, %s, %s) RETURNING role_id",
                    [role.role_name, role.description, role.permissions, role.access_level]
                )
                # Get the generated ID
                role.role_id = cursor.fetchone()[0]
            
            return Response(RolePermissionSerializer(role).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def api_role_detail(request, role_id):
    """API view to retrieve, update or delete a role"""
    try:
        role = RolePermission.objects.get(role_id=role_id)
    except RolePermission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RolePermissionSerializer(role)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RolePermissionSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            role = serializer.save()  # This calls update() but doesn't persist to DB
            
            # Use raw SQL for updating
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE admin.roles_permission SET role_name = %s, description = %s, permissions = %s, access_level = %s WHERE role_id = %s",
                    [role.role_name, role.description, role.permissions, role.access_level, role.role_id]
                )
            
            return Response(RolePermissionSerializer(role).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM admin.roles_permission WHERE role_id = %s", [role_id])
        
        return Response(status=status.HTTP_204_NO_CONTENT)