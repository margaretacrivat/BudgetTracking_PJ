from django import forms
from django.forms import TextInput, NumberInput, EmailInput, Textarea, Select, \
    DateInput
from django.contrib.auth.models import User
from .models import Signup
from django.contrib.auth.models import User


class SignupModelForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['username', 'first_name', 'last_name', 'email',
                  'description', 'gender', 'start_date', 'password1', 'password2']

        widgets = {
            'username': TextInput(attrs={'class': 'form-control',
                                         'placeholder': 'Please enter a username'}),
            'first_name': TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Please enter first name'}),
            'last_name': TextInput(attrs={'class': 'form-control',
                                          'placeholder': 'Please enter last name'}),
            'email': EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Please enter email'}),
            'description': Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Please enter description',
                                           'rows': 3}),
            'gender': Select(attrs={'class': 'form-select'}),
            'start_date': DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
            'password1': DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Password check'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        # unicitate pe email address
        check_emails = Signup.objects.filter(email=cleaned_data.get('email'))

        if check_emails:
            msg = 'This email address is already registered'
            self._errors['email'] = self.error_class([msg])

        # unicitate pe first_name si last_name
        check_first_name_and_last_name = Signup.objects.filter(
            first_name=cleaned_data.get('first_name'),
            last_name=cleaned_data.get('last_name'))

        if check_first_name_and_last_name:
            msg = 'The person with this name has been already registered'
            self._errors['first_name'] = self.error_class([msg])

        # unicitate pe username
        check_username = Signup.objects.filter(
            username=cleaned_data.get('username'))

        if check_username:
            msg = 'This username has been already registered'
            self._errors['username'] = self.error_class([msg])
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'placeholder': 'Enter Username',
                'class': 'form-control'
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password',
                'class': 'form-control'
            }
        ))

