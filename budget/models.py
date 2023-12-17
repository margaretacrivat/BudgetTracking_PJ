from django.db import models

# Create your models here.


class Items(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1000, null=True)


class Signup(models.Model):
    gender_options = (('male', 'Male'), ('female', 'Female'))

    username = models.CharField(max_length=50, null=False, blank=False, default=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    description = models.TextField(max_length=500)
    gender = models.CharField(choices=gender_options, max_length=6)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    profile = models.ImageField(upload_to='person_profile', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=20, null=False, blank=False, default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

