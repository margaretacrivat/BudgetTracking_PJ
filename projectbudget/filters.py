import django_filters
from django_filters import CharFilter
from .models import Project, Logistic
from django.utils.text import slugify


class ProjectFilter(django_filters.FilterSet):
    project_name = CharFilter(field_name='project_name', lookup_expr='icontains')
    project_type = CharFilter(field_name='project_type', lookup_expr='icontains')
    project_stage = CharFilter(field_name='project_stage', lookup_expr='icontains')

    @staticmethod
    def slugify(value):
        return slugify(value)

    class Meta:
        model = Project
        fields = ['project_name', 'project_type', 'project_stage']


class CentralizerFilter(django_filters.FilterSet):
    project_name = CharFilter(field_name='project_name', lookup_expr='icontains')
    project_stage = CharFilter(field_name='project_stage', lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['project_name', 'project_stage']

