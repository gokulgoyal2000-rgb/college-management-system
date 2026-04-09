from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from accounts.models import StudentProfile, TeacherProfile, Department, Course
from attendance.models import Attendance
from marks.models import Marks
from fees.models import FeePayment
from library.models import BookIssue
from django.utils import timezone
import json


@login_required
def analytics_dashboard(request):
    """
    Analytics dashboard with charts and statistics
    Only admin can access
    """
    if request.user.user_type != 'admin':
        messages.error(request, 'Only admin can access analytics.')
        return redirect('accounts:dashboard')
    
    # Overall Statistics
    total_students = StudentProfile.objects.count()
    total_teachers = TeacherProfile.objects.count()
    total_departments = Department.objects.count()
    total_courses = Course.objects.count()
    
    # Attendance Analytics
    total_attendance = Attendance.objects.count()
    present_count = Attendance.objects.filter(status='present').count()
    overall_attendance = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    # Department-wise attendance
    dept_attendance = []
    for dept in Department.objects.all():
        students = StudentProfile.objects.filter(department=dept)
        dept_records = Attendance.objects.filter(student__in=students)
        dept_total = dept_records.count()
        dept_present = dept_records.filter(status='present').count()
        dept_percentage = (dept_present / dept_total * 100) if dept_total > 0 else 0
        
        dept_attendance.append({
            'name': dept.name,
            'percentage': round(dept_percentage, 2)
        })
    
    # Performance Analytics
    avg_marks = Marks.objects.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    
    # Grade distribution
    grade_distribution = {
        'A+': Marks.objects.filter(grade='A+').count(),
        'A': Marks.objects.filter(grade='A').count(),
        'B+': Marks.objects.filter(grade='B+').count(),
        'B': Marks.objects.filter(grade='B').count(),
        'C': Marks.objects.filter(grade='C').count(),
        'D': Marks.objects.filter(grade='D').count(),
        'F': Marks.objects.filter(grade='F').count(),
    }
    
    # Fee Collection
    total_collected = FeePayment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    # Library Statistics
    total_books_issued = BookIssue.objects.count()
    books_overdue = BookIssue.objects.filter(
        is_returned=False,
        due_date__lt=timezone.now().date()
    ).count()
    
    # Low attendance students (below 75%)
    low_attendance_students = []
    for student in StudentProfile.objects.all():
        records = Attendance.objects.filter(student=student)
        total = records.count()
        present = records.filter(status='present').count()
        percentage = (present / total * 100) if total > 0 else 0
        
        if percentage < 75 and total > 0:
            low_attendance_students.append({
                'name': student.user.get_full_name(),
                'roll_number': student.roll_number,
                'percentage': round(percentage, 2)
            })
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'overall_attendance': round(overall_attendance, 2),
        'dept_attendance': json.dumps(dept_attendance),
        'avg_marks': round(avg_marks, 2),
        'grade_distribution': json.dumps(grade_distribution),
        'total_collected': total_collected,
        'total_books_issued': total_books_issued,
        'books_overdue': books_overdue,
        'low_attendance_students': low_attendance_students[:10],
    }
    
    return render(request, 'analytics/dashboard.html', context)