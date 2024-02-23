from django.contrib import admin
from .models import (Project, ProjectType, ProjectStage, Logistic, AcquisitionType, Displacement,
                     DisplacementType, Workforce, Person)

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('owner', 'institution', 'project_name', 'project_title', 'project_stages', 'project_manager',
                    'funder', 'contract', 'project_type', 'budget', 'start_date', 'end_date')
    search_fields = ('institution', 'project_name', 'project_title', 'project_stages', 'budget', 'start_date', 'end_date')
    list_per_page = 7


class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'project_name', 'project_stage', 'budget', 'start_date', 'end_date')
    search_fields = ('project_name', 'project_stage', 'budget', 'start_date', 'end_date')
    list_per_page = 7


class LogisticAdmin(admin.ModelAdmin):
    list_display = ('owner', 'project_name', 'project_stage', 'acquisition_name', 'acquisition_type',
                    'document_type', 'document_series', 'supplier_name', 'acquisition_description',
                    'acquisition_owner', 'work_place', 'cpv_code', 'amount', 'date')
    search_fields = ('project_name', 'project_stage', 'acquisition_name', 'acquisition_type',
                     'cpv_code', 'amount', 'date')
    list_per_page = 7


class DisplacementAdmin(admin.ModelAdmin):
    list_display = ('owner', 'project_name', 'project_stage', 'work_place', 'person_name', 'document_series',
                    'displaced_to', 'displacement_type', 'transportation_mean', 'budget_per_day', 'days_no',
                    'total_budget', 'other_expenses_description', 'other_expenses_budget', 'total_amount', 'start_date',
                    'end_date')
    search_fields = ('project_name', 'project_stage', 'work_place', 'person_name', 'document_series',
                     'displacement_type', 'total_amount', 'start_date', 'end_date')
    list_per_page = 7


class WorkforceAdmin(admin.ModelAdmin):
    list_display = ('owner', 'project_name', 'project_stage', 'work_place', 'person_work_id', 'person_name',
                    'person_role', 'salary_per_hour', 'work_days', 'salary_realized', 'vacation_leave_days_no',
                    'vacation_reimbursed_amount', 'gross_salary_amount', 'start_date', 'end_date')
    search_fields = ('project_name', 'project_stage', 'work_place', 'person_name', 'document_series',
                     'gross_salary_amount', 'start_date', 'end_date')
    list_per_page = 7


class PersonAdmin(admin.ModelAdmin):
    list_display = ('owner', 'person_name', 'person_id', 'age', 'is_internal', 'institution',
                    'department', 'email', 'phone', 'city', 'country')
    search_fields = ('person_name', 'person_id', 'age', 'institution', 'department')
    list_per_page = 7


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectType)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(Logistic, LogisticAdmin)
admin.site.register(AcquisitionType)
admin.site.register(Displacement, DisplacementAdmin)
admin.site.register(DisplacementType)
admin.site.register(Workforce, WorkforceAdmin)
admin.site.register(Person, PersonAdmin)