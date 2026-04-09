from django.db import models
from accounts.models import Course, TeacherProfile
from django.utils import timezone

class Note(models.Model):
    """
    Study notes uploaded by teachers for students
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    file = models.FileField(upload_to='notes/')  # PDF, DOCX, etc.
    uploaded_by = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"