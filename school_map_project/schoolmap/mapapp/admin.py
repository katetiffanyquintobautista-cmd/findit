from django.contrib import admin
from .models import BuildingInfo, FindUsPoster, HomePageContent

@admin.register(BuildingInfo)
class BuildingInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'floor_count', 'is_active', 'updated_at']
    search_fields = ['name', 'code']
    list_filter = ['is_active', 'updated_at']

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
    list_display = ['section', 'title', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['section', 'title', 'content']
    fieldsets = (
        ('Section Info', {
            'fields': ('section', 'title', 'is_active')
        }),
        ('Content', {
            'fields': ('content',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            HomePageContent.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)