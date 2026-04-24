from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\+?[0-9]{10,15}$",
                message="Введите корректный номер телефона.",
            )
        ],
    )
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.username
