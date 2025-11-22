import os
from django.db import models
from django.contrib.auth.models import User

def user_profile_picture_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/profile_pics/user_<id>/<filename>
    ext = filename.split('.')[-1]
    filename = f"profile_pic.{ext}"
    return os.path.join('profile_pics', f'user_{instance.user.id}', filename)

class UserPreferences(models.Model):
    THEME_CHOICES = [
        ('light', '🌞 Light'),
        ('dark', '🌙 Dark'),
        ('sunset', '🌇 Sunset'),
    ]
    
    FONT_SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    
    LAYOUT_CHOICES = [
        ('grid', 'Grid'),
        ('list', 'List'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    accent_color = models.CharField(max_length=7, default='#ff6b9e')
    font_size = models.CharField(max_length=10, choices=FONT_SIZE_CHOICES, default='medium')
    dashboard_layout = models.CharField(max_length=10, choices=LAYOUT_CHOICES, default='grid')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s preferences"

class BuildingInfo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='building_images/', blank=True, null=True)
    operating_hours = models.CharField(max_length=100, default="Monday - Friday: 7:00 AM - 6:00 PM")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FindUsPoster(models.Model):
    title = models.CharField(max_length=100, default="Find Us")
    poster_image = models.ImageField(upload_to='find_us_posters/', blank=True, null=True)
    
    # Video fields
    video_file = models.FileField(upload_to='find_us_videos/', blank=True, null=True, help_text="Upload a video file (MP4, WebM, etc.)")
    youtube_url = models.URLField(blank=True, null=True, help_text="YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def get_youtube_embed_id(self):
        """Extract YouTube video ID from URL for embedding"""
        if not self.youtube_url:
            return None
        
        import re
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)',
            r'youtube\.com/embed/([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return match.group(1)
        return None

class HomePageContent(models.Model):
    # Main content sections
    site_title = models.CharField(max_length=100, default="FINDIT - School Map")
    welcome_title = models.CharField(max_length=200, default="School Campus Map")
    welcome_subtitle = models.CharField(max_length=300, default="Welcome back, {username}!")
    welcome_description = models.TextField(default="Navigate your campus with ease - Find buildings, rooms, and more. Use the interactive map to explore facilities and get directions.")
    
    # Logo and branding
    logo_image = models.ImageField(upload_to='home_content/', blank=True, null=True)
    
    # Announcements
    announcement_text = models.TextField(blank=True, help_text="Important announcements to display on home page")
    announcement_active = models.BooleanField(default=False)
    
    # Background and styling
    background_image = models.ImageField(upload_to='home_content/', blank=True, null=True)
    
    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Home Page Content - {self.updated_at.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active home page content
        if self.is_active:
            HomePageContent.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)