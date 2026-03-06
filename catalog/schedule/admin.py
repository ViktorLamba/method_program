from django.contrib import admin

from .models import Course, Enrollment, Student, Teacher, TeacherInfo


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "email", "employee_code", "is_active")
    search_fields = ("last_name", "first_name", "email", "employee_code")


@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "teacher", "degree", "office", "years_of_experience")
    search_fields = ("teacher__last_name", "teacher__first_name", "degree")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "code", "teacher", "credits", "starts_at")
    list_filter = ("teacher", "credits")
    search_fields = ("title", "code")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "email", "student_number", "is_active")
    search_fields = ("last_name", "first_name", "email", "student_number")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "course", "enrolled_at")
    list_filter = ("course",)
