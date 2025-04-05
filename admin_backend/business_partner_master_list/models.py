from django.db import models

class BusinessPartnerMaster(models.Model):
    EMPLOYEE = 'Employee'
    VENDOR = 'Vendor'
    
    CATEGORY = [
        (EMPLOYEE, 'Employee'),
        (VENDOR, 'Vendor')
    ]


    partner_id = models.CharField(primary_key=True, max_length=255)
    employee_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    vendor_code = models.OneToOneField('Vendor', models.DO_NOTHING, db_column='vendor_code', blank=True, null=True)
    customer_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    partner_name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.partner_name
    
    class Meta:
        db_table = 'business_partner_master'
        verbose_name = 'Business Partner'
        verbose_name_plural = 'Business Partners'
        managed = False

class Vendor(models.Model):

    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    BLOCKED = 'Blocked'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (BLOCKED, 'Blocked')
    ]
    vendor_code = models.CharField(primary_key=True, max_length=255)
    application_reference = models.CharField(max_length=255, blank=True, null=True)
    vendor_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.vendor_name
    
    class Meta:
        db_table = 'vendor'
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        managed = False