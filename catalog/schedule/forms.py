from django import forms

from .models import Course, Student, Teacher, TeacherInfo


REQUIRED_FIELD_ERROR = "Это поле обязательно для заполнения."
GENERIC_INVALID_ERROR = "Введите корректное значение."
INVALID_EMAIL_ERROR = "Введите корректный адрес электронной почты."
INVALID_DATE_ERROR = "Введите дату в формате ГГГГ-ММ-ДД."
INVALID_INTEGER_ERROR = "Введите целое число."
INVALID_URL_ERROR = "Введите корректный URL."
INVALID_CHOICE_ERROR = "Выберите корректный вариант."
MAX_LENGTH_ERROR = "Слишком длинное значение (максимум %(limit_value)s символов)."
MIN_LENGTH_ERROR = "Слишком короткое значение (минимум %(limit_value)s символов)."
MIN_VALUE_ERROR = "Значение не может быть меньше %(limit_value)s."
MAX_VALUE_ERROR = "Значение не может быть больше %(limit_value)s."


class RussianValidationMixin:
    def _set_russian_error_messages(self):
        for field in self.fields.values():
            if field.required:
                field.error_messages["required"] = REQUIRED_FIELD_ERROR

            if "invalid" in field.error_messages:
                field.error_messages["invalid"] = self._invalid_message_for_field(field)

            if "invalid_choice" in field.error_messages:
                field.error_messages["invalid_choice"] = INVALID_CHOICE_ERROR

            if "max_length" in field.error_messages:
                field.error_messages["max_length"] = MAX_LENGTH_ERROR

            if "min_length" in field.error_messages:
                field.error_messages["min_length"] = MIN_LENGTH_ERROR

            if "min_value" in field.error_messages:
                field.error_messages["min_value"] = MIN_VALUE_ERROR

            if "max_value" in field.error_messages:
                field.error_messages["max_value"] = MAX_VALUE_ERROR

    @staticmethod
    def _invalid_message_for_field(field):
        if isinstance(field, forms.EmailField):
            return INVALID_EMAIL_ERROR
        if isinstance(field, forms.DateField):
            return INVALID_DATE_ERROR
        if isinstance(field, forms.IntegerField):
            return INVALID_INTEGER_ERROR
        if isinstance(field, forms.URLField):
            return INVALID_URL_ERROR
        return GENERIC_INVALID_ERROR


class TeacherForm(RussianValidationMixin, forms.ModelForm):
    class Meta:
        model = Teacher
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "employee_code",
            "phone",
            "hire_date",
            "is_active",
        )
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "middle_name": "Отчество",
            "email": "Электронная почта",
            "employee_code": "Табельный номер",
            "phone": "Телефон",
            "hire_date": "Дата приема на работу",
            "is_active": "Активен",
        }
        error_messages = {
            "email": {
                "unique": "Преподаватель с такой электронной почтой уже существует.",
            },
            "employee_code": {
                "unique": "Преподаватель с таким табельным номером уже существует.",
            },
            "phone": {
                "unique": "Преподаватель с таким телефоном уже существует.",
            },
        }
        widgets = {
            "hire_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_russian_error_messages()


class TeacherInfoForm(RussianValidationMixin, forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = (
            "biography",
            "degree",
            "office",
            "years_of_experience",
            "website",
        )
        labels = {
            "biography": "Биография",
            "degree": "Ученая степень",
            "office": "Кабинет",
            "years_of_experience": "Стаж (лет)",
            "website": "Сайт",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_russian_error_messages()


class CourseForm(RussianValidationMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            "title",
            "code",
            "description",
            "credits",
            "duration_weeks",
            "starts_at",
            "teacher",
        )
        labels = {
            "title": "Название",
            "code": "Код курса",
            "description": "Описание",
            "credits": "Кредиты",
            "duration_weeks": "Длительность (недели)",
            "starts_at": "Дата начала",
            "teacher": "Преподаватель",
        }
        error_messages = {
            "title": {
                "unique": "Курс с таким названием уже существует.",
            },
            "code": {
                "unique": "Курс с таким кодом уже существует.",
            },
        }
        widgets = {
            "starts_at": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_russian_error_messages()


class StudentForm(RussianValidationMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            "first_name",
            "last_name",
            "email",
            "student_number",
            "birth_date",
            "enrollment_year",
            "is_active",
        )
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Электронная почта",
            "student_number": "Номер студента",
            "birth_date": "Дата рождения",
            "enrollment_year": "Год поступления",
            "is_active": "Активен",
        }
        error_messages = {
            "email": {
                "unique": "Студент с такой электронной почтой уже существует.",
            },
            "student_number": {
                "unique": "Студент с таким номером уже существует.",
            },
        }
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_russian_error_messages()


class StudentEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        label="Курс",
        error_messages={
            "required": "Выберите курс.",
            "invalid_choice": "Выбран некорректный курс.",
        },
    )
