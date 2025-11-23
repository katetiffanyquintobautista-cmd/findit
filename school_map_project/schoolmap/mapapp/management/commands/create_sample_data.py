from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mapapp.models import UserPreferences, ActivityLog, BuildingInfo
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for testing dashboard analytics'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        sample_users = [
            {'username': 'student1', 'email': 'student1@school.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'student2', 'email': 'student2@school.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'teacher1', 'email': 'teacher1@school.com', 'first_name': 'Prof', 'last_name': 'Johnson'},
            {'username': 'student3', 'email': 'student3@school.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
            {'username': 'student4', 'email': 'student4@school.com', 'first_name': 'Sarah', 'last_name': 'Brown'},
        ]
        
        created_users = []
        for user_data in sample_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='password123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                
                # Create user preferences
                UserPreferences.objects.get_or_create(user=user)
                created_users.append(user)
                
                self.stdout.write(f'Created user: {user.username}')
        
        # Create sample buildings if they don't exist
        sample_buildings = [
            {'name': 'Main Building', 'description': 'Primary academic building with classrooms and offices'},
            {'name': 'Science Laboratory', 'description': 'Modern science labs for physics, chemistry, and biology'},
            {'name': 'Library', 'description': 'Multi-story library with study areas and computer lab'},
            {'name': 'Gymnasium', 'description': 'Sports facility with basketball court and fitness equipment'},
            {'name': 'Cafeteria', 'description': 'Student dining hall and food service area'},
        ]
        
        for building_data in sample_buildings:
            building, created = BuildingInfo.objects.get_or_create(
                name=building_data['name'],
                defaults={'description': building_data['description']}
            )
            if created:
                self.stdout.write(f'Created building: {building.name}')
        
        # Create sample activity logs for the past week
        now = timezone.now()
        all_users = User.objects.all()
        
        activities = [
            'user_login',
            'user_logout', 
            'user_registered',
            'building_added',
            'user_activated',
        ]
        
        # Create activities for the past 7 days
        for i in range(7):
            date = now - timedelta(days=i)
            
            # Create random number of activities for each day
            num_activities = random.randint(2, 8)
            
            for _ in range(num_activities):
                if all_users.exists():
                    user = random.choice(all_users)
                    action = random.choice(activities)
                    
                    # Create activity with random time on that day
                    activity_time = date.replace(
                        hour=random.randint(8, 17),
                        minute=random.randint(0, 59),
                        second=random.randint(0, 59)
                    )
                    
                    ActivityLog.objects.create(\n                        user=user,\n                        action=action,\n                        description=f'Sample activity: {action} by {user.username}',\n                        timestamp=activity_time,\n                        ip_address='127.0.0.1'\n                    )\n        \n        self.stdout.write(\n            self.style.SUCCESS('Successfully created sample data!')\n        )\n        self.stdout.write(\n            self.style.SUCCESS(\n                f'Created {len(created_users)} users and sample activity logs'\n            )\n        )