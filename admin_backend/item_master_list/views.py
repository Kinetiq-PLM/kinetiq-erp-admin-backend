from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ItemMasterData, Products, RawMaterials, Assets, ItemMasterDataForm, ProductsForm, RawMaterialsForm, AssetsForm
from .serializers import ItemMasterDataSerializer, ProductsSerializer, RawMaterialsSerializer, AssetsSerializer
from django.db import connection
from django.utils import timezone
import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

# Web views for Item Master List
@login_required
def dashboard(request):
    """Main dashboard view that displays item master list by default"""
    return redirect('item_master_list:item_list')

@login_required
def item_list(request):
    """View to display all items in a table format"""
    search_query = request.GET.get('search', '')

    sort_field = request.GET.get('sort', 'item_name')
    sort_direction = request.GET.get('direction', 'asc')

    items = ItemMasterData.objects.all()

    if search_query:
        items = items.filter(
            Q(item_id__icontains=search_query) |
            Q(asset_id__icontains=search_query) |
            Q(product_id__icontains=search_query) |
            Q(material_id__icontains=search_query) |
            Q(item_name__icontains=search_query) |
            Q(item_type__icontains=search_query) |
            Q(unit_of_measure__icontains=search_query) |
            Q(item_status__icontains=search_query) |
            Q(manage_item_by__icontains=search_query) |
            Q(preferred_vendor__vendor_code__icontains=search_query) |
            Q(purchasing_uom__icontains=search_query) |
            Q(items_per_purchase_unit__icontains=search_query) |
            Q(purchase_quantity_per_package__icontains=search_query) |
            Q(sales_uom__icontains=search_query) |
            Q(items_per_sale_unit__icontains=search_query) |
            Q(sales_quantity_per_package__icontains=search_query)
        )
    
    order_by = sort_field
    if sort_direction == 'desc':
        order_by = '-' + sort_field

    order_by = []
    if sort_field in ['item_status', 'item_type', 'unit_of_measure', 'manage_item_by', 'purchasing_uom', 'sales_uom', 'items_per_purchase_unit', 'items_per_sale_unit', 'purchase_quantity_per_package', 'sales_quantity_per_package']:
        if sort_direction == 'asc':
            order_by = [sort_field, 'item_name']
        else:
            order_by = ['-' + sort_field, 'item_name']

    items = items.order_by(*order_by) if isinstance(order_by, list) else items.order_by(order_by)
    

    return render(request, 'item_master_list/item_list.html', {
        'items': items,
        'active_tab': 'items',
        'active_app': 'item_master_list',
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_direction': sort_direction
    })

