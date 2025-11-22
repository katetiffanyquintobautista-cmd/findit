from django.contrib import admin
from .models import BuildingInfo, FindUsPoster, HomePageContent, HomePageContent

@admin.register(BuildingInfo)
class BuildingInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'operating_hours', 'updated_at']
    search_fields = ['name']
    list_filter = ['updated_at']

@admin.register(FindUsPoster)
class FindUsPosterAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']
    actions = ['make_active', 'make_inactive']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'is_active')
        }),
        ('Media Content', {
            'fields': ('poster_image', 'video_file', 'youtube_url'),
            'description': 'Upload a poster image and optionally add a video (either upload a file OR provide a YouTube URL)'
        })
    )
    
    def make_active(self, request, queryset):
        # First deactivate all posters
        FindUsPoster.objects.update(is_active=False)
        # Then activate selected ones
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} poster(s) activated.')
    make_active.short_description = "Activate selected posters"
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} poster(s) deactivated.')
    make_inactive.short_description = "Deactivate selected posters"

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'is_active', 'updated_at']
    list_filter = ['is_active', 'announcement_active', 'updated_at']
    search_fields = ['site_title', 'welcome_title']
    
    fieldsets = (
        ('Main Content', {
            'fields': ('site_title', 'welcome_title', 'welcome_subtitle', 'welcome_description')
        }),
        ('Media', {
            'fields': ('logo_image', 'background_image')
        }),
        ('Announcements', {
            'fields': ('announcement_text', 'announcement_active')
        }),
        ('Settings', {
            'fields': ('is_active',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if obj.is_active:
            # Deactivate other home page contents
            HomePageContent.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)