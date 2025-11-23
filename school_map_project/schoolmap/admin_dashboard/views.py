from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.models import User
from mapapp.models import BuildingInfo, UserPreferences, ActivityLog  # Import models from mapapp
from mapapp.utils import log_activity
from django.views.decorators.http import require_http_methods
import json

# Custom decorator to check if user is admin
def admin_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/login/'
    )
    return actual_decorator(view_func)

from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='home')
def dashboard(request):
    # Get recent user activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_activities = ActivityLog.objects.select_related('user').order_by('-timestamp')[:10]
    
    # Get building statistics
    total_buildings = BuildingInfo.objects.count()
    
    # Get user statistics
    total_users = User.objects.count()
    new_users_week = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=7)
    ).count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Get today's statistics
    today = timezone.now().date()
    users_today = User.objects.filter(date_joined__date=today).count()
    logins_today = ActivityLog.objects.filter(
        action='user_login',
        timestamp__date=today
    ).count()
    
    # Get user growth data for the last 7 days
    date_list = [today - timedelta(days=x) for x in range(6, -1, -1)]
    user_growth_data = {
        'labels': [date.strftime('%a') for date in date_list],
        'data': [
            User.objects.filter(date_joined__date=date).count() 
            for date in date_list
        ]
    }
    
    # Get login activity for the last 7 days
    login_activity_data = {
        'labels': [date.strftime('%a') for date in date_list],
        'data': [
            ActivityLog.objects.filter(
                action='user_login',
                timestamp__date=date
            ).count() for date in date_list
        ]
    }
    
    context = {
        'active_page': 'dashboard',
        'recent_users': recent_users,
        'recent_activities': recent_activities,
        'total_buildings': total_buildings,
        'total_users': total_users,
        'new_users_this_week': new_users_week,
        'active_users': active_users,
        'users_today': users_today,
        'logins_today': logins_today,
        'user_growth_data': user_growth_data,
        'login_activity_data': login_activity_data,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

@login_required
def toggle_user_status(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        action = 'user_activated' if user.is_active else 'user_deactivated'
        log_activity(request.user, action, f'Admin {request.user.username} {status} user {user.username}', request)
        messages.success(request, f"User {user.username} has been {status} successfully.")
    
    return redirect('admin_dashboard:user_management')

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        username = user.username
        user.delete()
        messages.success(request, f"User {username} has been deleted successfully.")
    
    return redirect('admin_dashboard:user_management')

@login_required
def user_management(request):
    if not request.user.is_staff:
        return redirect('home')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard/user_management.html', {
        'active_page': 'users',
        'users': users
    })

@login_required
def building_management(request):
    if not request.user.is_staff:
        return redirect('home')
    
    buildings = BuildingInfo.objects.all()
    return render(request, 'admin_dashboard/building_management.html', {
        'active_page': 'buildings',
        'buildings': buildings
    })

