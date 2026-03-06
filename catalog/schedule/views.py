from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CourseForm, StudentEnrollForm, StudentForm, TeacherForm, TeacherInfoForm
from .models import Course, Enrollment, Student, Teacher


def home(request):
    return render(request, "schedule/home.html")


def teacher_list(request):
    teachers = Teacher.objects.select_related("info").all()
    return render(request, "schedule/teacher_list.html", {"teachers": teachers})


def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher.objects.select_related("info"), id=teacher_id)
    return render(request, "schedule/teacher_detail.html", {"teacher": teacher})


def teacher_create(request):
    if request.method == "POST":
        teacher_form = TeacherForm(request.POST)
        info_form = TeacherInfoForm(request.POST)
        if teacher_form.is_valid() and info_form.is_valid():
            teacher = teacher_form.save()
            info = info_form.save(commit=False)
            info.teacher = teacher
            info.save()
            return redirect("schedule:teacher_list")
    else:
        teacher_form = TeacherForm()
        info_form = TeacherInfoForm()
    return render(
        request,
        "schedule/teacher_form.html",
        {"teacher_form": teacher_form, "info_form": info_form, "is_create": True},
    )


def teacher_update(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher_info = getattr(teacher, "info", None)
    if request.method == "POST":
        teacher_form = TeacherForm(request.POST, instance=teacher)
        info_form = TeacherInfoForm(request.POST, instance=teacher_info)
        if teacher_form.is_valid() and info_form.is_valid():
            teacher = teacher_form.save()
            info = info_form.save(commit=False)
            info.teacher = teacher
            info.save()
            return redirect("schedule:teacher_detail", teacher_id=teacher.id)
    else:
        teacher_form = TeacherForm(instance=teacher)
        info_form = TeacherInfoForm(instance=teacher_info)
    return render(
        request,
        "schedule/teacher_form.html",
        {"teacher_form": teacher_form, "info_form": info_form, "is_create": False, "teacher": teacher},
    )


def teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == "POST":
        teacher.delete()
        return redirect("schedule:teacher_list")
    return render(request, "schedule/teacher_delete.html", {"teacher": teacher})


def course_list(request):
    teacher_id = request.GET.get("teacher")
    courses = Course.objects.select_related("teacher").all()
    if teacher_id:
        courses = courses.filter(teacher_id=teacher_id)
    teachers = Teacher.objects.all()
    return render(
        request,
        "schedule/course_list.html",
        {"courses": courses, "teachers": teachers, "selected_teacher": teacher_id},
    )


def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("schedule:course_list")
    else:
        form = CourseForm()
    return render(request, "schedule/course_form.html", {"form": form, "is_create": True})


def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("schedule:course_list")
    else:
        form = CourseForm(instance=course)
    return render(
        request,
        "schedule/course_form.html",
        {"form": form, "is_create": False, "course": course},
    )


def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        return redirect("schedule:course_list")
    return render(request, "schedule/course_delete.html", {"course": course})


def student_list(request):
    students = Student.objects.prefetch_related("courses").all()
    return render(request, "schedule/student_list.html", {"students": students})


def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("schedule:student_list")
    else:
        form = StudentForm()
    return render(request, "schedule/student_form.html", {"form": form, "is_create": True})


def student_update(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("schedule:student_list")
    else:
        form = StudentForm(instance=student)
    return render(
        request,
        "schedule/student_form.html",
        {"form": form, "is_create": False, "student": student},
    )


def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        student.delete()
        return redirect("schedule:student_list")
    return render(request, "schedule/student_delete.html", {"student": student})


def student_enroll(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentEnrollForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data["course"]
            _, created = Enrollment.objects.get_or_create(student=student, course=course)
            if not created:
                messages.warning(request, "Студент уже записан на этот курс.")
            return redirect("schedule:student_list")
    else:
        form = StudentEnrollForm()
    return render(request, "schedule/student_enroll.html", {"form": form, "student": student})


def student_unenroll(request, student_id, course_id):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        Enrollment.objects.filter(student=student, course=course).delete()
        return redirect("schedule:student_list")
    return render(
        request,
        "schedule/student_unenroll.html",
        {"student": student, "course": course},
    )


def orm_queries(request):
    course_id = request.GET.get("course_id")
    min_courses = request.GET.get("min_courses", "1")
    min_courses_value = int(min_courses) if min_courses.isdigit() else 1

    students_for_course = Student.objects.none()
    selected_course = None
    if course_id and course_id.isdigit():
        selected_course = Course.objects.filter(id=course_id).first()
        if selected_course:
            students_for_course = Student.objects.filter(courses=selected_course).distinct()

    teachers_with_many_courses = Teacher.objects.annotate(course_count=Count("courses")).filter(
        course_count__gt=min_courses_value
    )
    students_without_courses = Student.objects.filter(courses__isnull=True).distinct()
    teachers_without_profile = Teacher.objects.filter(info__isnull=True)

    context = {
        "courses": Course.objects.all(),
        "selected_course": selected_course,
        "students_for_course": students_for_course,
        "teachers_with_many_courses": teachers_with_many_courses,
        "min_courses_value": min_courses_value,
        "students_without_courses": students_without_courses,
        "teachers_without_profile": teachers_without_profile,
    }
    return render(request, "schedule/orm_queries.html", context)
