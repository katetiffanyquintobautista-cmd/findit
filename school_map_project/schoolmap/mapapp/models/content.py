from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class FindUsPoster(models.Model):
    """
    Model to store the "Find Us" poster, video, and YouTube URL.
    """
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True, null=True)
    
    # Image field for the poster
    poster_image = models.ImageField(
        _('Poster Image'),
        upload_to='posters/',
        blank=True,
        null=True,
        help_text=_('Upload a poster image (JPEG, PNG, etc.)')
    )
    
    # Video file upload
    video_file = models.FileField(
        _('Video File'),
        upload_to='videos/',
        blank=True,
        null=True,
        help_text=_('Upload a video file (MP4, WebM, etc.)')
    )
    
    # YouTube URL
    youtube_url = models.URLField(
        _('YouTube URL'),
        blank=True,
        null=True,
        help_text=_('Or enter a YouTube video URL')
    )
    
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Find Us Media')
        verbose_name_plural = _('Find Us Media')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        """
        Ensure that either a video file or a YouTube URL is provided, but not both.
        """
        if self.video_file and self.youtube_url:
            raise ValidationError(_('Please provide either a video file or a YouTube URL, not both.'))
        if not self.video_file and not self.youtube_url and not self.poster_image:
            raise ValidationError(_('Please provide either a poster image, a video file, or a YouTube URL.'))

    def has_video(self):
        """Check if the poster has a video (either file or YouTube URL)."""
        return bool(self.video_file or self.youtube_url)

    def get_video_type(self):
        """Return the type of video (file or YouTube) or None if no video."""
        if self.video_file:
            return 'file'
        elif self.youtube_url:
            return 'youtube'
        return None


class HomePageContent(models.Model):
    """
    Model to store content for the home page.
    """
    section = models.CharField(
        _('Section'),
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text=_('A unique identifier for this section (e.g., "welcome", "about", "contact")')
    )
    title = models.CharField(
        _('Title'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_('The title to display for this section')
    )
    content = models.TextField(
        _('Content'),
        blank=True,
        null=True,
        help_text=_('Content for this section (can include HTML)')
    )
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Home Page Content')
        verbose_name_plural = _('Home Page Contents')
        ordering = ['section']

    def __str__(self):
        return f"{self.section} - {self.title}"
