from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TimeSlot
from accounts.models import Course, TeacherProfile, Department


@login_required
def timetable_view(request):
    """
    View timetable
    Different for each user type
    """
    user = request.user
    
    if user.user_type == 'student':
        student = user.student_profile
        timetable = TimeSlot.objects.filter(
            department=student.department,
            year=student.year,
            semester=student.semester
        )
        
        # Organize by day
        schedule = {}
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        for day in days:
            schedule[day] = timetable.filter(day=day)
        
        context = {'schedule': schedule}
        return render(request, 'timetable/student_timetable.html', context)
    
    elif user.user_type == 'teacher':
        teacher = user.teacher_profile
        timetable = TimeSlot.objects.filter(teacher=teacher)
        
        # Organize by day
        schedule = {}
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        for day in days:
            schedule[day] = timetable.filter(day=day)
        
        context = {'schedule': schedule}
        return render(request, 'timetable/teacher_timetable.html', context)
    
    elif user.user_type == 'admin':
        timetables = TimeSlot.objects.all()
        context = {'timetables': timetables}
        return render(request, 'timetable/admin_timetable.html', context)
    
    return redirect('accounts:dashboard')


@login_required
def create_timeslot(request):
    """
    Create timetable slot
    Only admin
    """
    if request.user.user_type != 'admin':
        messages.error(request, 'Only admin can create timetable slots.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        course_id = request.POST.get('course')
        teacher_id = request.POST.get('teacher')
        room_number = request.POST.get('room_number')
        department_id = request.POST.get('department')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        
        TimeSlot.objects.create(
            day=day,
            start_time=start_time,
            end_time=end_time,
            course_id=course_id,
            teacher_id=teacher_id,
            room_number=room_number,
            department_id=department_id,
            year=year,
            semester=semester
        )
        
        messages.success(request, 'Timetable slot created successfully!')
        return redirect('timetable:view')
    
    courses = Course.objects.all()
    teachers = TeacherProfile.objects.all()
    departments = Department.objects.all()
    
    context = {
        'courses': courses,
        'teachers': teachers,
        'departments': departments,
    }
    
    return render(request, 'timetable/create_timeslot.html', context)