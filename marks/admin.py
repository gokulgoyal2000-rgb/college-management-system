from django.contrib import admin
from .models import Marks

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'exam_type', 'marks_obtained', 'total_marks', 'grade']
    list_filter = ['exam_type', 'grade', 'course']
    search_fields = ['student__roll_number', 'course__code']