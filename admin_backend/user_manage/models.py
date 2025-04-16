# user_manage/models.py
from django.db import models
from django.utils import timezone


# Create your models here.

class RolePermission(models.Model):  
    role_id = models.CharField(primary_key=True, max_length=255)    
    role_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    permissions = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.role_name
    
    class Meta:
        db_table = '"admin"."roles_permission"'
        verbose_name = 'Role & Permission'
        verbose_name_plural = 'Roles & Permissions'
        managed = False

class User(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    
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
        db_table = '"admin"."users"'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        managed = False
