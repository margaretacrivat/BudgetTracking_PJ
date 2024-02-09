from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.


# ---->>>>>>>>>> EXPENSES <<<<<<<<<<<<----#

class Expense(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    item = models.CharField(max_length=1000)
    category = models.CharField(max_length=500)
    description = models.TextField()
    cost = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    date = models.DateField(default=now)

    def save(self, *args, **kwargs):
        # Convert cost and qty to floats or integers if they are provided as strings
        if isinstance(self.cost, str):
            try:
                self.cost = float(self.cost)
            except ValueError:
                self.cost = 0.0
        if isinstance(self.qty, str):
            try:
                self.qty = int(self.qty)
            except ValueError:
                self.qty = 0

        # Check if cost and qty are valid numeric values before performing multiplication
        if isinstance(self.cost, (float, int)) and isinstance(self.qty, int):
            self.amount = self.cost * self.qty
        else:
            self.amount = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['date']


class Category(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# ---->>>>>>>>>> INCOME <<<<<<<<<<<<----#

class Income(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=500)
    description = models.TextField()
    amount = models.FloatField(default=0)
    date = models.DateField(default=now)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['date']


class Source(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
