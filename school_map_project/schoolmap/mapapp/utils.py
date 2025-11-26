from .models import ActivityLog

ALLOWED_ACTIONS = {choice[0] for choice in ActivityLog.ACTION_CHOICES}

def log_activity(user, action, description, request=None):
    """Log user activity for analytics"""
    ip_address = None
    if request:
        ip_address = request.META.get('REMOTE_ADDR')

    action_value = action if action in ALLOWED_ACTIONS else 'other'
    details = description
    if action_value == 'other' and action:
        details = f"{action}: {description}"

    ActivityLog.objects.create(
        user=user,
        action=action_value,
        details=details,
        ip_address=ip_address
    )