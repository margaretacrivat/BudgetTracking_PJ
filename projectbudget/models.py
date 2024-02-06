# from django.db import models
# from django.contrib.auth.models import User
# from django.utils.timezone import now
#
# # Create your models here.
#
#
# #---->>>>>>>>>> PROJECTS <<<<<<<<<<<<----#
#
# class Projects(models.Model):
#     owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     project_name = models.CharField(max_length=200)
#     acronym = models.CharField(max_length=20)
#     funder = models.TextField()
#     contract = models.TextField()
#     type = models.CharField(max_length=100)
#     project_manager = models.CharField(max_length=100)
#     budget = models.FloatField(default=0)
#     start_date = models.DateField(default=now)
#     end_date = models.DateField(default=now)
#
#     @property
#     def acronym_upper(self):
#         return self.acronym.upper()
#
#     def save(self, *args, **kwargs):
#         self.acronym = self.acronym.upper()
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.acronym_upper
#
#     def get_type_str(self):
#         return f"Type: {self.type}"
#
#     class Meta:
#         ordering = ['date']
#
#
# class Type(models.Model):
#     name = models.CharField(max_length=300)
#
#     # class Meta:
#     #     verbose_name_plural = 'Types'
#
#     def __str__(self):
#         return self.name
#
