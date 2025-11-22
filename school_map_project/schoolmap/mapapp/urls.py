from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('building-info/', views.building_info, name='building_info'),
    path('profile/', views.profile, name='profile'),
    path('schedule/', views.schedule, name='schedule'),
    path('settings/', views.settings, name='settings'),
    path('help-support/', views.help_support, name='help_support'),
    path('about/', views.about, name='about'),
    path('landing/', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]