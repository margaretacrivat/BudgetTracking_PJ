from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Please enter a username',
                   'class': 'form-control',
                   'autocomplete': 'username',
                   }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Please enter first name',
                   'class': 'form-control',
                   'autocomplete': 'given-name',
                   }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Please enter last name',
                   'class': 'form-control',
                   'autocomplete': 'family-name',
                   }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Please enter email',
                   'class': 'form-control',
                   'autocomplete': 'email',
                   }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'class': 'form-control',
                   'autocomplete': 'current-password',
                   }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Repeat Password',
                   'class': 'form-control',
                   'autocomplete': 'new-password',
                   }
        ))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


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

