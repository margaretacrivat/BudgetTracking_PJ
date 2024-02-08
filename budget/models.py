from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PersonalDescription(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1000, null=True)


class ProjectDescription(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1000, null=True)



