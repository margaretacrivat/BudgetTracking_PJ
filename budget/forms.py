from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, NumberInput, EmailInput, Textarea, Select, \
    DateInput
from django.contrib.auth import authenticate
from .models import Signup


class SignupForm(UserCreationForm):
    class Meta:
        model = Signup
        fields = ['username', 'first_name', 'last_name', 'email',
                  'description', 'gender', 'birth_date', 'profile']

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
            'birth_date': DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
            'profile': forms.FileInput(
                attrs={'class': 'form-control', 'id': 'profile_image'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        check_emails = Signup.objects.filter(email=cleaned_data.get('email'))
        if check_emails:
            msg = 'Adresa de email exista in baza de date'
            self._errors['email'] = self.error_class([msg])

        #unicitate pe first_name si last_name
        check_first_name_and_last_name = Signup.objects.filter(first_name=cleaned_data.get('first_name'),
                                                                last_name= cleaned_data.get('last_name'))
        if check_first_name_and_last_name:
                msg = 'Acest nume si prenume a fost deja inregistrat'
                self._errors['first_name'] = self.error_class([msg])
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
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
