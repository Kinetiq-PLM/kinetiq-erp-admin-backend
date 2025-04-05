from django.contrib import admin
from .models import BusinessPartnerMaster, Vendor

@admin.register(BusinessPartnerMaster)
class BusinessPartnerMasterAdmin(admin.ModelAdmin):
    list_display = ('partner_id', 'employee_id', 'vendor_code', 'customer_id', 'partner_name', 'category', 'contact_info')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_code', 'application_reference', 'vendor_name', 'contact_person', 'status')

# Register your models here.
