from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from decimal import Decimal

# Create your models here.


#---->>>>>>>>>> PROJECTS <<<<<<<<<<<<----#

class Project(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    project_name = models.CharField(max_length=100)
    project_title = models.CharField(max_length=200)
    project_stages = models.IntegerField(default=0)
    project_manager = models.CharField(max_length=200)
    funder = models.CharField(max_length=200)
    contract = models.CharField(max_length=200)
    project_type = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    def __str__(self):
        return f"Type: {self.project_type}"

    class Meta:
        ordering = ['start_date']


class ProjectType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ---->>>>>>>>>> ETAPE PROIECT <<<<<<<<<<<<----#


class ProjectStage(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_stage = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    reimbursed_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    def __str__(self):
        return self.project_stage

    class Meta:
        ordering = ['start_date']


class Person(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100, null=False)
    age = models.IntegerField(null=False)
    is_internal = models.BooleanField(default=True)
    institution = models.CharField(max_length=200)
    department = models.CharField(max_length=100, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.person_name


class Logistic(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE)
    acquisition_name = models.CharField(max_length=200)
    acquisition_type = models.CharField(max_length=100)
    document_type = models.CharField(max_length=100)
    document_series = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=200)
    acquisition_description = models.TextField()
    acquisition_owner = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(default=now)

    def __str__(self):
        return f"Type: {self.acquisition_type}"

    class Meta:
        ordering = ['date']


class AcquisitionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Displacement(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    person_name = models.CharField(max_length=200)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE)
    document_series = models.CharField(max_length=100)
    displaced_to = models.TextField()
    displacement_type = models.CharField(max_length=100, default=0)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    days_no = models.IntegerField(default=0)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    def __str__(self):
        return self.document_series

    class Meta:
        ordering = ['start_date']


class DisplacementType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Workforce(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=200)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE)
    person_role = models.CharField(max_length=100)
    days_no = models.IntegerField(default=0)
    salary_per_hour = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.person_name


class PersonRole(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



