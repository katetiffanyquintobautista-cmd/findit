from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ActivityLog(models.Model):
    """
    Model to track user activities in the system.
    """
    ACTION_CHOICES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deleted', 'User Deleted'),
        ('building_created', 'Building Created'),
        ('building_updated', 'Building Updated'),
        ('building_deleted', 'Building Deleted'),
        ('profile_updated', 'Profile Updated'),
        ('password_changed', 'Password Changed'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs', null=True, blank=True)
    action = models.CharField(_('Action'), max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(_('Details'), blank=True, null=True)
    ip_address = models.GenericIPAddressField(_('IP Address'), blank=True, null=True)
    user_agent = models.TextField(_('User Agent'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), default=timezone.now)

    class Meta:
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_action_display()} - {self.user} - {self.created_at}"
