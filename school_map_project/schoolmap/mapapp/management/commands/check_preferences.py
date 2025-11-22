from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mapapp.models import UserPreferences

class Command(BaseCommand):
    help = 'Check and create UserPreferences for all users'

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.all()
        
        for user in users:
            # This will create UserPreferences if it doesn't exist
            preferences, created = UserPreferences.objects.get_or_create(
                user=user,
                defaults={
                    'theme': 'light',
                    'accent_color': '#ff6b9e',
                    'font_size': 'medium',
                    'dashboard_layout': 'grid'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created preferences for {user.username}'))
            else:
                self.stdout.write(f'Preferences already exist for {user.username}')
