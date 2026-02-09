from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "STUDENT"
        LIBRARIAN = "LIBRARIAN"
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)