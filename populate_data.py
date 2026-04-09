import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_management.settings')
django.setup()

from accounts.models import *
from attendance.models import *
from marks.models import *
from assignments.models import *
from notes.models import *
from timetable.models import *
from notices.models import *
from fees.models import *
from library.models import *
from django.utils import timezone
from datetime import timedelta, time
import random

print("="*60)
print("STARTING DATA POPULATION...")
print("="*60)

# Create Departments (or get existing)
print("\n1. Creating Departments...")
cs_dept, created = Department.objects.get_or_create(
    code="CS",
    defaults={
        "name": "Computer Science",
        "description": "Department of Computer Science and Engineering"
    }
)
if created:
    print("   ✓ Created CS department")
else:
    print("   ℹ CS department already exists")

ece_dept, created = Department.objects.get_or_create(
    code="ECE",
    defaults={
        "name": "Electronics & Communication",
        "description": "Department of Electronics and Communication Engineering"
    }
)
if created:
    print("   ✓ Created ECE department")
else:
    print("   ℹ ECE department already exists")

mech_dept, created = Department.objects.get_or_create(
    code="ME",
    defaults={
        "name": "Mechanical Engineering",
        "description": "Department of Mechanical Engineering"
    }
)
if created:
    print("   ✓ Created ME department")
else:
    print("   ℹ ME department already exists")

# Create Courses (or get existing)
print("\n2. Creating Courses...")
courses_data = [
    {"name": "Data Structures", "code": "CS201", "dept": cs_dept, "credits": 4, "sem": 3},
    {"name": "Database Management", "code": "CS202", "dept": cs_dept, "credits": 4, "sem": 3},
    {"name": "Operating Systems", "code": "CS301", "dept": cs_dept, "credits": 4, "sem": 5},
    {"name": "Computer Networks", "code": "CS302", "dept": cs_dept, "credits": 3, "sem": 5},
    {"name": "Digital Electronics", "code": "ECE201", "dept": ece_dept, "credits": 4, "sem": 3},
    {"name": "Signals and Systems", "code": "ECE202", "dept": ece_dept, "credits": 3, "sem": 3},
]

courses = []
for c_data in courses_data:
    course, created = Course.objects.get_or_create(
        code=c_data["code"],
        defaults={
            "name": c_data["name"],
            "department": c_data["dept"],
            "credits": c_data["credits"],
            "semester": c_data["sem"]
        }
    )
    courses.append(course)
    if created:
        print(f"   ✓ Created {course.code}")
    else:
        print(f"   ℹ {course.code} already exists")

# Handle Admin User
print("\n3. Checking Admin User...")
admin_user = User.objects.filter(username='admin').first()
if not admin_user:
    admin_user = User.objects.create_user(
        username='admin',
        password='admin123',
        email='admin@college.com',
        first_name='System',
        last_name='Administrator',
        user_type='admin',
        is_staff=True,
        is_superuser=True
    )
    print("   ✓ Created admin user")
else:
    print("   ℹ Admin user already exists")

# Create admin profile if doesn't exist
if not AdminProfile.objects.filter(user=admin_user).exists():
    AdminProfile.objects.create(
        user=admin_user,
        employee_id='ADM001',
        designation='System Administrator'
    )
    print("   ✓ Created admin profile")
else:
    print("   ℹ Admin profile already exists")

# Create Teachers
print("\n4. Creating Teachers...")
teachers = []
teacher_data = [
    {"username": "teacher1", "name": ["Dr. Rajesh", "Kumar"], "emp": "TCH001", "dept": cs_dept, "designation": "Professor"},
    {"username": "teacher2", "name": ["Dr. Priya", "Sharma"], "emp": "TCH002", "dept": cs_dept, "designation": "Assistant Professor"},
    {"username": "teacher3", "name": ["Dr. Amit", "Patel"], "emp": "TCH003", "dept": ece_dept, "designation": "Associate Professor"},
]

for t_data in teacher_data:
    user = User.objects.filter(username=t_data["username"]).first()
    
    if not user:
        user = User.objects.create_user(
            username=t_data["username"],
            password='teacher123',
            email=f'{t_data["username"]}@college.com',
            first_name=t_data["name"][0],
            last_name=t_data["name"][1],
            user_type='teacher'
        )
        print(f"   ✓ Created user {t_data['username']}")
    else:
        print(f"   ℹ User {t_data['username']} already exists")
    
    teacher = TeacherProfile.objects.filter(user=user).first()
    
    if not teacher:
        teacher = TeacherProfile.objects.create(
            user=user,
            employee_id=t_data["emp"],
            department=t_data["dept"],
            designation=t_data["designation"],
            qualification="PhD in " + t_data["dept"].name,
            joining_date=timezone.now().date() - timedelta(days=365)
        )
        print(f"   ✓ Created teacher profile {t_data['emp']}")
        
        # Assign courses
        if t_data["dept"] == cs_dept:
            teacher.courses.add(*[c for c in courses if c.department == cs_dept])
        else:
            teacher.courses.add(*[c for c in courses if c.department == ece_dept])
    else:
        print(f"   ℹ Teacher profile {t_data['emp']} already exists")
    
    teachers.append(teacher)

