from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date', 'course']
    search_fields = ['student__roll_number', 'course__code']
    date_hierarchy = 'date'