from datatable import dt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import auth
from django.contrib import messages
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .models import Items, Purchase
from .forms import LoginForm, SignUpForm

# Create your views here.

def home(request):
    # Logica pentru vizualizarea paginii principale
    html_template = loader.get_template('index.html')
    items = Items.objects.all()
    context = {'items': items}
    if request.user.is_authenticated:
        html_template = loader.get_template('homepage.html')
    return HttpResponse(html_template.render(context, request))


class HomePageView(TemplateView):
    template_name = "homepage.html"


def user_signup(request):
    msg = None
    success = False

    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            # username = user_form.cleaned_data.get("username")
            # raw_password = user_form.cleaned_data.get("password1")
            # user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="login">Login</a>.'
            success = True

            return redirect('login')

        else:
            msg = 'Form is not valid'
    else:
        user_form = SignUpForm()
    return render(request, "user/signup.html",
                  {"user_form": user_form, "msg": msg, "success": success})


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
                else:
                    return redirect('login')
            else:
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


def table_purchase(request):
    # Logica pentru pagina de inserare a datelor in tabel
    # all_purchases = Purchase.objects.all()
    return render(request, 'personal_page/tb_purchase.html')


