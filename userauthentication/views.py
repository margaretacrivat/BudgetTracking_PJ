from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from .forms import LoginForm, SignUpForm
from .models import PasswordHistory
import json
from django.http import JsonResponse
from django.views import View
from validate_email import validate_email
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
from django.core.mail import send_mail, get_connection


# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']

            # async validation - validate username
            if not str(username).isalnum():
                return JsonResponse({'username_error': 'username should only contain alphanumeric characters'},
                                    status=400)
            # check if the user already exist
            if User.objects.filter(username=username).exists():
                return JsonResponse({'username_error': 'username in use, please choose another one'}, status=409)

            return JsonResponse({'username_valid': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class EmailValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']

            # async validation - validate email
            if not validate_email(email):
                return JsonResponse({'email_error': 'email is invalid'}, status=400)
            # check if the email is taken
            if User.objects.filter(email=email).exists():
                return JsonResponse({'email_error': 'email in use, please choose another one'}, status=409)

            return JsonResponse({'email_valid': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class PasswordValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            password = data['password']

            # Django's built-in password validators
            try:
                password_validation.validate_password(password)
            except password_validation.ValidationError as e:
                return JsonResponse({'password_error': str(e)}, status=400)

            return JsonResponse({'password_valid': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def user_signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        # print("Is form valid?", user_form.is_valid())  # line for debugging
        # print("Form errors:", user_form.errors)  # line for debugging
        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'Account successfully created! Please Login')
            return redirect('login')
        else:
            messages.error(request, 'Form is not valid')
            # print("Form is not valid. Errors:", user_form.errors)  # line for debugging
    else:
        user_form = SignUpForm()
    return render(request, 'userauthentication/signup.html',
                  {'user_form': user_form})


def user_login(request):
    login_msg = ''

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
            else:
                messages.error(request, 'Invalid credentials, please try again')
                condition = 'invalid credentials'
                context = {'condition': condition,
                           'field_values': request.POST
                           }
                return render(request, 'userauthentication/login.html', context)
    else:
        login_form = LoginForm()
    return render(request, 'userauthentication/login.html',
                  {'login_form': login_form, 'login_msg': login_msg})


def user_logout(request):
    logout(request)
    return redirect('home')


# ---->>>>>>>>>> ACCOUNT SETTINGS - CHANGE CURRENT PASSWORD VIEW <<<<<<<<<<<<----#
class CurrentPasswordValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            current_password = data['current_password']

            # Get the user's actual password
            user = request.user

            # Authenticate the user with the entered current password
            auth_user = authenticate(username=user.username, password=current_password)

            # Check if authentication is successful
            if not auth_user:
                return JsonResponse({'password_error': 'Current password does not match'}, status=400)

            # Redirect to the login page
            return JsonResponse({'password_valid': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class SetNewPasswordValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            new_password = data['new_password1']

            # Django's built-in password validators
            try:
                password_validation.validate_password(new_password)
            except password_validation.ValidationError as e:
                return JsonResponse({'password_error': str(e)}, status=400)

            # Get the user's actual password
            user = request.user

            # Update the user's password
            user.set_password(new_password)
            user.save()

            # If the current password is valid, log out the user
            logout(request)

            messages.success(request, 'Your password was successfully changed! Please login')
            return JsonResponse({'password_valid': True, 'redirect': '/userauthentication/login/'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'userauthentication/account_settings.html'
    success_url = reverse_lazy('login')


# render the page where the user can supply the email
class ForgotRequestResetPassword(View):
    def get(self, request):
        return render(request, 'userauthentication/forgot_reset_password.html')


# class CompletePasswordChange(View):
#     def get(self, request):
#         return render(request, 'userauthentication/set_new_password.html')

