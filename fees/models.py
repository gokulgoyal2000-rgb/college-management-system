from django.db import models
from accounts.models import StudentProfile
from django.utils import timezone

class FeeStructure(models.Model):
    """
    Fee structure for different years/semesters
    """
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]
    
    year = models.IntegerField()
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2)
    sports_fee = models.DecimalField(max_digits=10, decimal_places=2)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def total_fee(self):
        """
        Property method - accessed like a field but calculates value
        Usage: fee_structure.total_fee
        """
        return (self.tuition_fee + self.library_fee + self.lab_fee + 
                self.sports_fee + self.other_fee)
    
    def __str__(self):
        return f"Year {self.year} - Semester {self.semester}"


class FeePayment(models.Model):
    """
    Records of fee payments by students
    """
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('overdue', 'Overdue'),
    )
    
    PAYMENT_METHOD = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online Transfer'),
        ('cheque', 'Cheque'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)
    receipt_number = models.CharField(max_length=50, unique=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.receipt_number}"