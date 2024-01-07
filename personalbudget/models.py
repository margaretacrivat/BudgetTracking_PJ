from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

# Models for personal_budget budget analysis
# Expenses


class Expense(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    item = models.CharField(max_length=1000)
    category = models.CharField(max_length=500)
    description = models.TextField()
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


class Currency(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return str(self.user)+'s' + 'preferences'


# Incomes


class Income(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    source = models.CharField(max_length=500)
    description = models.TextField()
    date = models.DateField(default=now)

    def __str__(self):
        return self.source

    class Meta:
        ordering: ['-date']


class Source(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
