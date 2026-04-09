from django.db import models
from accounts.models import StudentProfile, TeacherProfile, Course

class Marks(models.Model):
    """
    Stores marks for different types of exams
    Automatically calculates grade based on percentage
    """
    EXAM_TYPE_CHOICES = (
        ('midsem', 'Mid Semester'),
        ('final', 'Final Exam'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='marks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 85.50
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 100.00
    grade = models.CharField(max_length=2, blank=True)  # Auto-calculated
    remarks = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Updates automatically when saved
    
    class Meta:
        verbose_name_plural = 'Marks'  # Correct plural form
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """
        Override save method to auto-calculate grade
        This runs every time a Marks object is saved
        """
        # Calculate percentage
        percentage = (self.marks_obtained / self.total_marks) * 100
        
        # Assign grade based on percentage
        if percentage >= 90:
            self.grade = 'A+'
        elif percentage >= 80:
            self.grade = 'A'
        elif percentage >= 70:
            self.grade = 'B+'
        elif percentage >= 60:
            self.grade = 'B'
        elif percentage >= 50:
            self.grade = 'C'
        elif percentage >= 40:
            self.grade = 'D'
        else:
            self.grade = 'F'
        
        # Call parent class save method
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.course.code} - {self.exam_type}"