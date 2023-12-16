from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from .models import Items

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


