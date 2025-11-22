from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_management, name='user_management'),
    path('users/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('buildings/', views.building_management, name='building_management'),
    path('buildings/add/', views.add_building, name='add_building'),
    path('buildings/edit/<int:building_id>/', views.edit_building, name='edit_building'),
    path('buildings/delete/<int:building_id>/', views.delete_building, name='delete_building'),
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.admin_settings, name='settings'),
    path('profile/', views.admin_profile, name='profile'),
]
