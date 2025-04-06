from django.urls import path
from . import views

app_name = 'item_master_list'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('items/', views.item_list, name='item_list'),
    path('items/edit/<str:item_id>/', views.edit_item, name='edit_item'),
    path('items/delete/<str:item_id>/', views.delete_item, name='delete_item'),
    path('products/', views.product_list, name='product_list'),
    path('products/edit/<str:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<str:product_id>/', views.delete_product, name='delete_product'),
    path('raw-materials/', views.raw_material_list, name='raw_material_list'),
    path('raw-materials/edit/<str:material_id>/', views.edit_material, name='edit_raw_material'),
    path('raw-materials/delete/<str:material_id>/', views.delete_material, name='delete_raw_material'),
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/edit/<str:asset_id>/', views.edit_asset, name='edit_asset'),
    path('assets/delete/<str:asset_id>/', views.delete_asset, name='delete_asset'),

    #API endpoints
    path('api/items/', views.api_item_list, name='api_item_list'),
    path('api/items/<str:item_id>/', views.api_item_detail, name='api_item_detail'),
    path('api/products/', views.api_product_list, name='api_product_list'),
    path('api/products/<str:product_id>/', views.api_product_detail, name='api_product_detail'),
    path('api/raw-materials/', views.api_raw_material_list, name='api_raw_material_list'),
    path('api/raw-materials/<str:material_id>/', views.api_raw_material_detail, name='api_raw_material_detail'),
    path('api/assets/', views.api_asset_list, name='api_asset_list'),
    path('api/assets/<str:asset_id>/', views.api_asset_detail, name='api_asset_detail'),
]