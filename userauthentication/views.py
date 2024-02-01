from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm
import json
from django.http import JsonResponse
from django.views import View
from validate_email import validate_email


# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']
            # validate username
            if not str(username).isalnum():
                return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
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
            # validate email
            if not validate_email(email):
                return JsonResponse({'email_error': 'email is invalid'}, status=400)
            # check if the email is taken
            if User.objects.filter(email=email).exists():
                return JsonResponse({'email_error': 'email in use, please choose another one'}, status=409)

            return JsonResponse({'email_valid': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def user_signup(request):

    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'User was successfully created')
            return redirect('login')

        else:
            messages.error(request, 'Form is not valid')
    else:
        user_form = SignUpForm()
    return render(request, 'userauthentication/signup.html',
                  {'user_form': user_form})


def user_login(request):
    login_msg = ""
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                # else:
                #     return redirect('login')
            else:
                messages.error(request,
                               'Invalid credentials, please try again')
                condition = 'invalid credentials'
                context = {'condition': condition}
                return render(request, 'userauthentication/login.html', context)
    else:
        login_form = LoginForm()
    return render(request, 'userauthentication/login.html',
                  {'login_form': login_form, "login_msg": login_msg})


def user_logout(request):
    logout(request)
    return redirect('home')


def user_settings(request):
    return render(request, 'userauthentication/settings.html')



# def request_reset_password(request):
#     if request.method == 'GET':
#         return render(request, 'userauthentication/reset_password.html')
#
#     if request.method == 'POST':
#         email = request.POST['email']
#
#         context = {
#             'values': request.POST
#         }
#
#         if not validate_email(email):
#             messages.error(request, 'Please supply a valid email')
#             return render(request, 'userauthentication/reset_password.html', context)
#
#     current_site = get_current_site(request)
#
#     userauthentication = request.objects.filter(email=email)
#
#     if userauthentication.exists():
#         pass
#
#     messages.success(request, 'We have sent you an email to reset your password')

