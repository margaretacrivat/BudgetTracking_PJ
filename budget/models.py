# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models

from BudgetTracking_PJ import settings


# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1000, null=True)


# class UserData(AbstractUser):
#     # gender_options = (('male', 'Male'), ('female', 'Female'))
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     username = models.CharField(max_length=100, null=False, unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100, blank=True, unique=True)
#     description = models.TextField(max_length=500)
#     birth_date = models.DateField(null=True)
#     # gender = models.CharField(choices=gender_options, max_length=20)
#     profile_photo = models.ImageField(upload_to='media', null=True)
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

