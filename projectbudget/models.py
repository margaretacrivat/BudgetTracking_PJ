from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


#---->>>>>>>>>> PROJECTS <<<<<<<<<<<<----#

class Project(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    project = models.CharField(max_length=20, primary_key=True)
    project_stages = models.IntegerField(default=0)
    project_manager = models.CharField(max_length=100)
    funder = models.TextField()
    contract = models.TextField()
    project_scope = models.CharField(max_length=100)
    budget = models.FloatField(default=0)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    @property
    def project_upper(self):
        return self.project.upper()

    def save(self, *args, **kwargs):
        self.acronym = self.project.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.project_upper

    def get_type_str(self):
        return f"Type: {self.project_scope}"

    class Meta:
        ordering = ['start_date']


class ProjectScope(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ---->>>>>>>>>> ETAPE PROIECT <<<<<<<<<<<<----#


class ProjectStages(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='stages', on_delete=models.CASCADE)
    project_stage = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    budget = models.FloatField(default=0)
    reimbursed_amount = models.FloatField(default=0)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    def __str__(self):
        return self.project_stage

    class Meta:
        ordering = ['start_date']


class Logistic(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='logistics', on_delete=models.CASCADE)
    project_stage = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    expense_type = models.CharField(max_length=100)
    document_type = models.CharField(max_length=100)
    document_series = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100)
    description_acquisition = models.TextField()
    amount = models.FloatField(default=0)
    date = models.DateField(default=now)

    def __str__(self):
        return self.expense_type

    class Meta:
        ordering = ['date']


class ExpensesType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Displacement(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='displacements', on_delete=models.CASCADE)
    project_stage = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True)
    document_series = models.CharField(max_length=100)
    displaced_to = models.TextField()
    amount = models.FloatField(default=0)
    days_no = models.IntegerField(default=0)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    def __str__(self):
        return self.document_series

    class Meta:
        ordering = ['start_date']


class Workforce(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='workforces', on_delete=models.CASCADE)
    project_stage = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True)
    days_no = models.IntegerField(default=0)
    salary_per_hour = models.FloatField(default=0)
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.person


class Person(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    age = models.IntegerField(null=False)
    project = models.ManyToManyField(Project, related_name='persons')
    person_role = models.CharField(max_length=100)
    department = models.CharField(max_length=20, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class PersonRole(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
