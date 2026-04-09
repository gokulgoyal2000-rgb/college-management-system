from django.contrib import admin
from .models import TimeSlot

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'course', 'teacher', 'room_number']
    list_filter = ['day', 'department', 'year', 'semester']
    search_fields = ['course__code', 'teacher__user__username', 'room_number']