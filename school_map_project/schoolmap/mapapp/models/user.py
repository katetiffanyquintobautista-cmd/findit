from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier."""
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
            
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    """Custom user model with additional fields for security."""
    email = models.EmailField(_('email address'), unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    
    # Student specific fields
    lrn = models.CharField(max_length=12, blank=True, null=True, validators=[MinLengthValidator(12)])
    grade_section = models.CharField(max_length=50, blank=True, null=True)
    
    # Teacher specific fields
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    # Make email required
    email = models.EmailField(_('email address'), unique=True)
    
    # Set email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Remove 'email' from REQUIRED_FIELDS
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    last_password_change = models.DateTimeField(default=timezone.now)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Override the default user manager with our custom one
    objects = CustomUserManager()

    # Make email the main identifier instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def increment_failed_login_attempts(self):
        """Increment the failed login counter and lock the account if needed."""
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        
        # Lock account after 5 failed attempts for 15 minutes
        if self.failed_login_attempts >= 5:
            self.account_locked_until = timezone.now() + timezone.timedelta(minutes=15)
            
        self.save(update_fields=['failed_login_attempts', 'last_failed_login', 'account_locked_until'])
    
    def reset_login_attempts(self):
        """Reset the failed login counter."""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])
    
    def is_account_locked(self):
        """Check if the account is currently locked."""
        if self.account_locked_until:
            if timezone.now() < self.account_locked_until:
                return True
            else:
                # If lockout period has passed, reset the lock
                self.reset_login_attempts()
        return False
    
    def update_last_login_ip(self, ip_address):
        """Update the last login IP address."""
        self.last_login_ip = ip_address
        self.save(update_fields=['last_login_ip'])
    
    def update_password(self, new_password):
        """Update the user's password and reset the last password change date."""
        self.set_password(new_password)
        self.last_password_change = timezone.now()
        self.save(update_fields=['password', 'last_password_change'])
        self.reset_login_attempts()
