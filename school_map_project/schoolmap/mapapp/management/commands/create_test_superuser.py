from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mapapp.models import UserPreferences

class Command(BaseCommand):
    help = 'Create a test superuser for admin dashboard testing'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@findit.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists')
            )
            return
        
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        
        # Create user preferences
        UserPreferences.objects.get_or_create(
            user=user,
            defaults={
                'theme': 'light',
                'accent_color': '#ff6b9e',
                'font_size': 'medium',
                'dashboard_layout': 'grid'
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created superuser "{username}" with password "{password}"'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'You can now login to the admin dashboard at /admin/ or /admin_dashboard/'
            )
        )