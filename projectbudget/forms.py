from django import forms
from django.forms import ModelForm
from .models import Project, ProjectStage, Logistic, Displacement, Workforce


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('owner',)


class ProjectStageForm(ModelForm):
    class Meta:
        model = ProjectStage
        fields = '__all__'
        exclude = ('owner',)
        widgets = {
            'project_name': forms.Select(attrs={'class': 'form-control'}),
        }


class LogisticForm(ModelForm):
    class Meta:
        model = Logistic
        fields = '__all__'
        exclude = ('owner',)
        widgets = {
            'project_name': forms.Select(attrs={'class': 'form-control'}),
            'project_stage': forms.Select(attrs={'class': 'form-control'}),
        }


class DisplacementForm(ModelForm):
    class Meta:
        model = Displacement
        fields = '__all__'
        exclude = ('owner',)
        widgets = {
            'project_name': forms.Select(attrs={'class': 'form-control'}),
            'project_stage': forms.Select(attrs={'class': 'form-control'}),
        }


class WorkforceForm(ModelForm):
    class Meta:
        model = Workforce
        fields = '__all__'
        exclude = ('owner',)
        widgets = {
            'project_name': forms.Select(attrs={'class': 'form-control'}),
            'project_stage': forms.Select(attrs={'class': 'form-control'}),
        }



