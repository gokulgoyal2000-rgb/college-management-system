from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from accounts.models import StudentProfile, Course
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


@login_required
def attendance_list(request):
    """
    View attendance records
    Different view for students and teachers
    """
    user = request.user
    
    if user.user_type == 'student':
        student = user.student_profile
        attendances = Attendance.objects.filter(student=student)
        
        # Calculate overall attendance percentage
        total = attendances.count()
        present = attendances.filter(status='present').count()
        percentage = (present / total * 100) if total > 0 else 0
        
        # Calculate course-wise attendance
        course_attendance = {}
        for course in student.courses.all():
            course_records = attendances.filter(course=course)
            course_total = course_records.count()
            course_present = course_records.filter(status='present').count()
            course_percentage = (course_present / course_total * 100) if course_total > 0 else 0
            
            course_attendance[course] = {
                'total': course_total,
                'present': course_present,
                'percentage': round(course_percentage, 2),
                'records': course_records[:10]  # Latest 10 records
            }
        
        context = {
            'attendances': attendances[:20],
            'total': total,
            'present': present,
            'percentage': round(percentage, 2),
            'course_attendance': course_attendance,
        }
        return render(request, 'attendance/student_attendance.html', context)
    
    elif user.user_type == 'teacher':
        teacher = user.teacher_profile
        courses = teacher.courses.all()
        
        context = {
            'courses': courses,
        }
        return render(request, 'attendance/teacher_attendance.html', context)
    
    return redirect('accounts:dashboard')


@login_required
def mark_attendance(request, course_id):
    """
    Mark attendance for a course
    Only teachers can access this
    """
    # Check if user is teacher
    if request.user.user_type != 'teacher':
        messages.error(request, 'Only teachers can mark attendance.')
        return redirect('accounts:dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    teacher = request.user.teacher_profile
    
    # Check if teacher teaches this course
    if course not in teacher.courses.all():
        messages.error(request, 'You are not authorized to mark attendance for this course.')
        return redirect('attendance:list')
    
    # Get all students enrolled in this course
    students = StudentProfile.objects.filter(courses=course)
    today = timezone.now().date()
    
    if request.method == 'POST':
        # Process attendance form
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}', '')
            
            if status:
                # Update or create attendance record
                Attendance.objects.update_or_create(
                    student=student,
                    course=course,
                    date=today,
                    defaults={
                        'status': status,
                        'marked_by': teacher,
                        'remarks': remarks
                    }
                )
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('attendance:list')
    
    # Get existing attendance for today (if already marked)
    existing_attendance = {}
    for att in Attendance.objects.filter(course=course, date=today):
        existing_attendance[att.student.id] = att
    
    context = {
        'course': course,
        'students': students,
        'today': today,
        'existing_attendance': existing_attendance,
    }
    
    return render(request, 'attendance/mark_attendance.html', context)