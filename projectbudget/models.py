from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from decimal import Decimal
import phonenumbers
from django.core.exceptions import ValidationError


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
        ordering = ['-start_date']


class ProjectType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ---->>>>>>>>>> PROJECT STAGES <<<<<<<<<<<<----#

class ProjectStage(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_stage = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    def __str__(self):
        return self.project_stage

    class Meta:
        ordering = ['-start_date']


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
    work_place = models.CharField(max_length=200)
    cpv_code = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(default=now)

    def __str__(self):
        return f"Type: {self.acquisition_type}"

    class Meta:
        ordering = ['-date']


class AcquisitionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Displacement(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE)
    work_place = models.CharField(max_length=200)
    person_name = models.CharField(max_length=200)
    document_series = models.CharField(max_length=100)
    displaced_to = models.TextField()
    displacement_type = models.CharField(max_length=100, default=0)
    transportation_mean = models.CharField(max_length=100, default=0)
    budget_per_day = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    days_no = models.IntegerField(default=0)
    total_budget = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    other_expenses_description = models.CharField(max_length=200)
    other_expenses_budget = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    def __str__(self):
        return self.document_series

    class Meta:
        ordering = ['-start_date']


class DisplacementType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Workforce(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE)
    work_place = models.CharField(max_length=200)
    person_work_id = models.IntegerField(default=0)
    person_name = models.CharField(max_length=200)
    person_role = models.CharField(max_length=100)
    salary_per_hour = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    work_days = models.IntegerField(default=0)
    salary_realized = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    vacation_leave_days_no = models.IntegerField(default=0)
    vacation_reimbursed_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    gross_salary_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    def __str__(self):
        return self.person_name

    class Meta:
        ordering = ['-start_date']


class Person(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100, null=False)
    person_id = models.IntegerField(default=0)
    age = models.IntegerField(null=False)
    is_internal = models.BooleanField()
    institution = models.CharField(max_length=200)
    department = models.CharField(max_length=100, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=False)
    city = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)

    @staticmethod
    def validate_phone_number(phone):
        try:
            parsed_number = phonenumbers.parse(phone, None)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False

    def clean(self):
        super().clean()
        if self.phone and not self.validate_phone_number(self.phone):
            raise ValidationError({'phone': 'Invalid phone number'})

    def __str__(self):
        return self.person_name


class ExpensesCentralizerDetails(models.Model):
    name = models.CharField(max_length=100, null=False)
    details = models.TextField(max_length=1000, null=True)




