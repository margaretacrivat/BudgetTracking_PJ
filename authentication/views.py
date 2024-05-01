from audioop import reverse

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from .forms import LoginForm, SignUpForm
import json
from django.http import JsonResponse
from django.views import View
from validate_email import validate_email
from numpy import generic
from django.views.generic import DeleteView


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
        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'Account successfully created! Please Login')
            return redirect('login')
        else:
            messages.error(request, 'Form is not valid')
    else:
        user_form = SignUpForm()
    return render(request, 'authentication/signup.html',
                  {'user_form': user_form})

            # token_generator = PasswordResetTokenGenerator()
            # confirmation_url = reverse('activate', kwargs={'uidb64': urlsafe_base64.urlsafe_b64encode(user.pk).decode(),
            #                                                'token': token_generator.make_token(user)})
            #
            # send_mail(
            #     subject='Account Confirmation - Your Awesome Site',
            #     message=get_template('registration/account_confirmation_email.html').render(
            #         context={'user': user, 'confirmation_url': confirmation_url,
            #                  'your_site_name': 'Your Awesome Site'}),
            #     from_email='your_server_email_address',
            #     recipient_list=[user.email],
            # )

            # user = user_form.save(commit=False)  # Don't commit yet
            # user.is_active = False  # Set user inactive until confirmed
            # user.save()

            # Generate confirmation token
            # token_generator = PasswordResetTokenGenerator()
            # confirmation_url = reverse('activate',
            #                            kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            #                                    'token': token_generator.make_token(user)})

            # Prepare email content
            # subject = 'Account Confirmation - Your Awesome Site'
            # message = get_template('authentication/account_confirmation_email.html').render(
            #     context={'user': user, 'confirmation_url': confirmation_url,
            #              'your_site_name': 'Your Awesome Site'})

            # Send confirmation email
            # send_mail(
            #     subject=subject,
            #     message=message,
            #     from_email='your_server_email_address',
            #     recipient_list=[user.email],
            # )


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#
#     if user is not None and PasswordResetTokenGenerator().check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Your account has been confirmed!')
#         return redirect('login')
#     else:
#         messages.error(request, 'Activation link is invalid or expired!')
#         return redirect('login')


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
                context = {
                    'field_values': request.POST
                }
                return render(request, 'authentication/login.html', context)
        else:
            messages.error(request, 'Please enter your username and password.')
            context = {
                'field_values': request.POST
            }
            return render(request, 'authentication/login.html', context)
    else:
        login_form = LoginForm()
    return render(request, 'authentication/login.html',
                  {'login_form': login_form, 'login_msg': login_msg})


def user_logout(request):
    logout(request)
    return redirect('home')


# ---->>>>>>>>>> ACCOUNT SETTINGS - CHANGE CURRENT PASSWORD VIEW <<<<<<<<<<<<----#

def set_new_password(request):
    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Your password was successfully changed! Please login')
            # print('Redirecting to login page...')
            return redirect('login')
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, 'authentication/account_settings.html', {'fm': fm})


# render the page where the user can supply the email
class ForgotRequestResetPassword(View):
    def get(self, request):
        return render(request, 'authentication/forgot_reset_password.html')


class DeleteUserAccount(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'authentication/delete_user_confirm.html'
    success_message = 'Your account has been deleted! Please Sign Up'
    success_url = reverse_lazy('signup')





