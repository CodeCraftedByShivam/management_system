from django import forms
from .models import Student, Course, Enrollment, Grade, Attendance, Announcement

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 
            'gender', 'address', 'city', 'state', 'postal_code', 'country',
            'student_id', 'status', 'profile_image', 'parent_name', 
            'parent_phone', 'emergency_contact', 'blood_group'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 1234567890'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '110001'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'India'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'STU001'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'parent_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Parent/Guardian name'
            }),
            'parent_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 9876543210'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 9876543210'
            }),
            'blood_group': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'A+, B+, O+, etc.'
            }),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'course_code', 'course_name', 'description', 'credits', 
            'instructor', 'duration_weeks', 'difficulty_level', 
            'max_students', 'fees', 'start_date', 'end_date', 'is_active'
        ]
        widgets = {
            'course_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CS101'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Introduction to Computer Science'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Course description...'
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'instructor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Professor name'
            }),
            'duration_weeks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '12'
            }),
            'difficulty_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '30'
            }),
            'fees': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '10000.00'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status', 'final_grade', 'completion_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'final_grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'A+, A, B+, etc.'
            }),
            'completion_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['enrollment', 'assignment_name', 'marks_obtained', 'total_marks', 'remarks']
        widgets = {
            'enrollment': forms.Select(attrs={'class': 'form-control'}),
            'assignment_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Assignment 1'
            }),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'total_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'remarks': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Teacher comments...'
            }),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['enrollment', 'date', 'status', 'remarks']
        widgets = {
            'enrollment': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Optional remarks...'
            }),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'priority', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Announcement title'
            }),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Announcement content...'
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
