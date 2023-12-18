from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse
from django.template import loader
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .models import Items, Signup
from .forms import SignupModelForm, LoginForm


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


class SignupCreateView(SuccessMessageMixin, CreateView):
    template_name = 'user/signup.html'
    model = Signup
    form_class = SignupModelForm
    success_message = 'The person {first_name} {last_name} was successfully added'
    success_url = reverse_lazy('index.html')

    def get_success_message(self, cleaned_data):
        return self.success_message.format(f_name=self.object.first_name,
                                           l_name=self.object.last_name)


def login_view(request):
    form = LoginForm(request.POST or None)
    message = None
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                message = 'Username does not exist'
        else:
            message = "Invalid data"

    context = {'form': form, "msg": message}

    return render(request, 'user/login.html', context)

