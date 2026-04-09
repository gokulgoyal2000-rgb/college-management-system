from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Custom User Model
class User(AbstractUser):
    """
    Extended User model to support different user types
    Inherits from AbstractUser (Django's built-in user model)
    """
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    
    # Which type of user (student/teacher/admin)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    # Phone number with validation (must be 10-15 digits)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Profile picture (optional)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Address (optional)
    address = models.TextField(blank=True)
    
    def __str__(self):
        # How this object will be displayed (e.g., in admin panel)
        return f"{self.username} - {self.user_type}"


class Department(models.Model):
    """
    Represents academic departments (CS, ECE, Mechanical, etc.)
    """
    name = models.CharField(max_length=100)  # e.g., "Computer Science"
    code = models.CharField(max_length=10, unique=True)  # e.g., "CS"
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Represents courses/subjects (e.g., Data Structures, DBMS)
    """
    name = models.CharField(max_length=100)  # e.g., "Data Structures"
    code = models.CharField(max_length=10, unique=True)  # e.g., "CS201"
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Which department
    credits = models.IntegerField()  # Course credits
    semester = models.IntegerField()  # Which semester
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class StudentProfile(models.Model):
    """
    Additional information specific to students
    OneToOne relationship with User model
    """
    YEAR_CHOICES = (
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    )
    
    # Link to User model (one user = one student profile)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES)
    semester = models.IntegerField()
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)
    
    # Many-to-Many: One student can have many courses
    courses = models.ManyToManyField(Course, related_name='students')
    
    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"


class TeacherProfile(models.Model):
    """
    Additional information specific to teachers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)  # e.g., "Assistant Professor"
    qualification = models.CharField(max_length=200)  # e.g., "PhD in Computer Science"
    joining_date = models.DateField()
    courses = models.ManyToManyField(Course, related_name='teachers')
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"


class AdminProfile(models.Model):
    """
    Additional information specific to admin users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"