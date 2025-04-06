from django.contrib import admin
from .models import User, RolePermission, RolePermissionForm, UserForm
from django.utils import timezone
from django.db import connection


# Register models with the admin site
@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    form = RolePermissionForm
    list_display = ('role_id', 'role_name', 'access_level')
    search_fields = ('role_name', 'description')
    list_filter = ('access_level',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # New record
            # Use raw SQL for inserting
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO admin.roles_permission (role_name, description, permissions, access_level) VALUES (%s, %s, %s, %s) RETURNING role_id",
                    [obj.role_name, obj.description, obj.permissions, obj.access_level]
                )
                # Get the generated ID
                obj.role_id = cursor.fetchone()[0]
        else:
            # Use raw SQL for updating
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE admin.roles_permission SET role_name = %s, description = %s, permissions = %s, access_level = %s WHERE role_id = %s",
                    [obj.role_name, obj.description, obj.permissions, obj.access_level, obj.role_id]
                )
    
    def response_add(self, request, obj, post_url_continue=None):
        # Refresh the object from database to ensure we have the generated ID
        obj.refresh_from_db()
        return super().response_add(request, obj, post_url_continue)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'role', 'status', 'type')
    search_fields = ('first_name', 'last_name', 'email', 'employee_id')
    list_filter = ('status', 'type', 'role')
    
    def save_model(self, request, obj, form, change):
        if not change:  # New record
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
                        obj.employee_id, obj.first_name, obj.last_name, obj.email, obj.password,
                        obj.role_id if obj.role else None, obj.status, obj.type,
                        timezone.now(), timezone.now()
                    ]
                )
                # Get the generated ID
                obj.user_id = cursor.fetchone()[0]
        else:
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
                        obj.employee_id, obj.first_name, obj.last_name, obj.email, obj.password,
                        obj.role_id if obj.role else None, obj.status, obj.type, timezone.now(),
                        obj.user_id
                    ]
                )
    
    def response_add(self, request, obj, post_url_continue=None):
        # Refresh the object from database to ensure we have the generated ID
        obj.refresh_from_db()
        return super().response_add(request, obj, post_url_continue)