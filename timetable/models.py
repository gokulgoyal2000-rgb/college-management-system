from django.db import models
from accounts.models import Course, TeacherProfile, Department

class TimeSlot(models.Model):
    """
    Class schedule for each department/year/semester
    """
    DAYS_OF_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
    
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()  # e.g., 09:00
    end_time = models.TimeField()    # e.g., 10:00
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    
    class Meta:
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.day} - {self.start_time} - {self.course.code}"