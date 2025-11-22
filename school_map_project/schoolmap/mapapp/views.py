from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BuildingInfo, UserPreferences, FindUsPoster, HomePageContent
from .forms import FindUsPosterForm, UserPreferencesForm
from django.http import JsonResponse

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
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            preferences.profile_picture = request.FILES['profile_picture']
            preferences.save()
            messages.success(request, 'Profile picture updated successfully!')
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
    # Get the active poster
    active_poster = FindUsPoster.objects.filter(is_active=True).first()
    
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
                messages.success(request, 'Poster updated successfully!')
                return redirect('about')
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
    return render(request, 'register.html')