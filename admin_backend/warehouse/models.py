from django.db import models

# Create your models here.
class WarehouseManagers(models.Model):
    user_id = models.CharField(primary_key=True, max_length=255)
    employee_id = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = '"admin"."users"'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        managed = False

class Warehouse(models.Model):
    warehouse_id = models.CharField(primary_key=True, max_length=255)
    warehouse_location = models.CharField(max_length=255)
    warehouse_name = models.CharField(max_length=255)
    warehouse_manager = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=50)

    def __str__(self):
        return self.warehouse_name
    
    class Meta:
        db_table = '"admin"."warehouse"'
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        managed = False