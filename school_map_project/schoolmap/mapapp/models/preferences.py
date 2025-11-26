import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

def user_profile_picture_path(instance, filename):
    """
    Generates a file path for user profile pictures.
    The file will be uploaded to MEDIA_ROOT/profile_pics/user_<id>/<filename>
    """
    # Get the file extension
    ext = os.path.splitext(filename)[1]
    # Create a safe filename
    safe_username = slugify(instance.user.username)
    # Create the filename
    filename = f"profile_pic_{safe_username}{ext}"
    # Return the full path
    return os.path.join('profile_pics', f'user_{instance.user.id}', filename)

class Preferences(models.Model):
    """User preferences model."""

    # Theme choices
    THEME_LIGHT = 'light'
    THEME_DARK = 'dark'
    THEME_SUNSET = 'sunset'
    THEME_CHOICES = [
        (THEME_LIGHT, 'Light'),
        (THEME_DARK, 'Dark'),
        (THEME_SUNSET, 'Sunset'),
    ]

    # Font size choices (match UI expectations)
    FONT_SIZE_SMALL = 'small'
    FONT_SIZE_MEDIUM = 'medium'
    FONT_SIZE_LARGE = 'large'
    FONT_SIZE_XLARGE = 'xlarge'
    FONT_SIZE_CHOICES = [
        (FONT_SIZE_SMALL, 'Small'),
        (FONT_SIZE_MEDIUM, 'Medium'),
        (FONT_SIZE_LARGE, 'Large'),
        (FONT_SIZE_XLARGE, 'Extra Large'),
    ]

    # Layout choices
    LAYOUT_GRID = 'grid'
    LAYOUT_LIST = 'list'
    LAYOUT_CHOICES = [
        (LAYOUT_GRID, 'Grid View'),
        (LAYOUT_LIST, 'List View'),
    ]

    # User reference
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferences'
    )

    # Preference fields
    theme = models.CharField(
        _('Theme'),
        max_length=20,
        choices=THEME_CHOICES,
        default=THEME_LIGHT
    )

    font_size = models.CharField(
        _('Font Size'),
        max_length=10,
        choices=FONT_SIZE_CHOICES,
        default=FONT_SIZE_MEDIUM,
        help_text=_('Font size preference (small, medium, large)')
    )

    dashboard_layout = models.CharField(
        _('Dashboard Layout'),
        max_length=20,
        choices=LAYOUT_CHOICES,
        default=LAYOUT_GRID
    )

    accent_color = models.CharField(
        _('Accent Color'),
        max_length=7,  # For hex color codes like #RRGGBB
        default='#4a6baf',
        help_text=_('Primary color for the UI in hex format (e.g., #4a6baf)')
    )
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('User Preferences')
        verbose_name_plural = _('User Preferences')
        ordering = ['user__username']

    def __str__(self):
        return f"Preferences for {self.user.username}"
