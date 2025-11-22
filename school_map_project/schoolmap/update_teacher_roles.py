import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmap.settings')
django.setup()

from django.contrib.auth import get_user_model
from mapapp.models import UserProfile

def update_teacher_roles():
    # Get all users who registered through the teacher form
    # Since we don't have a direct way to identify teachers, we'll update all existing users
    # You can modify this logic based on your actual user identification method
    User = get_user_model()
    
    # Update all existing profiles to have the 'student' role by default
    # This is a one-time operation
    UserProfile.objects.update(role='student')
    
    # If you have a way to identify teachers (e.g., based on email or username pattern)
    # You can add that logic here. For example:
    # teachers = User.objects.filter(email__endswith='@school.edu')
    # for teacher in teachers:
    #     profile, created = UserProfile.objects.get_or_create(user=teacher)
    #     profile.role = 'teacher'
    #     profile.save()
    
    print("User roles have been updated.")

if __name__ == "__main__":
    update_teacher_roles()
