from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse
from django.template import loader
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Items, Signup
from .forms import SignupForm

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
    form_class = SignupForm
    success_message = 'The person {first_name} {last_name} was successfully added'
    success_url = reverse_lazy('index.html')

    def get_success_message(self, cleaned_data):
        return self.success_message.format(f_name=self.object.first_name, l_name=self.object.last_name)