@login_required
@require_http_methods(["POST"])
def add_building(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        # Get data from request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description', '')
            edit_id = data.get('edit_id')
        else:
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            edit_id = request.POST.get('edit_id')
            
        if not name:
            return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
        
        if edit_id:
            # Edit existing building
            building = get_object_or_404(BuildingInfo, id=edit_id)
            
            # Check if another building with this name exists
            if BuildingInfo.objects.filter(name=name).exclude(id=edit_id).exists():
                return JsonResponse({'success': False, 'error': 'Another building with this name already exists'}, status=400)
            
            building.name = name
            building.description = description
            building.save()
        else:
            # Create new building
            if BuildingInfo.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'A building with this name already exists'}, status=400)
            
            building = BuildingInfo.objects.create(
                name=name,
                description=description
            )
            log_activity(request.user, 'building_added', f'Admin {request.user.username} added building: {name}', request)
        
        return JsonResponse({
            'success': True,
            'building': {
                'id': building.id,
                'name': building.name,
                'description': building.description or ''
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def edit_building(request, building_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        building = get_object_or_404(BuildingInfo, id=building_id)
        
        # Get data from request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description', '')
        else:
            name = request.POST.get('name')
            description = request.POST.get('description', '')
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
        
        # Check if another building with this name already exists
        if BuildingInfo.objects.filter(name=name).exclude(id=building_id).exists():
            return JsonResponse(
                {'success': False, 'error': 'Another building with this name already exists'}, 
                status=400
            )
        
        # Update the building
        building.name = name
        building.description = description
        building.save()
        
        return JsonResponse({
            'success': True,
            'building': {
                'id': building.id,
                'name': building.name,
                'description': building.description or ''
            }
        })
    except Exception as e:
        print(f"Error updating building: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def delete_building(request, building_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        building = get_object_or_404(BuildingInfo, id=building_id)
        building_name = building.name
        building.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Building {building_name} has been deleted successfully.'
        })
    except Exception as e:
        print(f"Error deleting building: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def analytics(request):
    if not request.user.is_staff:
        return redirect('home')
    
    # Calculate date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Get user registration data for the last 7 days
    date_list = [today - timedelta(days=x) for x in range(6, -1, -1)]
    user_registrations = {
        'labels': [date.strftime('%a, %b %d') for date in date_list],
        'data': [
            User.objects.filter(
                date_joined__date=date
            ).count() for date in date_list
        ]
    }
    
    # Get building statistics
    buildings = BuildingInfo.objects.all()
    building_stats = {
        'labels': [building.name for building in buildings],
        'data': [1] * len(buildings)  # Placeholder for room counts
    }
    
    # Get user statistics
    total_users = User.objects.count()
    new_users_week = User.objects.filter(
        date_joined__gte=week_ago
    ).count()
    
    active_users_today = User.objects.filter(
        last_login__date=today
    ).count()
    
    total_buildings = buildings.count()
    
    return render(request, 'admin_dashboard/analytics.html', {
        'active_page': 'analytics',
        'user_registrations': user_registrations,
        'building_stats': building_stats,
        'total_users': total_users,
        'new_users_this_week': new_users_week,
        'active_users_today': active_users_today,
        'total_buildings': total_buildings
    })

@login_required
def admin_settings(request):
    if not request.user.is_staff:
        return redirect('home')
        
    if request.method == 'POST':
        # Handle settings form submission
        messages.success(request, 'Settings updated successfully')
        return redirect('admin_settings')
    
    return render(request, 'admin_dashboard/settings.html', {
        'active_page': 'settings'
    })

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='home')
def admin_profile(request):
    user = request.user
    preferences, created = UserPreferences.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            preferences.profile_picture = request.FILES['profile_picture']
            preferences.save()
            messages.success(request, 'Profile picture uploaded successfully!')
            return redirect('admin_dashboard:profile')
        
        # Handle basic profile updates
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('admin_dashboard:profile')
    
    context = {
        'active_page': 'profile',
        'user': user,
        'preferences': preferences,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'admin_dashboard/profile.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='home')
def dashboard_api(request):
    """API endpoint for live dashboard updates"""
    today = timezone.now().date()
    
    # Get real-time statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    users_today = User.objects.filter(date_joined__date=today).count()
    logins_today = ActivityLog.objects.filter(
        action='user_login',
        timestamp__date=today
    ).count()
    
    # Get recent activities
    recent_activities = ActivityLog.objects.select_related('user').order_by('-timestamp')[:5]
    activities_data = []
    for activity in recent_activities:
        activities_data.append({
            'action': activity.get_action_display(),
            'description': activity.description,
            'timestamp': activity.timestamp.strftime('%H:%M:%S'),
            'user': activity.user.username if activity.user else 'System'
        })
    
    data = {
        'total_users': total_users,
        'active_users': active_users,
        'users_today': users_today,
        'logins_today': logins_today,
        'recent_activities': activities_data,
        'last_updated': timezone.now().strftime('%H:%M:%S')
    }
    
    return JsonResponse(data)
