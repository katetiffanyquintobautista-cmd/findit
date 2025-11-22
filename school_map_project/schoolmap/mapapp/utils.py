from .models import ActivityLog

def log_activity(user, action, description, request=None):
    """Log user activity for analytics"""
    ip_address = None
    if request:
        ip_address = request.META.get('REMOTE_ADDR')
    
    ActivityLog.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=ip_address
    )