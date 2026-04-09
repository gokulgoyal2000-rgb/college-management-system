from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notice


@login_required
def notice_list(request):
    """
    View notices based on user type
    """
    user = request.user
    
    if user.user_type == 'student':
        notices = Notice.objects.filter(
            target_audience__in=['all', 'students'],
            is_active=True
        )
    elif user.user_type == 'teacher':
        notices = Notice.objects.filter(
            target_audience__in=['all', 'teachers'],
            is_active=True
        )
    else:
        notices = Notice.objects.filter(is_active=True)
    
    context = {'notices': notices}
    return render(request, 'notices/notice_list.html', context)


@login_required
def create_notice(request):
    """
    Create new notice
    Only teachers and admin
    """
    if request.user.user_type not in ['teacher', 'admin']:
        messages.error(request, 'Only teachers and admin can create notices.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        target_audience = request.POST.get('target_audience')
        file = request.FILES.get('file')
        
        Notice.objects.create(
            title=title,
            content=content,
            target_audience=target_audience,
            posted_by=request.user,
            file=file
        )
        
        messages.success(request, 'Notice posted successfully!')
        return redirect('notices:list')
    
    return render(request, 'notices/create_notice.html')