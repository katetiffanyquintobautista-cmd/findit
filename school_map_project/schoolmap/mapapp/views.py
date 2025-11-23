from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import models
from .models import BuildingInfo, UserPreferences, FindUsPoster, HomePageContent
from .forms import FindUsPosterForm, UserPreferencesForm
from django.http import JsonResponse
from .utils import log_activity

@login_required
def home(request):
    # Get user preferences
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    
    # Get active home page content
    home_content = HomePageContent.objects.filter(is_active=True).first()
    
    # Create default content if none exists
    if not home_content:
        home_content = HomePageContent.objects.create(
            site_title="FINDIT - School Map",
            welcome_title="School Campus Map",
            welcome_subtitle="Welcome back, {username}!",
            welcome_description="Navigate your campus with ease - Find buildings, rooms, and more. Use the interactive map to explore facilities and get directions.",
            is_active=True
        )
    
    # Process welcome subtitle to replace {username} placeholder
    welcome_subtitle = home_content.welcome_subtitle
    if '{username}' in welcome_subtitle:
        username = request.user.get_full_name() or request.user.username
        welcome_subtitle = welcome_subtitle.replace('{username}', username)
    
    context = {
        'home_content': home_content,
        'welcome_subtitle': welcome_subtitle,
        'user_preferences': preferences,
        'current_theme': preferences.theme,
        'current_accent': preferences.accent_color,
        'current_font_size': preferences.font_size,
    }
    return render(request, 'home.html', context)

def building_info(request):
    building_name = request.GET.get('name')
    if not building_name:
        return render(request, 'building_info.html', {'error': 'Building not specified'})
    
    building = get_object_or_404(BuildingInfo, name=building_name)
    return render(request, 'building_info.html', {'building': building})

@login_required
def profile(request):
    user = request.user
    preferences, created = UserPreferences.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Handle AJAX profile picture upload
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if 'profile_picture' in request.FILES:
                preferences.profile_picture = request.FILES['profile_picture']
                preferences.save()
                return JsonResponse({'success': True, 'message': 'Profile picture updated successfully!'})
            else:
                return JsonResponse({'success': False, 'error': 'No file provided'})
        
        # Handle regular form submission
        if 'profile_picture' in request.FILES:
            preferences.profile_picture = request.FILES['profile_picture']
            preferences.save()
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'user': user,
        'preferences': preferences,
    }
    return render(request, 'profile.html', context)

@login_required
def schedule(request):
    return render(request, 'schedule.html')

@login_required
def settings(request):
    user = request.user
    preferences, created = UserPreferences.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Settings saved successfully!',
                    'theme': preferences.theme,
                    'accent_color': preferences.accent_color,
                    'font_size': preferences.font_size
                })
            
            messages.success(request, 'Settings saved successfully!')
            return redirect('settings')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': form.errors
                })
    else:
        form = UserPreferencesForm(instance=preferences)
    
    context = {
        'form': form,
        'preferences': preferences,
        'current_theme': preferences.theme,
        'current_accent': preferences.accent_color,
        'current_font_size': preferences.font_size,
        'font_sizes': UserPreferences.FONT_SIZE_CHOICES,
    }
    return render(request, 'settings.html', context)

@login_required
def help_support(request):
    return render(request, 'help_support.html')

def about(request):
    # Get the active poster, or the most recent one with content
    active_poster = FindUsPoster.objects.filter(is_active=True).first()
    
    # If no active poster, get the most recent one with either image or video
    if not active_poster:
        active_poster = FindUsPoster.objects.filter(
            models.Q(poster_image__isnull=False) | 
            models.Q(video_file__isnull=False) | 
            models.Q(youtube_url__isnull=False)
        ).exclude(
            models.Q(poster_image='') & 
            models.Q(video_file='') & 
            models.Q(youtube_url='')
        ).order_by('-created_at').first()
        
        # Make it active if found
        if active_poster:
            FindUsPoster.objects.filter(is_active=True).update(is_active=False)
            active_poster.is_active = True
            active_poster.save()
    
    # Handle poster upload (only for staff/admin)
    poster_form = None
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            poster_form = FindUsPosterForm(request.POST, request.FILES)
            if poster_form.is_valid():
                # Deactivate previous posters
                FindUsPoster.objects.filter(is_active=True).update(is_active=False)
                # Save new poster
                new_poster = poster_form.save()
                messages.success(request, 'Content updated successfully!')
                return redirect('about')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            poster_form = FindUsPosterForm()
    
    context = {
        'active_poster': active_poster,
        'poster_form': poster_form,
        'can_upload': request.user.is_authenticated and request.user.is_staff
    }
    return render(request, 'about.html', context)

def landing(request):
    return render(request, 'landing.html')

def register(request):
    from django.contrib.auth.models import User
    from .forms import StudentRegistrationForm, TeacherRegistrationForm
    from django.contrib.auth import login
    from .utils import log_activity
    
    if request.method == 'POST':
        if 'student_submit' in request.POST:
            form = StudentRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Create user preferences
                UserPreferences.objects.get_or_create(user=user)
                # Log activity
                log_activity(user, 'user_registered', f'New student {user.username} registered', request)
                # Login user automatically
                login(request, user)
                # Return JSON response for AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Registration successful! Welcome to FINDIT.',
                        'redirect_url': '/'
                    })
                messages.success(request, 'Registration successful! Welcome to FINDIT.')
                return redirect('home')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': form.errors
                    })
        elif 'teacher_submit' in request.POST:
            form = TeacherRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Create user preferences
                UserPreferences.objects.get_or_create(user=user)
                # Log activity
                log_activity(user, 'user_registered', f'New teacher {user.username} registered', request)
                # Login user automatically
                login(request, user)
                # Return JSON response for AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Registration successful! Welcome to FINDIT.',
                        'redirect_url': '/'
                    })
                messages.success(request, 'Registration successful! Welcome to FINDIT.')
                return redirect('home')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': form.errors
                    })
    
    student_form = StudentRegistrationForm()
    teacher_form = TeacherRegistrationForm()
    
    context = {
        'student_form': student_form,
        'teacher_form': teacher_form,
        'active_tab': 'student'
    }
    return render(request, 'register.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            log_activity(user, 'user_login', f'User {user.username} logged in', request)
            if user.is_superuser:
                return redirect('admin_dashboard:dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    if request.user.is_authenticated:
        log_activity(request.user, 'user_logout', f'User {request.user.username} logged out', request)
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')