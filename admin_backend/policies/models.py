from django.db import models

# Create your models here.
class Policies(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    SUSPENDED = 'Suspended'
    
    STATUS = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    policy_id = models.CharField(primary_key=True, max_length=255)
    policy_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)

    def __str__(self):
        return self.policy_name
    
    class Meta:
        db_table = 'policies'
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'
        managed = False
