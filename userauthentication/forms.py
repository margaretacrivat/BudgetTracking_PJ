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
                   'class': 'form-control',
                   }
        ))
    password1 = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Password',
                   'class': 'form-control',
                   }
        ))
    password2 = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Repeat Password',
                   'class': 'form-control',
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
