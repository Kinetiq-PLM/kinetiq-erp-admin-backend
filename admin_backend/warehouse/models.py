from django.db import models

# Create your models here.
class Warehouse(models.Model):
    warehouse_id = models.CharField(primary_key=True, max_length=255)
    warehouse_location = models.CharField(max_length=255)
    stored_materials = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.warehouse_location
    
    class Meta:
        db_table = '"admin"."warehouse"'
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        managed = False