@login_required
def product_list(request):
    """View to display all products in a table format"""
    search_query = request.GET.get('search', '')

    sort_field = request.GET.get('sort', 'item_name')
    sort_direction = request.GET.get('direction', 'asc')

    products = Products.objects.all()

    if search_query:
        products = products.filter(
            Q(product_id__icontains=search_query) |
            Q(product_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(unit_of_measure__icontains=search_query) |
            Q(item_status__icontains=search_query) |
            Q(warranty_period__icontains=search_query) |
            Q(policy__policy_name__icontains=search_query)
        )

    order_by = sort_field
    if sort_direction == 'desc':
        order_by = '-' + sort_field

    if sort_field in ['item_status', 'unit_of_measure']:
        if sort_direction == 'asc':
            order_by = [sort_field, 'product_name']
        else:
            order_by = ['-' + sort_field, 'product_name']
    
    products = products.order_by(*order_by) if isinstance(order_by, list) else products.order_by(order_by)

    return render(request, 'item_master_list/product_list.html', {
        'products': products,
        'active_tab': 'products',
        'active_app': 'item_master_list',
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_direction': sort_direction
    })

@login_required
def raw_material_list(request):
    """View to display all raw materials in a table format"""
    search_query = request.GET.get('search', '')

    sort_field = request.GET.get('sort', 'item_name')
    sort_direction = request.GET.get('direction', 'asc')

    materials = RawMaterials.objects.all()

    if search_query:
        materials = materials.filter(
            Q(material_id__icontains=search_query) |
            Q(material_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(unit_of_measure__icontains=search_query) |
            Q(cost_per_unit__icontains=search_query) |
            Q(vendor_code__vendor_code__icontains=search_query)
        )

    order_by = sort_field
    if sort_direction == 'desc':
        order_by = '-' + sort_field

    if sort_field == 'unit_of_measure':
        if sort_direction == 'asc':
            order_by = [sort_field, 'material_name']
        else:
            order_by = ['-' + sort_field, 'material_name']

    materials = materials.order_by(*order_by) if isinstance(order_by, list) else materials.order_by(order_by)

    return render(request, 'item_master_list/raw_material_list.html', {
        'materials': materials,
        'active_tab': 'raw_materials',
        'active_app': 'item_master_list',
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_direction': sort_direction
    })

@login_required
def asset_list(request):
    """View to display all assets in a table format"""
    search_query = request.GET.get('search', '')
    sort_field = request.GET.get('sort', 'asset_name')
    sort_direction = request.GET.get('direction', 'asc')

    assets = Assets.objects.all()
    
    if search_query:
        assets = assets.filter(
            Q(asset_id__icontains=search_query) |
            Q(asset_name__icontains=search_query) |
            Q(purchase_date__icontains=search_query) |
            Q(purchase_price__icontains=search_query) |
            Q(serial_no__icontains=search_query)
        )
    
    order_by = sort_field
    if sort_direction == 'desc':
        order_by = '-' + sort_field
    
    if sort_field == 'purchase_date':
        if sort_direction == 'asc':
            order_by = [sort_field, 'asset_name']
        else:
            order_by = ['-' + sort_field, 'asset_name']
    
    assets = assets.order_by(*order_by) if isinstance(order_by, list) else assets.order_by(order_by)

    return render(request, 'item_master_list/asset_list.html', {
        'assets': assets,
        'active_tab': 'assets',
        'active_app': 'item_master_list',
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_direction': sort_direction
    })

# Item Master Data CRUD operations
@login_required
def edit_item(request, item_id):
    """View to edit an existing item"""
    item = get_object_or_404(ItemMasterData, item_id=item_id)
    
    if request.method == 'POST':
        form = ItemMasterDataForm(request.POST, instance=item)
        if form.is_valid():
            # Update item fields but don't save to DB yet
            item = form.save(commit=False)
            
            # Validate with serializer
            serializer = ItemMasterDataSerializer(item, data={
                'preferred_vendor': item.preferred_vendor,
                'purchasing_uom': item.purchasing_uom,
                'items_per_purchase_unit': item.items_per_purchase_unit,
                'purchase_quantity_per_package': item.purchase_quantity_per_package,
                'sales_uom': item.sales_uom,
                'items_per_sale_unit': item.items_per_sale_unit,
                'sales_quantity_per_package': item.sales_quantity_per_package
            }, partial=True)
            
            if serializer.is_valid():
                # Use raw SQL for updating
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE item_master_data SET 
                        preferred_vendor = %s, purchasing_uom = %s, items_per_purchase_unit = %s, 
                        purchase_quantity_per_package = %s, sales_uom = %s, items_per_sale_unit = %s, 
                        sales_quantity_per_package = %s
                        WHERE item_id = %s
                        """,
                        [
                            item.preferred_vendor, item.purchasing_uom, item.items_per_purchase_unit,
                            item.purchase_quantity_per_package, item.sales_uom, item.items_per_sale_unit,
                            item.sales_quantity_per_package,
                            item.item_id
                        ]
                    )
                
                messages.success(request, f'Item {item.item_name} has been updated successfully.')
                return redirect('item_master_list:item_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = ItemMasterDataForm(instance=item)
    
    return render(request, 'item_master_list/item_form.html', {
        'form': form,
        'title': 'Edit Item',
        'active_tab': 'items',
        'active_app': 'item_master_list'
    })

@login_required
def delete_item(request, item_id):
    """View to delete an item"""
    item = get_object_or_404(ItemMasterData, item_id=item_id)
    
    if request.method == 'POST':
        item_name = item.item_name
        
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM item_master_data WHERE item_id = %s", [item_id])
        
        messages.success(request, f'Item {item_name} has been deleted successfully.')
        return redirect('item_master_list:item_list')
    
    return render(request, 'item_master_list/item_confirm_delete.html', {
        'item': item,
        'active_tab': 'items',
        'active_app': 'item_master_list'
    })

# Products CRUD operations
@login_required
def add_product(request):
    """View to add a new product"""
    if request.method == 'POST':
        form = ProductsForm(request.POST)
        if form.is_valid():
            # Create a product instance but don't save to DB yet
            product = form.save(commit=False)
            
            # Create serializer to validate the data
            serializer = ProductsSerializer(data={
                'product_name': product.product_name,
                'description': product.description,
                'selling_price': str(product.selling_price),
                'stock_level': product.stock_level,
                'unit_of_measure': product.unit_of_measure,
                'batch_no': product.batch_no,
                'item_status': product.item_status,
                'warranty_period': product.warranty_period,
                'policy': product.policy.policy_id if product.policy else None,
                'content_id': product.content_id
            })
            
            if serializer.is_valid():
                # Generate a temporary ID for the product object
                product.product_id = str(uuid.uuid4())
                
                # Use raw SQL for inserting
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO products 
                        (product_id, product_name, description, selling_price, stock_level, unit_of_measure, batch_no, 
                        item_status, warranty_period, policy_id, content_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        RETURNING product_id
                        """,
                        [
                            product.product_id, product.product_name, product.description, product.selling_price,
                            product.stock_level, product.unit_of_measure, product.batch_no, product.item_status,
                            product.warranty_period, 
                            product.policy.policy_id if product.policy else None,
                            product.content_id
                        ]
                    )
                    # Get the generated ID
                    product.product_id = cursor.fetchone()[0]
                
                messages.success(request, f'Product {product.product_name} has been added successfully.')
                return redirect('item_master_list:product_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = ProductsForm()
    
    return render(request, 'item_master_list/product_form.html', {
        'form': form,
        'title': 'Add New Product',
        'active_tab': 'products',
        'active_app': 'item_master_list'
    })

@login_required
def edit_product(request, product_id):
    """View to edit an existing product"""
    product = get_object_or_404(Products, product_id=product_id)
    
    if request.method == 'POST':
        form = ProductsForm(request.POST, instance=product)
        if form.is_valid():
            # Update product fields but don't save to DB yet
            product = form.save(commit=False)
            
            # Validate with serializer
            serializer = ProductsSerializer(product, data={
                'product_name': product.product_name,
                'description': product.description,
                'selling_price': str(product.selling_price),
                'stock_level': product.stock_level,
                'unit_of_measure': product.unit_of_measure,
                'batch_no': product.batch_no,
                'item_status': product.item_status,
                'warranty_period': product.warranty_period,
                'policy': product.policy.policy_id if product.policy else None,
                'content_id': product.content_id
            }, partial=True)
            
            if serializer.is_valid():
                # Use raw SQL for updating
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE products SET 
                        product_name = %s, description = %s, selling_price = %s, stock_level = %s,
                        unit_of_measure = %s, batch_no = %s, item_status = %s, warranty_period = %s,
                        policy_id = %s, content_id = %s
                        WHERE product_id = %s
                        """,
                        [
                            product.product_name, product.description, product.selling_price, product.stock_level,
                            product.unit_of_measure, product.batch_no, product.item_status, product.warranty_period,
                            product.policy.policy_id if product.policy else None,
                            product.content_id, product.product_id
                        ]
                    )
                
                messages.success(request, f'Product {product.product_name} has been updated successfully.')
                return redirect('item_master_list:product_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = ProductsForm(instance=product)
    
    return render(request, 'item_master_list/product_form.html', {
        'form': form,
        'title': 'Edit Product',
        'active_tab': 'products',
        'active_app': 'item_master_list'
    })

@login_required
def delete_product(request, product_id):
    """View to delete a product"""
    product = get_object_or_404(Products, product_id=product_id)
    
    if request.method == 'POST':
        product_name = product.product_name
        
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE product_id = %s", [product_id])
        
        messages.success(request, f'Product {product_name} has been deleted successfully.')
        return redirect('item_master_list:product_list')
    
    return render(request, 'item_master_list/product_confirm_delete.html', {
        'product': product,
        'active_tab': 'products',
        'active_app': 'item_master_list'
    })

# Raw Materials CRUD operations
@login_required
def add_material(request):
    """View to add a new raw material"""
    if request.method == 'POST':
        form = RawMaterialsForm(request.POST)
        if form.is_valid():
            # Create a material instance but don't save to DB yet
            material = form.save(commit=False)
            
            # Create serializer to validate the data
            serializer = RawMaterialsSerializer(data={
                'material_name': material.material_name,
                'description': material.description,
                'unit_of_measure': material.unit_of_measure,
                'cost_per_unit': str(material.cost_per_unit) if material.cost_per_unit else None,
                'vendor_code': material.vendor_code.vendor_code if material.vendor_code else None
            })
            
            if serializer.is_valid():
                # Generate a UUID for the material ID
                material.material_id = str(uuid.uuid4())
                
                # Use raw SQL for inserting
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO raw_materials 
                        (material_id, material_name, description, unit_of_measure, cost_per_unit, vendor_code) 
                        VALUES (%s, %s, %s, %s, %s, %s) 
                        RETURNING material_id
                        """,
                        [
                            material.material_id, material.material_name, material.description, 
                            material.unit_of_measure, material.cost_per_unit,
                            material.vendor_code.vendor_code if material.vendor_code else None
                        ]
                    )
                    # Get the generated ID
                    material.material_id = cursor.fetchone()[0]
                
                messages.success(request, f'Raw Material {material.material_name} has been added successfully.')
                return redirect('item_master_list:raw_material_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = RawMaterialsForm()
    
    return render(request, 'item_master_list/material_form.html', {
        'form': form,
        'title': 'Add New Raw Material',
        'active_tab': 'raw_materials',
        'active_app': 'item_master_list'
    })

@login_required
def edit_material(request, material_id):
    """View to edit an existing raw material"""
    material = get_object_or_404(RawMaterials, material_id=material_id)
    
    if request.method == 'POST':
        form = RawMaterialsForm(request.POST, instance=material)
        if form.is_valid():
            # Update material fields but don't save to DB yet
            material = form.save(commit=False)
            
            # Validate with serializer
            serializer = RawMaterialsSerializer(material, data={
                'material_name': material.material_name,
                'description': material.description,
                'unit_of_measure': material.unit_of_measure,
                'cost_per_unit': str(material.cost_per_unit) if material.cost_per_unit else None,
                'vendor_code': material.vendor_code.vendor_code if material.vendor_code else None
            }, partial=True)
            
            if serializer.is_valid():
                # Use raw SQL for updating
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE raw_materials SET 
                        material_name = %s, description = %s, unit_of_measure = %s,
                        cost_per_unit = %s, vendor_code = %s
                        WHERE material_id = %s
                        """,
                        [
                            material.material_name, material.description, material.unit_of_measure,
                            material.cost_per_unit, 
                            material.vendor_code.vendor_code if material.vendor_code else None,
                            material.material_id
                        ]
                    )
                
                messages.success(request, f'Raw Material {material.material_name} has been updated successfully.')
                return redirect('item_master_list:raw_material_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = RawMaterialsForm(instance=material)
    
    return render(request, 'item_master_list/material_form.html', {
        'form': form,
        'title': 'Edit Raw Material',
        'active_tab': 'raw_materials',
        'active_app': 'item_master_list'
    })

@login_required
def delete_material(request, material_id):
    """View to delete a raw material"""
    material = get_object_or_404(RawMaterials, material_id=material_id)
    
    if request.method == 'POST':
        material_name = material.material_name
        
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM raw_materials WHERE material_id = %s", [material_id])
        
        messages.success(request, f'Raw Material {material_name} has been deleted successfully.')
        return redirect('item_master_list:raw_material_list')
    
    return render(request, 'item_master_list/material_confirm_delete.html', {
        'material': material,
        'active_tab': 'raw_materials',
        'active_app': 'item_master_list'
    })

# Assets CRUD operations
@login_required
def add_asset(request):
    """View to add a new asset"""
    if request.method == 'POST':
        form = AssetsForm(request.POST)
        if form.is_valid():
            # Create an asset instance but don't save to DB yet
            asset = form.save(commit=False)
            
            # Create serializer to validate the data
            serializer = AssetsSerializer(data={
                'asset_name': asset.asset_name,
                'purchase_date': asset.purchase_date.isoformat() if asset.purchase_date else None,
                'purchase_price': str(asset.purchase_price),
                'serial_no': asset.serial_no,
                'content_id': asset.content_id
            })
            
            if serializer.is_valid():
                # Generate a UUID for the asset ID
                asset.asset_id = str(uuid.uuid4())
                
                # Use raw SQL for inserting
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO assets 
                        (asset_id, asset_name, purchase_date, purchase_price, serial_no, content_id) 
                        VALUES (%s, %s, %s, %s, %s, %s) 
                        RETURNING asset_id
                        """,
                        [
                            asset.asset_id, asset.asset_name, asset.purchase_date, asset.purchase_price,
                            asset.serial_no, asset.content_id
                        ]
                    )
                    # Get the generated ID
                    asset.asset_id = cursor.fetchone()[0]
                
                messages.success(request, f'Asset {asset.asset_name} has been added successfully.')
                return redirect('item_master_list:asset_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = AssetsForm()
    
    return render(request, 'item_master_list/asset_form.html', {
        'form': form,
        'title': 'Add New Asset',
        'active_tab': 'assets',
        'active_app': 'item_master_list'
    })

@login_required
def edit_asset(request, asset_id):
    """View to edit an existing asset"""
    asset = get_object_or_404(Assets, asset_id=asset_id)
    
    if request.method == 'POST':
        form = AssetsForm(request.POST, instance=asset)
        if form.is_valid():
            # Update asset fields but don't save to DB yet
            asset = form.save(commit=False)
            
            # Validate with serializer
            serializer = AssetsSerializer(asset, data={
                'asset_name': asset.asset_name,
                'purchase_date': asset.purchase_date.isoformat() if asset.purchase_date else None,
                'purchase_price': str(asset.purchase_price),
                'serial_no': asset.serial_no,
                'content_id': asset.content_id
            }, partial=True)
            
            if serializer.is_valid():
                # Use raw SQL for updating
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE assets SET 
                        asset_name = %s, purchase_date = %s, purchase_price = %s, 
                        serial_no = %s, content_id = %s
                        WHERE asset_id = %s
                        """,
                        [
                            asset.asset_name, asset.purchase_date, asset.purchase_price,
                            asset.serial_no, asset.content_id, asset.asset_id
                        ]
                    )
                
                messages.success(request, f'Asset {asset.asset_name} has been updated successfully.')
                return redirect('item_master_list:asset_list')
            else:
                # Add serializer errors to form errors
                for field, error_list in serializer.errors.items():
                    for error in error_list:
                        form.add_error(field, error)
    else:
        form = AssetsForm(instance=asset)
    
    return render(request, 'item_master_list/asset_form.html', {
        'form': form,
        'title': 'Edit Asset',
        'active_tab': 'assets',
        'active_app': 'item_master_list'
    })

@login_required
def delete_asset(request, asset_id):
    """View to delete an asset"""
    asset = get_object_or_404(Assets, asset_id=asset_id)
    
    if request.method == 'POST':
        asset_name = asset.asset_name
        
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM assets WHERE asset_id = %s", [asset_id])
        
        messages.success(request, f'Asset {asset_name} has been deleted successfully.')
        return redirect('item_master_list:asset_list')
    
    return render(request, 'item_master_list/asset_confirm_delete.html', {
        'asset': asset,
        'active_tab': 'assets',
        'active_app': 'item_master_list'
    })

# Similar CRUD operations for RawMaterials, Assets, Policies, and Vendor
# would follow the same pattern as above

# API Views
@api_view(['GET'])
def api_item_list(request):
    """API view to list all items"""
    if request.method == 'GET':
        items = ItemMasterData.objects.all()
        serializer = ItemMasterDataSerializer(items, many=True)
        return Response(serializer.data)
    

@api_view(['GET', 'PUT', 'DELETE'])
def api_item_detail(request, item_id):
    """API view to retrieve, update or delete an item"""
    try:
        item = ItemMasterData.objects.get(item_id=item_id)
    except ItemMasterData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ItemMasterDataSerializer(item)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ItemMasterDataSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            item = serializer.save()  # This calls update() but doesn't persist to DB
            
            # Use raw SQL for updating
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE item_master_data SET 
                    preferred_vendor = %s, purchasing_uom = %s, items_per_purchase_unit = %s, 
                    purchase_quantity_per_package = %s, sales_uom = %s, items_per_sale_unit = %s, 
                    sales_quantity_per_package = %s
                    WHERE item_id = %s
                    """,
                    [
                        item.preferred_vendor, item.purchasing_uom, item.items_per_purchase_unit,
                        item.purchase_quantity_per_package, item.sales_uom, item.items_per_sale_unit,
                        item.sales_quantity_per_package,
                        item.item_id
                    ]
                )
            
            return Response(ItemMasterDataSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM item_master_data WHERE item_id = %s", [item_id])
        
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def api_product_list(request):
    """API view to list all products or create a new one"""
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            product = Products(**serializer.validated_data)
            product.product_id = str(uuid.uuid4())
            
            # Use raw SQL for inserting
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO products 
                    (product_id, product_name, description, selling_price, stock_level, unit_of_measure, batch_no, 
                    item_status, warranty_period, policy_id, content_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    RETURNING product_id
                    """,
                    [
                        product.product_id, product.product_name, product.description, product.selling_price,
                        product.stock_level, product.unit_of_measure, product.batch_no, product.item_status,
                        product.warranty_period, 
                        product.policy.policy_id if hasattr(product, 'policy') and product.policy else None,
                        product.content_id
                    ]
                )
                # Get the generated ID
                product.product_id = cursor.fetchone()[0]
            
            return Response(ProductsSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def api_product_detail(request, product_id):
    """API view to retrieve, update or delete a product"""
    try:
        product = Products.objects.get(product_id=product_id)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductsSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()  # This calls update() but doesn't persist to DB
            
            # Use raw SQL for updating
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE products SET 
                    product_name = %s, description = %s, selling_price = %s, stock_level = %s,
                    unit_of_measure = %s, batch_no = %s, item_status = %s, warranty_period = %s,
                    policy_id = %s, content_id = %s
                    WHERE product_id = %s
                    """,
                    [
                        product.product_name, product.description, product.selling_price, product.stock_level,
                        product.unit_of_measure, product.batch_no, product.item_status, product.warranty_period,
                        product.policy.policy_id if hasattr(product, 'policy') and product.policy else None,
                        product.content_id, product.product_id
                    ]
                )
            
            return Response(ProductsSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE product_id = %s", [product_id])
        
        return Response(status=status.HTTP_204_NO_CONTENT)

# Similar API view functions for RawMaterials, Assets, Policies
@api_view(['GET', 'POST'])
def api_raw_material_list(request):
    """API view to list all raw materials or create a new one"""
    if request.method == 'GET':
        materials = RawMaterials.objects.all()
        serializer = RawMaterialsSerializer(materials, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RawMaterialsSerializer(data=request.data)
        if serializer.is_valid():
            material = RawMaterials(**serializer.validated_data)
            material.material_id = str(uuid.uuid4())
            
            # Use raw SQL for inserting
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO raw_materials 
                    (material_id, material_name, description, unit_of_measure, cost_per_unit, vendor_code) 
                    VALUES (%s, %s, %s, %s, %s, %s) 
                    RETURNING material_id
                    """,
                    [
                        material.material_id, material.material_name, material.description,
                        material.unit_of_measure, material.cost_per_unit,
                        material.vendor_code.vendor_code if hasattr(material, 'vendor_code') and material.vendor_code else None
                    ]
                )
                # Get the generated ID
                material.material_id = cursor.fetchone()[0]
            
            return Response(RawMaterialsSerializer(material).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def api_raw_material_detail(request, material_id):
    """API view to retrieve, update or delete a raw material"""
    try:
        material = RawMaterials.objects.get(material_id=material_id)
    except RawMaterials.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RawMaterialsSerializer(material)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RawMaterialsSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            material = serializer.save()  # This calls update() but doesn't persist to DB

            # Use raw SQL for updating
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE raw_materials SET 
                    material_name = %s, description = %s, unit_of_measure = %s,
                    cost_per_unit = %s, vendor_code = %s
                    WHERE material_id = %s
                    """,
                    [
                        material.material_name, material.description, material.unit_of_measure,
                        material.cost_per_unit,
                        material.vendor_code.vendor_code if hasattr(material, 'vendor_code') and material.vendor_code else None,
                        material.material_id
                    ]
                )
            
            return Response(RawMaterialsSerializer(material).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM raw_materials WHERE material_id = %s", [material_id])
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def api_asset_list(request):
    """API view to list all assets or create a new one"""
    if request.method == 'GET':
        assets = Assets.objects.all()
        serializer = AssetsSerializer(assets, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AssetsSerializer(data=request.data)
        if serializer.is_valid():
            asset = Assets(**serializer.validated_data)
            asset.asset_id = str(uuid.uuid4())
            
            # Use raw SQL for inserting
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO assets 
                    (asset_id, asset_name, purchase_date, purchase_price, serial_no, content_id) 
                    VALUES (%s, %s, %s, %s, %s, %s) 
                    RETURNING asset_id
                    """,
                    [
                        asset.asset_id, asset.asset_name, asset.purchase_date.isoformat() if asset.purchase_date else None,
                        asset.purchase_price, asset.serial_no, asset.content_id
                    ]
                )
                # Get the generated ID
                asset.asset_id = cursor.fetchone()[0]
            
            return Response(AssetsSerializer(asset).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def api_asset_detail(request, asset_id):
    """API view to retrieve, update or delete an asset"""
    try:
        asset = Assets.objects.get(asset_id=asset_id)
    except Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AssetsSerializer(asset)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AssetsSerializer(asset, data=request.data, partial=True)
        if serializer.is_valid():
            asset = serializer.save()

            # Use raw SQL for updating
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE assets SET 
                    asset_name = %s, purchase_date = %s, purchase_price = %s, 
                    serial_no = %s, content_id = %s
                    WHERE asset_id = %s
                    """,
                    [
                        asset.asset_name, asset.purchase_date.isoformat() if asset.purchase_date else None,
                        asset.purchase_price, asset.serial_no, asset.content_id, asset.asset_id
                    ]
                )

            return Response(AssetsSerializer(asset).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Use raw SQL for deleting
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM assets WHERE asset_id = %s", [asset_id])
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    