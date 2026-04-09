from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment, AssignmentSubmission
from accounts.models import Course


@login_required
def assignment_list(request):
    """
    List all assignments
    Different view for students and teachers
    """
    user = request.user
    
    if user.user_type == 'student':
        student = user.student_profile
        assignments = Assignment.objects.filter(course__in=student.courses.all())
        
        # Get which assignments are already submitted
        submissions = AssignmentSubmission.objects.filter(student=student)
        submitted_ids = submissions.values_list('assignment_id', flat=True)
        
        context = {
            'assignments': assignments,
            'submitted_ids': submitted_ids,
            'submissions': submissions,
        }
        return render(request, 'assignments/student_assignments.html', context)
    
    elif user.user_type == 'teacher':
        teacher = user.teacher_profile
        assignments = Assignment.objects.filter(created_by=teacher)
        
        context = {
            'assignments': assignments,
        }
        return render(request, 'assignments/teacher_assignments.html', context)
    
    return redirect('accounts:dashboard')


@login_required
def create_assignment(request):
    """
    Create new assignment
    Only teachers
    """
    if request.user.user_type != 'teacher':
        messages.error(request, 'Only teachers can create assignments.')
        return redirect('accounts:dashboard')
    
    teacher = request.user.teacher_profile
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_id = request.POST.get('course')
        total_marks = request.POST.get('total_marks')
        deadline = request.POST.get('deadline')
        file = request.FILES.get('file')
        
        course = Course.objects.get(id=course_id)
        
        Assignment.objects.create(
            title=title,
            description=description,
            course=course,
            created_by=teacher,
            total_marks=total_marks,
            deadline=deadline,
            file=file
        )
        
        messages.success(request, 'Assignment created successfully!')
        return redirect('assignments:list')
    
    courses = teacher.courses.all()
    context = {'courses': courses}
    
    return render(request, 'assignments/create_assignment.html', context)


@login_required
def submit_assignment(request, assignment_id):
    """
    Submit assignment
    Only students
    """
    if request.user.user_type != 'student':
        messages.error(request, 'Only students can submit assignments.')
        return redirect('accounts:dashboard')
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student_profile
    
    # Check if already submitted
    if AssignmentSubmission.objects.filter(assignment=assignment, student=student).exists():
        messages.warning(request, 'You have already submitted this assignment.')
        return redirect('assignments:list')
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        remarks = request.POST.get('remarks', '')
        
        AssignmentSubmission.objects.create(
            assignment=assignment,
            student=student,
            file=file,
            remarks=remarks
        )
        
        messages.success(request, 'Assignment submitted successfully!')
        return redirect('assignments:list')
    
    context = {'assignment': assignment}
    return render(request, 'assignments/submit_assignment.html', context)


@login_required
def grade_submissions(request, assignment_id):
    """
    Grade assignment submissions
    Only teachers
    """
    if request.user.user_type != 'teacher':
        messages.error(request, 'Only teachers can grade assignments.')
        return redirect('accounts:dashboard')
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)
    
    if request.method == 'POST':
        for submission in submissions:
            marks = request.POST.get(f'marks_{submission.id}')
            feedback = request.POST.get(f'feedback_{submission.id}', '')
            
            if marks:
                submission.marks_obtained = marks
                submission.feedback = feedback
                submission.graded = True
                submission.save()
        
        messages.success(request, 'Submissions graded successfully!')
        return redirect('assignments:list')
    
    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    
    return render(request, 'assignments/grade_submissions.html', context)