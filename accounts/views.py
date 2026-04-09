from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserLoginForm, StudentProfileForm, TeacherProfileForm, UserProfileForm
from .models import StudentProfile, TeacherProfile, Course
from attendance.models import Attendance
from marks.models import Marks
from assignments.models import Assignment
from notices.models import Notice
from django.db.models import Avg, Count
from django.utils import timezone


def user_login(request):
    """
    Handle user login
    GET: Show login form
    POST: Process login
    """
    # If already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Create session
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """
    Logout user and redirect to login page
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    """
    Main dashboard - different view for each user type
    """
    user = request.user
    context = {'user': user}
    
    # Handle users without proper user_type
    if not hasattr(user, 'user_type') or not user.user_type:
        # If user is superuser/staff, treat as admin
        if user.is_superuser or user.is_staff:
            user.user_type = 'admin'
            user.save()
        else:
            # Redirect to profile to complete setup
            messages.warning(request, 'Please complete your profile setup.')
            return redirect('accounts:profile')
    
    if user.user_type == 'student':
        try:
            student = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            messages.error(request, 'Student profile not found. Please contact admin.')
            return render(request, 'accounts/dashboard.html', context)
        
        # Calculate attendance statistics
        attendance_records = Attendance.objects.filter(student=student)
        total_classes = attendance_records.count()
        present_classes = attendance_records.filter(status='present').count()
        attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
        
        # Get recent marks
        recent_marks = Marks.objects.filter(student=student).order_by('-created_at')[:5]
        
        # Get pending assignments (not yet submitted, deadline not passed)
        pending_assignments = Assignment.objects.filter(
            course__in=student.courses.all(),
            deadline__gte=timezone.now()
        ).exclude(submissions__student=student).order_by('deadline')[:5]
        
        # Get recent notices
        recent_notices = Notice.objects.filter(
            target_audience__in=['all', 'students'],
            is_active=True
        ).order_by('-created_at')[:5]
        
        context.update({
            'student': student,
            'attendance_percentage': round(attendance_percentage, 2),
            'total_classes': total_classes,
            'present_classes': present_classes,
            'recent_marks': recent_marks,
            'pending_assignments': pending_assignments,
            'recent_notices': recent_notices,
        })
        return render(request, 'accounts/student_dashboard.html', context)
    
    elif user.user_type == 'teacher':
        try:
            teacher = TeacherProfile.objects.get(user=user)
        except TeacherProfile.DoesNotExist:
            messages.error(request, 'Teacher profile not found. Please contact admin.')
            return render(request, 'accounts/dashboard.html', context)
        
        # Get courses taught
        courses = teacher.courses.all()
        
        # Count total students in all courses
        total_students = StudentProfile.objects.filter(courses__in=courses).distinct().count()
        
        # Get recent notices posted by this teacher
        recent_notices = Notice.objects.filter(posted_by=user).order_by('-created_at')[:5]
        
        # Count pending assignments to grade
        pending_grading = Assignment.objects.filter(
            course__in=courses,
            submissions__graded=False
        ).distinct().count()
        
        context.update({
            'teacher': teacher,
            'courses': courses,
            'total_students': total_students,
            'recent_notices': recent_notices,
            'pending_grading': pending_grading,
        })
        return render(request, 'accounts/teacher_dashboard.html', context)
    
    elif user.user_type == 'admin':
        # Get overall statistics
        total_students = StudentProfile.objects.count()
        total_teachers = TeacherProfile.objects.count()
        total_courses = Course.objects.count()
        
        # Get recent notices
        recent_notices = Notice.objects.all().order_by('-created_at')[:5]
        
        context.update({
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'recent_notices': recent_notices,
        })
        return render(request, 'accounts/admin_dashboard.html', context)
    
    # Fallback for any other case
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile(request):
    """
    View and edit user profile
    """
    user = request.user
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        
        # Get appropriate profile form based on user type
        if user.user_type == 'student':
            profile_form = StudentProfileForm(request.POST, instance=user.student_profile)
        elif user.user_type == 'teacher':
            profile_form = TeacherProfileForm(request.POST, instance=user.teacher_profile)
        else:
            profile_form = None
        
        # Validate and save both forms
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserProfileForm(instance=user)
        
        if user.user_type == 'student':
            profile_form = StudentProfileForm(instance=user.student_profile)
        elif user.user_type == 'teacher':
            profile_form = TeacherProfileForm(instance=user.teacher_profile)
        else:
            profile_form = None
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'accounts/profile.html', context)