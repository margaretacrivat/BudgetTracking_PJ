from django import forms
from django.forms import ModelForm
from .models import Project, ProjectStage


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
            'project': forms.Select(attrs={'class': 'form-control'}),
        }



