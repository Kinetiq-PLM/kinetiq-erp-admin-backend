from django.urls import path
from . import views

app_name = 'user_manage'

urlpatterns = [
    # Web views
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<str:user_id>/', views.edit_user, name='edit_user'),
    path('roles/', views.role_list, name='role_list'),
    path('roles/add/', views.add_role, name='add_role'),
    path('roles/edit/<str:role_id>/', views.edit_role, name='edit_role'),
    path('roles/delete/<str:role_id>/', views.delete_role, name='delete_role'),
    
    # API endpoints
    path('api/users/', views.api_user_list, name='api_user_list'),
    path('api/users/<str:user_id>/', views.api_user_detail, name='api_user_detail'),
    path('api/roles/', views.api_role_list, name='api_role_list'),
    path('api/roles/<str:role_id>/', views.api_role_detail, name='api_role_detail'),
]