from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
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

CustomUser = get_user_model()


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
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        user.is_student = True
        user.lrn = self.cleaned_data['lrn']
        user.grade_section = self.cleaned_data['grade_section']
        if commit:
            user.save()
        return user


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
    grade_level = forms.CharField(
        max_length=50,
        required=True,
        label='Grade Level Teaching',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Grade 7, Grade 8-10, All Grades',
            'autocomplete': 'off'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        user.is_teacher = True
        user.employee_id = self.cleaned_data['faculty_id']
        user.department = self.cleaned_data['department']
        # Store teaching level in grade_section for now; adjust if a dedicated field is added later
        user.grade_section = self.cleaned_data['grade_level']
        if commit:
            user.save()
        return user




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
    
    def clean(self):
        cleaned_data = super().clean()
        poster_image = cleaned_data.get('poster_image')
        video_file = cleaned_data.get('video_file')
        youtube_url = cleaned_data.get('youtube_url')
        
        if not any([poster_image, video_file, youtube_url]):
            raise ValidationError('Please provide at least one content type: an image, video file, or YouTube URL.')
        
        return cleaned_data
    
    def clean_youtube_url(self):
        youtube_url = self.cleaned_data.get('youtube_url')
        if youtube_url:
            import re
            patterns = [
                r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)',
                r'youtube\.com/embed/([a-zA-Z0-9_-]+)'
            ]
            
            valid = False
            for pattern in patterns:
                if re.search(pattern, youtube_url):
                    valid = True
                    break
            
            if not valid:
                raise ValidationError('Please enter a valid YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)')
        
        return youtube_url
