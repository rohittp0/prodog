from django.contrib import admin

from home.models import Document, MaintenanceRequest, Announcement


# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)
    date_hierarchy = 'uploaded_at'
    list_per_page = 10


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_type', 'status', 'created_at')
    search_fields = ('request_type', 'status')
    list_filter = ('status',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['status']

        return super().get_readonly_fields(request, obj)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 10
