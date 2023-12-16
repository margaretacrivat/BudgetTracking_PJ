from django import forms
from django.forms import TextInput, NumberInput, EmailInput, Textarea, Select, \
    DateInput
from .models import Signup
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['first_name', 'last_name', 'age', 'email',
                  'description', 'gender', 'start_date', 'end_date']

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Please enter first name'}),
            'last_name': TextInput(attrs={'class': 'form-control',
                                          'placeholder': 'Please enter last name'}),
            'age': NumberInput(attrs={'class': 'form-control',
                                      'placeholder': 'Please enter age'}),
            'email': EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Please enter email'}),
            'description': Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Please enter description',
                                           'rows': 3}),
            'gender': Select(attrs={'class': 'form-select'}),
            'start_date': DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        check_emails = Signup.objects.filter(email=cleaned_data.get('email'))

        if check_emails:
            msg = 'This email address is already registered'
            self._errors['email'] = self.error_class([msg])

        # validare start_date. Daca start_date > end_date => eroare
        if cleaned_data.get('start_date') > cleaned_data.get('end_date'):
            msg = 'The date of start/end is not correct'
            self._errors['start_date'] = self.error_class([msg])

        # unicitate pe first_name si last_name
        check_first_name_and_last_name = Signup.objects.filter(
            first_name=cleaned_data.get('first_name'),
            last_name=cleaned_data.get('last_name'))

        if check_first_name_and_last_name:
            msg = 'The person with this name has been already registered'
            self._errors['first_name'] = self.error_class([msg])
        return cleaned_data
