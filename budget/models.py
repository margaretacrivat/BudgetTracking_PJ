from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from BudgetTracking_PJ import settings


# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1000, null=True)


class Signup(AbstractUser):
    gender_options = (('male', 'Male'), ('female', 'Female'))

    username = models.CharField(max_length=100, null=False, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=True, unique=True)
    description = models.TextField(max_length=500)
    gender = models.CharField(choices=gender_options, max_length=6)
    birth_date = models.DateField(null=True)
    active = models.BooleanField(default=True)
    profile = models.ImageField(upload_to='media', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

