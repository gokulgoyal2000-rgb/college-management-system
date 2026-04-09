from django.db import models
from accounts.models import StudentProfile, TeacherProfile, Course
from django.utils import timezone

class Attendance(models.Model):
    """
    Records daily attendance for each student in each course
    """
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Prevent duplicate: same student, same course, same date
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']  # Newest first
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.course.code} - {self.date} - {self.status}"