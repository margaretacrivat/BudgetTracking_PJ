from django.db import models

# Create your models here.


class Items(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1000, null=True)


# models for personal_page budget analysis

class Purchase(models.Model):
    person_name = models.CharField(max_length=200, null=False)
    item = models.CharField(max_length=200)
    category = models.CharField(max_length=1000, null=True)
    cost = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.person_name

    # JSON
    # def get_data(self):
    #     return {
    #         'person_name': self.person_name,
    #         'item': self.item,
    #         'category': self.category,
    #         'cost': self.cost,
    #         'qty': self.qty,
    #         'amount': self.amount,
    #     }


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



