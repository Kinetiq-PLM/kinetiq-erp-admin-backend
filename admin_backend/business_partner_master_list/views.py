from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BusinessPartnerMaster, Vendor, BusinessPartnerMasterForm, VendorForm
from .serializers import BusinessPartnerMasterSerializer, VendorSerializer
from django.db import connection
from django.utils import timezone
import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

# Web views (unchanged)
@login_required
def dashboard(request):
    """Main dashboard view that displays users by default"""
    return redirect('business_partner_master_list:business_partner_list')

@login_required
def business_partner_list(request):
    """View to display the list of business partners"""
    search_query = request.GET.get('search', '')
    sort_field = request.GET.get('sort', 'name')
    sort_direction = request.GET.get('direction', 'asc')

    partners = BusinessPartnerMaster.objects.all()

    if search_query:
        partners = partners.filter(
            Q(partner_id__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(vendor_code__vendor_name__icontains=search_query) |
            Q(customer_id__icontains=search_query) |
            Q(partner_name__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(contact_info__icontains=search_query)
        )

    order_by = sort_field 
    if sort_direction == 'desc':
        order_by = '-' + sort_field

    if sort_field == 'category':
        order_by = 'partner_name' if sort_direction == 'asc' else '-partner_name'

    partners = partners.order_by(order_by)

    return render(request, 'business_partner_master_list/business_partner_list.html', {
        'partners': partners,
        'active_tab': 'business_partner',
        'active_app': 'business_partner_master_list',
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_direction': sort_direction,
    })

@login_required
def vendor_list(request):
    """View to display the list of vendors"""
    search_query = request.GET.get('search', '')
    sort_field = request.GET.get('sort', 'vendor_name')
    sort_direction = request.GET.get('direction', 'asc')

    vendors = Vendor.objects.all()

    if search_query:
        vendors = vendors.filter(
            Q(vendor_code__icontains=search_query) |
            Q(application_reference__icontains=search_query) |
            Q(vendor_name__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    order_by = sort_field 
    if sort_direction == 'desc':
        order_by = '-' + sort_field

    if sort_field == 'status':
        order_by = 'vendor_name' if sort_direction == 'asc' else '-vendor_name'

    vendors = vendors.order_by(order_by)

    return render(request, 'business_partner_master_list/vendor_list.html', {
        'vendors': vendors,
        'active_tab': 'vendors',
        'active_app': 'business_partner_master_list',
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_direction': sort_direction,
    })

@login_required
def edit_business_partner(request, partner_id):
    """View to edit a new business partner"""
    business_partner = get_object_or_404(BusinessPartnerMaster, partner_id=partner_id)

    if request.method == 'POST':
        form = BusinessPartnerMasterForm(request.POST, instance=business_partner)
        if form.is_valid():
            business_partner = form.save(commit=False)

            serializer = BusinessPartnerMasterSerializer(data={
                'employee_id': business_partner.employee_id,
                'vendor_code': business_partner.vendor_code,
                'customer_id': business_partner.customer_id,
                'partner_name': business_partner.partner_name,
                'category': business_partner.category,
                'contact_info': business_partner.contact_info,
            }, partial=True)
            
            if serializer.is_valid():
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE business_partner_master SET
                        partner_name = %s, category = %s, contact_info = %s
                        WHERE partner_id = %s
                        """,
                        [
                            business_partner.partner_name,
                            business_partner.category,
                            business_partner.contact_info,
                            business_partner.partner_id
                        ]
                    )

                messages.success(request, f'Business partner {business_partner.partner_name} has been updated successfully.')
                return redirect('business_partner_master_list:business_partner_list')
            else:
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = BusinessPartnerMasterForm(instance=business_partner)
    
    return render(request, 'business_partner_master_list/edit_business_partner.html', {
        'form': form,
        'title': 'Edit business_partner',
        'active_tab': 'business_partner',
        'active_app': 'business_partner_master_list',
    })

@login_required
def delete_business_partner(request, partner_id):
    """View to delete a business partner"""
    business_partner = get_object_or_404(BusinessPartnerMaster, partner_id=partner_id)

    if request.method == 'POST':
        business_partner = business_partner.partner_name
        
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM business_partner_master
                WHERE partner_id = %s
                """,
                [partner_id]
            )
        messages.success(request, f'Business partner {business_partner.partner_name} has been deleted successfully.')
        return redirect('business_partner_master_list:business_partner_list')

    return render(request, 'business_partner_master_list/delete_business_partner.html', {
        'business_partner': business_partner,
        'active_tab': 'business_partner',
        'active_app': 'business_partner_master_list',
    })


