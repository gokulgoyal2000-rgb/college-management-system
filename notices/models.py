from django.db import models
from accounts.models import User
from django.utils import timezone

class Notice(models.Model):
    """
    Announcements/notices posted by teachers or admin
    """
    TARGET_CHOICES = (
        ('all', 'All'),
        ('students', 'Students'),
        ('teachers', 'Teachers'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    target_audience = models.CharField(max_length=10, choices=TARGET_CHOICES)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='notices/', blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Can be deactivated
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title