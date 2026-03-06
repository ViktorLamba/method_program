from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True)
    email = models.EmailField(unique=True)
    employee_code = models.CharField(max_length=20, unique=True)
    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r"^\+?[0-9]{10,15}$", "Введите корректный номер телефона.")],
    )
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class TeacherInfo(models.Model):
    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name="info",
    )
    biography = models.TextField()
    degree = models.CharField(max_length=100)
    office = models.CharField(max_length=50)
    years_of_experience = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0, message="Стаж не может быть меньше 0 лет."),
            MaxValueValidator(60, message="Стаж не может быть больше 60 лет."),
        ]
    )
    website = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("teacher__last_name",)

    def __str__(self):
        return f"Профиль: {self.teacher}"


class Student(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    student_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    enrollment_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(2000, message="Год поступления не может быть меньше 2000."),
            MaxValueValidator(2100, message="Год поступления не может быть больше 2100."),
        ]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Course(models.Model):
    title = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    credits = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Количество кредитов не может быть меньше 1."),
            MaxValueValidator(20, message="Количество кредитов не может быть больше 20."),
        ]
    )
    duration_weeks = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Длительность курса не может быть меньше 1 недели."),
            MaxValueValidator(52, message="Длительность курса не может быть больше 52 недель."),
        ]
    )
    starts_at = models.DateField()
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
    )
    students = models.ManyToManyField(
        Student,
        through="Enrollment",
        related_name="courses",
    )

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("student", "course"), name="unique_student_course"),
        ]
        ordering = ("-enrolled_at",)

    def __str__(self):
        return f"{self.student} -> {self.course}"
