from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm


# Create your views here.

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
    return render(request, "user/signup.html",
                  {"user_form": user_form})


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
                return render(request, 'user/login.html', context)
    else:
        login_form = LoginForm()
    return render(request, 'user/login.html',
                  {'login_form': login_form, "login_msg": login_msg})


def user_logout(request):
    logout(request)
    return redirect('home')


def user_settings(request):
    return render(request, 'user/settings.html')



# def request_reset_password(request):
#     if request.method == 'GET':
#         return render(request, 'user/reset_password.html')
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
#             return render(request, 'user/reset_password.html', context)
#
#     current_site = get_current_site(request)
#
#     user = request.objects.filter(email=email)
#
#     if user.exists():
#         pass
#
#     messages.success(request, 'We have sent you an email to reset your password')

