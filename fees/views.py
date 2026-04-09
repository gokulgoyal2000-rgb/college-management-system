from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FeeStructure, FeePayment
from accounts.models import StudentProfile
from django.db.models import Sum


@login_required
def fee_details(request):
    """
    View fee details
    """
    user = request.user
    
    if user.user_type == 'student':
        student = user.student_profile
        
        # Get fee structure for current semester
        fee_structure = FeeStructure.objects.filter(
            year=student.year,
            semester=student.semester
        ).first()
        
        # Get payment history
        payments = FeePayment.objects.filter(student=student)
        total_paid = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        
        pending_amount = 0
        if fee_structure:
            pending_amount = fee_structure.total_fee - total_paid
        
        context = {
            'fee_structure': fee_structure,
            'payments': payments,
            'total_paid': total_paid,
            'pending_amount': pending_amount,
        }
        return render(request, 'fees/student_fees.html', context)
    
    elif user.user_type == 'admin':
        fee_structures = FeeStructure.objects.all()
        recent_payments = FeePayment.objects.all()[:20]
        
        context = {
            'fee_structures': fee_structures,
            'recent_payments': recent_payments,
        }
        return render(request, 'fees/admin_fees.html', context)
    
    return redirect('accounts:dashboard')


@login_required
def add_payment(request):
    """
    Add fee payment
    Only admin
    """
    if request.user.user_type != 'admin':
        messages.error(request, 'Only admin can add payments.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        fee_structure_id = request.POST.get('fee_structure')
        amount_paid = request.POST.get('amount_paid')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')
        receipt_number = request.POST.get('receipt_number')
        status = request.POST.get('status')
        
        FeePayment.objects.create(
            student_id=student_id,
            fee_structure_id=fee_structure_id,
            amount_paid=amount_paid,
            payment_method=payment_method,
            transaction_id=transaction_id,
            receipt_number=receipt_number,
            status=status
        )
        
        messages.success(request, 'Payment added successfully!')
        return redirect('fees:details')
    
    students = StudentProfile.objects.all()
    fee_structures = FeeStructure.objects.all()
    
    context = {
        'students': students,
        'fee_structures': fee_structures,
    }
    
    return render(request, 'fees/add_payment.html', context)