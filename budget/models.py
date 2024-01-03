from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Items(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1000, null=True)


# Models for personal_page budget analysis

class Expense(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    item = models.CharField(max_length=1000)
    category = models.CharField(max_length=500)
    cost = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    date = models.DateField(default=now)

    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']


class Category(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# class House(models.Model):
#     person_name = models.CharField(max_length=200, null=False)
#     rent = models.IntegerField()
#     utilities = models.IntegerField()
#     insurance = models.IntegerField()
#     taxes = models.IntegerField()
#     transportation = models.IntegerField()
#     shops_expenses = models.IntegerField()
#     expenses_monthly = models.IntegerField(default=0)
#     income_monthly = models.IntegerField(default=0)
#     balance = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.person_name
#



