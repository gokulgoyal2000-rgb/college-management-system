from django.db import models
from accounts.models import StudentProfile, TeacherProfile
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    """
    Library books catalog
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    category = models.CharField(max_length=100)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    shelf_location = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.title} - {self.author}"


class BookIssue(models.Model):
    """
    Track which books are issued to which members
    """
    MEMBER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPE_CHOICES)
    
    # Either student OR teacher (only one will have value)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True)
    
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_returned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-issue_date']
    
    def save(self, *args, **kwargs):
        """
        Auto-set due date to 14 days from issue date
        """
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(days=14)
        super().save(*args, **kwargs)
    
    def calculate_fine(self):
        """
        Calculate fine for late returns
        ₹5 per day after due date
        """
        if self.is_returned and self.return_date:
            if self.return_date > self.due_date:
                days_late = (self.return_date - self.due_date).days
                self.fine_amount = days_late * 5
                self.save()
    
    def __str__(self):
        member = self.student if self.student else self.teacher
        return f"{self.book.title} - {member}"