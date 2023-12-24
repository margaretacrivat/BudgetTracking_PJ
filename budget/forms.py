from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.forms import TextInput, NumberInput, EmailInput, Textarea, Select, \
    DateInput
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Please enter a username',
                   'class': 'form-control'
                   }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Please enter first name',
                   'class': 'form-control'
                   }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Please enter last name',
                   'class': 'form-control'
                   }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Please enter email',
                   'class': 'form-control'
                   }
        ))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)


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
