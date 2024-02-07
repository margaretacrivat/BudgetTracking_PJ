from django import forms
from django.forms import ModelForm, DateInput
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('owner',)

