# Generated by Django 5.0.1 on 2024-02-15 15:58

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
            name='DisplacementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExpensesType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PersonRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
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
                ('age', models.IntegerField()),
                ('is_internal', models.BooleanField(default=True)),
                ('institution', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=50, null=True)),
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
                ('project_name', models.CharField(max_length=50)),
                ('project_title', models.CharField(max_length=200)),
                ('project_stages', models.IntegerField(default=0)),
                ('project_manager', models.CharField(max_length=100)),
                ('funder', models.CharField(max_length=200)),
                ('contract', models.CharField(max_length=200)),
                ('project_type', models.CharField(max_length=100)),
                ('budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='ProjectStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_stage', models.CharField(max_length=200)),
                ('budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('reimbursed_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.project')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Logistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_type', models.CharField(max_length=100)),
                ('document_type', models.CharField(max_length=100)),
                ('document_series', models.CharField(max_length=100)),
                ('supplier_name', models.CharField(max_length=100)),
                ('acquisition_description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('acquisition_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projectbudget.person')),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.project')),
                ('project_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projectstage')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Displacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=200)),
                ('document_series', models.CharField(max_length=100)),
                ('displaced_to', models.TextField()),
                ('displacement_type', models.CharField(default=0, max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('days_no', models.IntegerField(default=0)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('person_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projectbudget.person')),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.project')),
                ('project_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projectstage')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Workforce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_role', models.CharField(max_length=100)),
                ('days_no', models.IntegerField(default=0)),
                ('salary_per_hour', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.person')),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.project')),
                ('project_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectbudget.projectstage')),
            ],
        ),
    ]
