from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_audience', 'posted_by', 'is_active', 'created_at']
    list_filter = ['target_audience', 'is_active', 'created_at']
    search_fields = ['title', 'content']