from django.contrib import admin
from .models import Assignment, AssignmentSubmission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_by', 'deadline', 'total_marks']
    list_filter = ['course', 'deadline']
    search_fields = ['title', 'course__code']

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'graded', 'marks_obtained']
    list_filter = ['graded', 'submitted_at']
    search_fields = ['student__roll_number', 'assignment__title']