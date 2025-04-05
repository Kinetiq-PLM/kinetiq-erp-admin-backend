from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.

class RolePermission(models.Model):
    FULL_ACCESS = 'Full Access'
    VIEW_ONLY = 'Read-Only'
    
    ACCESS_LEVEL_CHOICES = [
        (FULL_ACCESS, 'Full Access'),
        (VIEW_ONLY, 'Read-Only'),
    ]
    
    role_id = models.CharField(primary_key=True, max_length=255)    
    role_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    permissions = models.TextField(null=True, blank=True)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, default=VIEW_ONLY)
    
    def __str__(self):
        return self.role_name
    
    class Meta:
        db_table = 'roles_permission'
        verbose_name = 'Role & Permission'
        verbose_name_plural = 'Roles & Permissions'
        managed = False

class User(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    SUSPENDED = 'Suspended'
    
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    
    EMPLOYEE = 'Employee'
    CUSTOMER = 'Customer'
    
    TYPE_CHOICES = [
        (EMPLOYEE, 'Employee'),
        (CUSTOMER, 'Customer'),
    ]
    
    user_id = models.CharField(primary_key=True, max_length=255)
    employee_id = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(RolePermission, on_delete=models.SET_NULL, null=True, blank=True, to_field='role_id', db_column='role_id')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=EMPLOYEE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        managed = False

class RolePermissionForm(forms.ModelForm):
    class Meta:
        model = RolePermission
        exclude = ['role_id']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['user_id', 'created_at', 'updated_at']