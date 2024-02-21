from django import forms
from django.forms import ModelForm
from .models import Project, ProjectStage, Logistic, Displacement, Workforce, Person
from django.core.exceptions import ValidationError


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


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ('owner',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Email field is required')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not Person.validate_phone_number(phone):
                raise ValidationError('Invalid phone number. Please enter a valid phone number with country code.')
        return phone
