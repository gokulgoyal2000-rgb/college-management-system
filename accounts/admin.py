from django.contrib import admin
from .models import User, Department, Course, StudentProfile, TeacherProfile, AdminProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'first_name', 'last_name']
    list_filter = ['user_type']
    search_fields = ['username', 'email', 'first_name', 'last_name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'credits', 'semester']
    list_filter = ['department', 'semester']
    search_fields = ['name', 'code']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'user', 'department', 'year', 'semester']
    list_filter = ['department', 'year', 'semester']
    search_fields = ['roll_number', 'user__username']

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'department', 'designation']
    list_filter = ['department']
    search_fields = ['employee_id', 'user__username']

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'designation']
    search_fields = ['employee_id', 'user__username']