# Create Students
print("\n5. Creating Students...")
students = []
for i in range(1, 16):
    username = f'student{i}'
    user = User.objects.filter(username=username).first()
    
    if not user:
        dept = cs_dept if i <= 10 else ece_dept
        year = 2 if i <= 5 or (i > 10 and i <= 13) else 3
        semester = year * 2 - 1
        
        user = User.objects.create_user(
            username=username,
            password='student123',
            email=f'{username}@college.com',
            first_name='Student',
            last_name=f'Number{i}',
            user_type='student'
        )
        
        student = StudentProfile.objects.create(
            user=user,
            roll_number=f'{dept.code}{year}0{i:02d}',
            department=dept,
            year=year,
            semester=semester,
            date_of_birth=timezone.now().date() - timedelta(days=365*20)
        )
        
        # Enroll in courses
        dept_courses = [c for c in courses if c.department == dept and c.semester <= semester]
        student.courses.add(*dept_courses)
        
        students.append(student)
        print(f"   ✓ Created {username}")
    else:
        student = StudentProfile.objects.filter(user=user).first()
        if student:
            students.append(student)
            print(f"   ℹ {username} already exists")

# Create Attendance Records (only if none exist)
print("\n6. Creating Attendance Records...")
if Attendance.objects.count() == 0:
    attendance_count = 0
    for student in students:
        for course in student.courses.all():
            for days_ago in range(20):
                date = timezone.now().date() - timedelta(days=days_ago)
                status = random.choice(['present', 'present', 'present', 'absent'])
                
                Attendance.objects.create(
                    student=student,
                    course=course,
                    date=date,
                    status=status,
                    marked_by=course.teachers.first()
                )
                attendance_count += 1
    print(f"   ✓ Created {attendance_count} attendance records")
else:
    print(f"   ℹ Attendance records already exist ({Attendance.objects.count()} records)")

# Create Marks (only if none exist)
print("\n7. Creating Marks...")
if Marks.objects.count() == 0:
    marks_count = 0
    for student in students:
        for course in student.courses.all():
            # Midsem
            Marks.objects.create(
                student=student,
                course=course,
                exam_type='midsem',
                marks_obtained=random.randint(60, 95),
                total_marks=100,
                uploaded_by=course.teachers.first()
            )
            marks_count += 1
            
            # Final
            Marks.objects.create(
                student=student,
                course=course,
                exam_type='final',
                marks_obtained=random.randint(65, 98),
                total_marks=100,
                uploaded_by=course.teachers.first()
            )
            marks_count += 1
    print(f"   ✓ Created {marks_count} marks records")
else:
    print(f"   ℹ Marks already exist ({Marks.objects.count()} records)")

# Create Assignments (only if none exist)
print("\n8. Creating Assignments...")
if Assignment.objects.count() == 0:
    assignment_count = 0
    for course in courses:
        for i in range(3):
            Assignment.objects.create(
                title=f"{course.code} Assignment {i+1}",
                description=f"Complete the assignment on {course.name}",
                course=course,
                created_by=course.teachers.first(),
                total_marks=20,
                deadline=timezone.now() + timedelta(days=random.randint(5, 15))
            )
            assignment_count += 1
    print(f"   ✓ Created {assignment_count} assignments")
else:
    print(f"   ℹ Assignments already exist ({Assignment.objects.count()} assignments)")

# Create Notices (only if none exist)
print("\n9. Creating Notices...")
if Notice.objects.count() == 0:
    Notice.objects.create(
        title="Welcome to New Semester",
        content="Welcome all students to the new semester. Classes will begin from next Monday.",
        target_audience='all',
        posted_by=admin_user
    )
    Notice.objects.create(
        title="Mid-Semester Exams Schedule",
        content="Mid-semester exams will be conducted from 15th to 20th of next month.",
        target_audience='students',
        posted_by=teachers[0].user
    )
    Notice.objects.create(
        title="Faculty Meeting",
        content="All faculty members are requested to attend the meeting on Friday at 3 PM.",
        target_audience='teachers',
        posted_by=admin_user
    )
    print("   ✓ Created 3 notices")
else:
    print(f"   ℹ Notices already exist ({Notice.objects.count()} notices)")

# Create Fee Structure
print("\n10. Creating Fee Structure...")
for year_num in [2, 3]:
    semester_num = year_num * 2 - 1
    fee, created = FeeStructure.objects.get_or_create(
        year=year_num,
        semester=semester_num,
        defaults={
            "tuition_fee": 50000,
            "library_fee": 2000,
            "lab_fee": 5000,
            "sports_fee": 1000,
            "other_fee": 2000
        }
    )
    if created:
        print(f"   ✓ Created fee structure for Year {year_num}")
    else:
        print(f"   ℹ Fee structure for Year {year_num} already exists")

