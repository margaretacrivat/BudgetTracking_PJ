# Generated by Django 5.0.1 on 2024-02-23 21:20

import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcquisitionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DisplacementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExpensesCentralizerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('details', models.TextField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=100)),
                ('person_id', models.IntegerField(default=0)),
                ('age', models.IntegerField()),
                ('is_internal', models.BooleanField()),
                ('institution', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=100)),
                ('project_title', models.CharField(max_length=200)),
                ('project_stages', models.IntegerField(default=0)),
                ('project_manager', models.CharField(max_length=200)),
                ('funder', models.CharField(max_length=200)),
                ('contract', models.CharField(max_length=200)),
                ('project_type', models.CharField(max_length=100)),
                ('budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='ProjectStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_stage', models.CharField(max_length=200)),
                ('budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projects')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Logistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_name', models.CharField(max_length=200)),
                ('acquisition_type', models.CharField(max_length=100)),
                ('document_type', models.CharField(max_length=100)),
                ('document_series', models.CharField(max_length=100)),
                ('supplier_name', models.CharField(max_length=200)),
                ('acquisition_description', models.TextField()),
                ('acquisition_owner', models.CharField(max_length=200)),
                ('work_place', models.CharField(max_length=200)),
                ('cpv_code', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projects')),
                ('project_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projectstage')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Displacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_place', models.CharField(max_length=200)),
                ('person_name', models.CharField(max_length=200)),
                ('document_series', models.CharField(max_length=100)),
                ('displaced_to', models.TextField()),
                ('displacement_type', models.CharField(default=0, max_length=100)),
                ('transportation_mean', models.CharField(default=0, max_length=100)),
                ('budget_per_day', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('days_no', models.IntegerField(default=0)),
                ('total_budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('other_expenses_description', models.CharField(max_length=200)),
                ('other_expenses_budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('total_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projects')),
                ('project_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projectstage')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Workforce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_place', models.CharField(max_length=200)),
                ('person_work_id', models.IntegerField(default=0)),
                ('person_name', models.CharField(max_length=200)),
                ('person_role', models.CharField(max_length=100)),
                ('salary_per_hour', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('work_days', models.IntegerField(default=0)),
                ('salary_realized', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('vacation_leave_days_no', models.IntegerField(default=0)),
                ('vacation_reimbursed_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('gross_salary_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projects')),
                ('project_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projectstage')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
    ]
