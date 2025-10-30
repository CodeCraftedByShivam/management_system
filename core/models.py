from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Graduated', 'Graduated'),
        ('Suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100, default='Unknown')
    state = models.CharField(max_length=100, default='Unknown')
    postal_code = models.CharField(max_length=10, default='000000')
    country = models.CharField(max_length=100, default='India')
    enrollment_date = models.DateField(auto_now_add=True)
    student_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    profile_image = models.ImageField(upload_to='students/', null=True, blank=True)
    parent_name = models.CharField(max_length=200, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    
    class Meta:
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    instructor = models.CharField(max_length=100)
    duration_weeks = models.IntegerField(default=12)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Beginner')
    max_students = models.IntegerField(default=30)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
    @property
    def enrolled_count(self):
        return self.enrollment_set.filter(status='Active').count()
    
    @property
    def seats_available(self):
        return self.max_students - self.enrolled_count

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Dropped', 'Dropped'),
        ('Failed', 'Failed'),
    ], default='Active')
    final_grade = models.CharField(max_length=2, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
    
    @property
    def average_grade(self):
        grades = self.grade_set.all()
        if grades:
            total = sum((g.marks_obtained / g.total_marks) * 100 for g in grades)
            return round(total / len(grades), 2)
        return 0

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=200)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.enrollment.student} - {self.assignment_name}"
    
    @property
    def percentage(self):
        return round((self.marks_obtained / self.total_marks) * 100, 2)
    
    @property
    def grade_letter(self):
        perc = self.percentage
        if perc >= 90: return 'A+'
        elif perc >= 80: return 'A'
        elif perc >= 70: return 'B+'
        elif perc >= 60: return 'B'
        elif perc >= 50: return 'C'
        elif perc >= 40: return 'D'
        else: return 'F'

class Attendance(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ])
    remarks = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('enrollment', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.enrollment.student} - {self.date} - {self.status}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    priority = models.CharField(max_length=20, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ], default='Medium')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
