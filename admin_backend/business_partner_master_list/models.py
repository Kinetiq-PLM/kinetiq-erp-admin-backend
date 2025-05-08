from django.db import models
from django.utils import timezone
from django import forms

class Vendor(models.Model):

    vendor_code = models.CharField(primary_key=True, max_length=255)
    company_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='Approved')


    def __str__(self):
        return self.company_name

    class Meta:
        managed = False
        db_table = '"purchasing"."vendors"'

class BusinessPartnerMaster(models.Model):
    EMPLOYEE = 'Employee'
    VENDOR = 'Vendor'
    
    CATEGORY = [
        (EMPLOYEE, 'Employee'),
        (VENDOR, 'Vendor')
    ]


    partner_id = models.CharField(primary_key=True, max_length=255)
    partner_name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.partner_name
    
    class Meta:
        db_table = '"admin"."business_partner_master"'
        verbose_name = 'Business Partner'
        verbose_name_plural = 'Business Partners'
        managed = False
