from django.db import models
from django.utils.translation import gettext_lazy as _

class BuildingInfo(models.Model):
    """
    Model to store information about buildings in the school.
    """
    name = models.CharField(_('Building Name'), max_length=100, unique=True)
    code = models.CharField(
        _('Building Code'),
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Short code for the building (e.g., MAIN, GYM, LIB)')
    )
    description = models.TextField(_('Description'), blank=True, null=True)
    floor_count = models.PositiveIntegerField(_('Number of Floors'), default=1)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Building')
        verbose_name_plural = _('Buildings')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
