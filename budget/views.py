from django.contrib.auth.models import auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse
from django.template import loader
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import Items, Signup
from .forms import LoginForm, SignupForm
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.

def home(request):
    html_template = loader.get_template('index.html')
    items = Items.objects.all()
    context = {'items': items}
    # if request.user.is_authenticated:
    #     html_template = loader.get_template('index.html')
    #     context = {'items': items}
    return HttpResponse(html_template.render(context, request))


# class HomePageView(TemplateView):
#     template_name = "index.html"


class SignupView(SuccessMessageMixin, CreateView):
    template_name = 'user/signup.html'
    model = Signup
    form_class = SignupForm
    success_message = 'The person {first_name} {last_name} was successfully added'
    success_url = reverse_lazy("login")

    def get_success_message(self, cleaned_data):
        return self.success_message.format(first_name=self.object.first_name,
                                           last_name=self.object.last_name)


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
                    return redirect('homepage')
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
    return redirect('homepage')
