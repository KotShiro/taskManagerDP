from django.db import models
from django.contrib.auth.models import AbstractUser, User
from datetime import date

#CastomUser
class User(AbstractUser):
    fathername = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)