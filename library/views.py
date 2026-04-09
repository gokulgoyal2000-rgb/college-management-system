from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, BookIssue
from accounts.models import StudentProfile, TeacherProfile
from django.utils import timezone


@login_required
def library_view(request):
    """
    View library books and issued books
    """
    user = request.user
    
    if user.user_type == 'student':
        student = user.student_profile
        issued_books = BookIssue.objects.filter(student=student, is_returned=False)
        history = BookIssue.objects.filter(student=student, is_returned=True)[:10]
        
        context = {
            'issued_books': issued_books,
            'history': history,
        }
        return render(request, 'library/student_library.html', context)
    
    elif user.user_type == 'teacher':
        teacher = user.teacher_profile
        issued_books = BookIssue.objects.filter(teacher=teacher, is_returned=False)
        history = BookIssue.objects.filter(teacher=teacher, is_returned=True)[:10]
        
        context = {
            'issued_books': issued_books,
            'history': history,
        }
        return render(request, 'library/teacher_library.html', context)
    
    elif user.user_type == 'admin':
        books = Book.objects.all()
        active_issues = BookIssue.objects.filter(is_returned=False)
        overdue_issues = active_issues.filter(due_date__lt=timezone.now().date())
        
        context = {
            'books': books,
            'active_issues': active_issues,
            'overdue_issues': overdue_issues,
        }
        return render(request, 'library/admin_library.html', context)
    
    return redirect('accounts:dashboard')


@login_required
def issue_book(request):
    """
    Issue a book
    Only admin
    """
    if request.user.user_type != 'admin':
        messages.error(request, 'Only admin can issue books.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        book_id = request.POST.get('book')
        member_type = request.POST.get('member_type')
        member_id = request.POST.get('member_id')
        
        book = Book.objects.get(id=book_id)
        
        if book.available_copies <= 0:
            messages.error(request, 'No copies available!')
            return redirect('library:view')
        
        issue_data = {
            'book': book,
            'member_type': member_type,
        }
        
        if member_type == 'student':
            issue_data['student_id'] = member_id
        else:
            issue_data['teacher_id'] = member_id
        
        BookIssue.objects.create(**issue_data)
        
        book.available_copies -= 1
        book.save()
        
        messages.success(request, 'Book issued successfully!')
        return redirect('library:view')
    
    books = Book.objects.filter(available_copies__gt=0)
    students = StudentProfile.objects.all()
    teachers = TeacherProfile.objects.all()
    
    context = {
        'books': books,
        'students': students,
        'teachers': teachers,
    }
    
    return render(request, 'library/issue_book.html', context)


@login_required
def return_book(request, issue_id):
    """
    Return a book and calculate fine if late
    Only admin
    """
    if request.user.user_type != 'admin':
        messages.error(request, 'Only admin can process returns.')
        return redirect('accounts:dashboard')
    
    issue = get_object_or_404(BookIssue, id=issue_id)
    
    issue.return_date = timezone.now().date()
    issue.is_returned = True
    issue.calculate_fine()
    issue.save()
    
    book = issue.book
    book.available_copies += 1
    book.save()
    
    messages.success(request, f'Book returned successfully! Fine: ₹{issue.fine_amount}')
    return redirect('library:view')