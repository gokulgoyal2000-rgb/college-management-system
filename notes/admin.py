from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'uploaded_by', 'uploaded_at']
    list_filter = ['course', 'uploaded_at']
    search_fields = ['title', 'course__code']