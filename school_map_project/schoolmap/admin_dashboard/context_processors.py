from mapapp.models import UserPreferences

def user_preferences(request):
    """Add user preferences to template context"""
    if request.user.is_authenticated:
        preferences, created = UserPreferences.objects.get_or_create(user=request.user)
        return {'user_preferences': preferences}
    return {}