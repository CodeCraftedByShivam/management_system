from django.contrib import admin
from .models import Student, Course, Enrollment, Grade, Attendance, Announcement

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'email', 'status', 'city', 'enrollment_date']
    list_filter = ['status', 'gender', 'city', 'enrollment_date']
    search_fields = ['student_id', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['enrollment_date']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender', 'blood_group', 'profile_image')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Academic Information', {
            'fields': ('student_id', 'status', 'enrollment_date')
        }),
        ('Emergency Contact', {
            'fields': ('parent_name', 'parent_phone', 'emergency_contact')
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'difficulty_level', 'credits', 'instructor', 'enrolled_count', 'seats_available', 'is_active']
    list_filter = ['difficulty_level', 'is_active', 'start_date']
    search_fields = ['course_code', 'course_name', 'instructor']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course_code', 'course_name', 'description', 'difficulty_level')
        }),
        ('Academic Details', {
            'fields': ('credits', 'duration_weeks', 'instructor')
        }),
        ('Enrollment', {
            'fields': ('max_students', 'fees', 'is_active')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'status', 'final_grade', 'average_grade']
    list_filter = ['status', 'enrollment_date']
    search_fields = ['student__first_name', 'student__last_name', 'course__course_name']
    readonly_fields = ['enrollment_date', 'average_grade']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'assignment_name', 'marks_obtained', 'total_marks', 'percentage', 'grade_letter', 'date']
    list_filter = ['date']
    search_fields = ['enrollment__student__first_name', 'enrollment__student__last_name', 'assignment_name']
    readonly_fields = ['date', 'percentage', 'grade_letter']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'date', 'status', 'remarks']
    list_filter = ['status', 'date']
    search_fields = ['enrollment__student__first_name', 'enrollment__student__last_name']
    date_hierarchy = 'date'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active', 'created_at']
    list_filter = ['priority', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at']
