from django.db import models

# Create your models here.
class Currency(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    SUSPENDED = 'Suspended'
    
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    currency_id = models.CharField(primary_key=True, max_length=255)
    currency_name = models.CharField(max_length=255)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6)
    is_active = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.currency_name
    
    class Meta:
        db_table = '"admin"."currency"'
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'