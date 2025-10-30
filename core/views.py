from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from .models import Student, Course, Enrollment, Grade, Attendance, Announcement
from .forms import StudentForm, CourseForm, EnrollmentForm, GradeForm, AttendanceForm

# Landing Page
def landing_page(request):
    return render(request, 'landing.html')

# Dashboard
def dashboard(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='Active').count()
    total_courses = Course.objects.count()
    active_courses = Course.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.count()
    active_enrollments = Enrollment.objects.filter(status='Active').count()
    
    # Recent students
    recent_students = Student.objects.all()[:5]
    
    # Recent enrollments
    recent_enrollments = Enrollment.objects.select_related('student', 'course')[:5]
    
    # Announcements
    announcements = Announcement.objects.filter(is_active=True)[:3]
    
    # Course statistics
    course_stats = Course.objects.annotate(
        enrolled=Count('enrollment', filter=Q(enrollment__status='Active'))
    ).order_by('-enrolled')[:5]
    
    context = {
        'total_students': total_students,
        'active_students': active_students,
        'total_courses': total_courses,
        'active_courses': active_courses,
        'total_enrollments': total_enrollments,
        'active_enrollments': active_enrollments,
        'recent_students': recent_students,
        'recent_enrollments': recent_enrollments,
        'announcements': announcements,
        'course_stats': course_stats,
    }
    return render(request, 'dashboard.html', context)

# Student Views
def student_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    students = Student.objects.all()
    
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(email__icontains=query)
        )
    
    if status_filter:
        students = students.filter(status=status_filter)
    
    students = students.order_by('-enrollment_date')
    
    context = {
        'students': students,
        'query': query,
        'status_filter': status_filter,
    }
    return render(request, 'student_list.html', context)

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} added successfully!')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form, 'title': 'Add New Student'})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student {student.full_name} updated successfully!')
            return redirect('student_detail', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form, 'title': 'Edit Student'})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student_name = student.full_name
        student.delete()
        messages.success(request, f'Student {student_name} deleted successfully!')
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    
    # Calculate statistics
    total_courses = enrollments.count()
    active_courses = enrollments.filter(status='Active').count()
    completed_courses = enrollments.filter(status='Completed').count()
    
    # Get recent grades
    recent_grades = Grade.objects.filter(enrollment__student=student).order_by('-date')[:5]
    
    # Get attendance summary
    total_classes = Attendance.objects.filter(enrollment__student=student).count()
    present_count = Attendance.objects.filter(enrollment__student=student, status='Present').count()
    attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'total_courses': total_courses,
        'active_courses': active_courses,
        'completed_courses': completed_courses,
        'recent_grades': recent_grades,
        'attendance_percentage': round(attendance_percentage, 2),
    }
    return render(request, 'student_detail.html', context)

# Course Views
def course_list(request):
    query = request.GET.get('q', '')
    difficulty = request.GET.get('difficulty', '')
    
    courses = Course.objects.all()
    
    if query:
        courses = courses.filter(
            Q(course_code__icontains=query) |
            Q(course_name__icontains=query) |
            Q(instructor__icontains=query)
        )
    
    if difficulty:
        courses = courses.filter(difficulty_level=difficulty)
    
    courses = courses.annotate(enrolled=Count('enrollment', filter=Q(enrollment__status='Active')))
    
    context = {
        'courses': courses,
        'query': query,
        'difficulty': difficulty,
    }
    return render(request, 'course_list.html', context)

def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course {course.course_name} added successfully!')
            return redirect('course_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form, 'title': 'Add New Course'})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    
    context = {
        'course': course,
        'enrollments': enrollments,
    }
    return render(request, 'course_detail.html', context)
