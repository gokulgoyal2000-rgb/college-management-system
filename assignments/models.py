from django.db import models
from accounts.models import StudentProfile, TeacherProfile, Course
from django.utils import timezone

class Assignment(models.Model):
    """
    Assignments created by teachers
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    created_by = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    deadline = models.DateTimeField()
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    def is_overdue(self):
        """
        Method to check if assignment deadline has passed
        Returns True/False
        """
        return timezone.now() > self.deadline


class AssignmentSubmission(models.Model):
    """
    Student submissions for assignments
    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    remarks = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graded = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    
    class Meta:
        # One student can only submit once per assignment
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.assignment.title}"