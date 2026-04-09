from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Marks
from accounts.models import Course, StudentProfile
from django.db.models import Avg


@login_required
def marks_list(request):
    """
    View marks
    Different for students and teachers
    """
    user = request.user
    
    if user.user_type == 'student':
        student = user.student_profile
        marks = Marks.objects.filter(student=student)
        
        # Organize marks by course
        course_marks = {}
        for course in student.courses.all():
            course_records = marks.filter(course=course)
            midsem = course_records.filter(exam_type='midsem').first()
            final = course_records.filter(exam_type='final').first()
            
            course_marks[course] = {
                'midsem': midsem,
                'final': final,
                'all_marks': course_records
            }
        
        context = {
            'marks': marks,
            'course_marks': course_marks,
        }
        return render(request, 'marks/student_marks.html', context)
    
    elif user.user_type == 'teacher':
        teacher = user.teacher_profile
        courses = teacher.courses.all()
        
        context = {
            'courses': courses,
        }
        return render(request, 'marks/teacher_marks.html', context)
    
    return redirect('accounts:dashboard')


@login_required
def upload_marks(request, course_id):
    """
    Upload marks for a course
    Only teachers can access
    """
    if request.user.user_type != 'teacher':
        messages.error(request, 'Only teachers can upload marks.')
        return redirect('accounts:dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    teacher = request.user.teacher_profile
    
    # Check authorization
    if course not in teacher.courses.all():
        messages.error(request, 'You are not authorized to upload marks for this course.')
        return redirect('marks:list')
    
    students = StudentProfile.objects.filter(courses=course)
    
    if request.method == 'POST':
        exam_type = request.POST.get('exam_type')
        total_marks = request.POST.get('total_marks')
        
        for student in students:
            marks_obtained = request.POST.get(f'marks_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}', '')
            
            if marks_obtained:
                Marks.objects.create(
                    student=student,
                    course=course,
                    exam_type=exam_type,
                    marks_obtained=marks_obtained,
                    total_marks=total_marks,
                    remarks=remarks,
                    uploaded_by=teacher
                )
        
        messages.success(request, 'Marks uploaded successfully!')
        return redirect('marks:list')
    
    context = {
        'course': course,
        'students': students,
    }
    
    return render(request, 'marks/upload_marks.html', context)