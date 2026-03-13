from django.contrib import admin
from .models import StudentProfile, TeacherProfile, Subject, CareerPath


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


class CareerPathInline(admin.TabularInline):
    model = CareerPath
    extra = 1


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department']
    search_fields = ['user__username', 'employee_id']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_number', 'department', 'semester', 'cgpa', 'attendance', 'risk_level']
    list_filter = ['risk_level', 'department']
    list_editable = ['cgpa', 'attendance', 'risk_level']
    search_fields = ['user__username', 'roll_number']
    inlines = [SubjectInline, CareerPathInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'student', 'marks_obtained', 'max_marks']


@admin.register(CareerPath)
class CareerPathAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'match_score', 'created_at']
