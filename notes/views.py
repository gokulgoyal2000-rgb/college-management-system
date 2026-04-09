from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from accounts.models import Course


@login_required
def notes_list(request):
    """
    View all notes
    """
    user = request.user
    
    if user.user_type == 'student':
        student = user.student_profile
        notes = Note.objects.filter(course__in=student.courses.all())
        
        context = {'notes': notes}
        return render(request, 'notes/student_notes.html', context)
    
    elif user.user_type == 'teacher':
        teacher = user.teacher_profile
        notes = Note.objects.filter(uploaded_by=teacher)
        
        context = {'notes': notes}
        return render(request, 'notes/teacher_notes.html', context)
    
    return redirect('accounts:dashboard')


@login_required
def upload_note(request):
    """
    Upload new note
    Only teachers
    """
    if request.user.user_type != 'teacher':
        messages.error(request, 'Only teachers can upload notes.')
        return redirect('accounts:dashboard')
    
    teacher = request.user.teacher_profile
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_id = request.POST.get('course')
        file = request.FILES.get('file')
        
        course = Course.objects.get(id=course_id)
        
        Note.objects.create(
            title=title,
            description=description,
            course=course,
            file=file,
            uploaded_by=teacher
        )
        
        messages.success(request, 'Note uploaded successfully!')
        return redirect('notes:list')
    
    courses = teacher.courses.all()
    context = {'courses': courses}
    
    return render(request, 'notes/upload_note.html', context)