from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import UserPreferences, FindUsPoster

class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ['theme', 'accent_color', 'font_size', 'dashboard_layout']
        widgets = {
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
            'theme': forms.RadioSelect(attrs={'class': 'theme-radio'}),
            'font_size': forms.RadioSelect(attrs={'class': 'font-size-radio'}),
            'dashboard_layout': forms.RadioSelect(attrs={'class': 'layout-radio'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['theme'].widget.choices = UserPreferences.THEME_CHOICES
        self.fields['font_size'].widget.choices = UserPreferences.FONT_SIZE_CHOICES
        self.fields['dashboard_layout'].widget.choices = UserPreferences.LAYOUT_CHOICES

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name'
        })
    )
    lrn = forms.CharField(
        max_length=12,
        required=True,
        label='LRN (Learner Reference Number)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your LRN',
            'autocomplete': 'off'
        })
    )
    grade_section = forms.CharField(
        max_length=50,
        required=True,
        label='Grade Level - Section',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 10 - Newton',
            'autocomplete': 'off'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'lrn', 'grade_section')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Create a password',
                'autocomplete': 'new-password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password',
                'autocomplete': 'new-password'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username


class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name'
        })
    )
    faculty_id = forms.CharField(
        max_length=20,
        required=True,
        label='Faculty ID Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your faculty ID',
            'autocomplete': 'off'
        })
    )
    department = forms.ChoiceField(
        choices=[
            ('', 'Select your department'),
            ('math', 'Mathematics'),
            ('science', 'Science'),
            ('english', 'English'),
            ('filipino', 'Filipino'),
            ('ap', 'Araling Panlipunan'),
            ('tle', 'TLE'),
            ('mapeh', 'MAPEH'),
            ('values', 'Values Education'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'faculty_id', 'department')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Create a password',
                'autocomplete': 'new-password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password',
                'autocomplete': 'new-password'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username




class FindUsPosterForm(forms.ModelForm):
    class Meta:
        model = FindUsPoster
        fields = ['title', 'poster_image', 'video_file', 'youtube_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter poster title (optional)'
            }),
            'poster_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/watch?v=VIDEO_ID'
            })
        }