# Create Fee Payments (only if none exist)
print("\n11. Creating Fee Payments...")
if FeePayment.objects.count() == 0:
    payment_count = 0
    for student in students[:10]:
        fee_structure = FeeStructure.objects.filter(
            year=student.year,
            semester=student.semester
        ).first()
        
        if fee_structure:
            FeePayment.objects.create(
                student=student,
                fee_structure=fee_structure,
                amount_paid=fee_structure.total_fee,
                payment_method='online',
                transaction_id=f'TXN{student.roll_number}{int(timezone.now().timestamp())}',
                receipt_number=f'RCP{student.roll_number}',
                status='paid'
            )
            payment_count += 1
    print(f"   ✓ Created {payment_count} fee payments")
else:
    print(f"   ℹ Fee payments already exist ({FeePayment.objects.count()} payments)")

# Create Library Books
print("\n12. Creating Library Books...")
books_data = [
    {"title": "Introduction to Algorithms", "author": "Cormen", "isbn": "9780262033848", "category": "Computer Science"},
    {"title": "Database System Concepts", "author": "Silberschatz", "isbn": "9780078022159", "category": "Computer Science"},
    {"title": "Operating System Concepts", "author": "Galvin", "isbn": "9781118063330", "category": "Computer Science"},
    {"title": "Digital Design", "author": "Morris Mano", "isbn": "9780132774208", "category": "Electronics"},
    {"title": "Signals and Systems", "author": "Oppenheim", "isbn": "9780138147570", "category": "Electronics"},
]

books = []
for b_data in books_data:
    book, created = Book.objects.get_or_create(
        isbn=b_data["isbn"],
        defaults={
            "title": b_data["title"],
            "author": b_data["author"],
            "publisher": "Pearson",
            "publication_year": 2020,
            "category": b_data["category"],
            "total_copies": 5,
            "available_copies": 5,
            "shelf_location": f"A-{random.randint(1,20)}"
        }
    )
    books.append(book)
    if created:
        print(f"   ✓ Created book: {book.title}")
    else:
        print(f"   ℹ Book already exists: {book.title}")

# Issue Books (only if none issued)
print("\n13. Issuing Books...")
if BookIssue.objects.count() == 0:
    for i, student in enumerate(students[:5]):
        book = books[i % len(books)]
        BookIssue.objects.create(
            book=book,
            member_type='student',
            student=student,
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=14)
        )
        book.available_copies -= 1
        book.save()
    print(f"   ✓ Issued {min(5, len(students))} books")
else:
    print(f"   ℹ Books already issued ({BookIssue.objects.count()} issues)")

# Create Timetable (only if none exist)
print("\n14. Creating Timetable...")
if TimeSlot.objects.count() == 0:
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    times = [
        (time(9, 0), time(10, 0)),
        (time(10, 0), time(11, 0)),
        (time(11, 0), time(12, 0)),
        (time(14, 0), time(15, 0)),
        (time(15, 0), time(16, 0)),
    ]
    
    timeslot_count = 0
    course_idx = 0
    for day in days:
        for start, end in times:
            if course_idx < len(courses):
                course = courses[course_idx]
                TimeSlot.objects.create(
                    day=day,
                    start_time=start,
                    end_time=end,
                    course=course,
                    teacher=course.teachers.first(),
                    room_number=f'R-{random.randint(101, 310)}',
                    department=course.department,
                    year=2 if course.semester <= 4 else 3,
                    semester=course.semester
                )
                course_idx += 1
                timeslot_count += 1
    print(f"   ✓ Created {timeslot_count} timetable slots")
else:
    print(f"   ℹ Timetable already exists ({TimeSlot.objects.count()} slots)")

print("\n" + "="*60)
print("DATABASE POPULATED SUCCESSFULLY!")
print("="*60)
print("\n📚 SUMMARY:")
print(f"   • {Department.objects.count()} Departments")
print(f"   • {Course.objects.count()} Courses")
print(f"   • {StudentProfile.objects.count()} Students")
print(f"   • {TeacherProfile.objects.count()} Teachers")
print(f"   • {Attendance.objects.count()} Attendance Records")
print(f"   • {Marks.objects.count()} Marks Records")
print(f"   • {Assignment.objects.count()} Assignments")
print(f"   • {Notice.objects.count()} Notices")
print(f"   • {Book.objects.count()} Library Books")
print(f"   • {TimeSlot.objects.count()} Timetable Slots")

print("\n" + "="*60)
print("🔐 LOGIN CREDENTIALS:")
print("="*60)
print("\n👨‍💼 ADMIN:")
print("   Username: admin")
print("   Password: admin123")
print("\n👨‍🏫 TEACHERS:")
print("   Username: teacher1, teacher2, teacher3")
print("   Password: teacher123")
print("\n👨‍🎓 STUDENTS:")
print("   Username: student1 to student15")
print("   Password: student123")
print("="*60)
print("\n✅ You can now run: python manage.py runserver")
print("   Then login at: http://127.0.0.1:8000")
print("="*60)