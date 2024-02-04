from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PasswordHistory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)