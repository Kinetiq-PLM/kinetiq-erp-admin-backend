from django.contrib import admin
from .models import User, RolePermission



# Register models with the admin site
@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'role', 'status')
