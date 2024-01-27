from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template import loader
from django.template.loader import get_template

from .models import Items


# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile

from django.db.models import Sum

# Create your views here.


def home(request):
    # Logica pentru vizualizarea paginii principale
    html_template = get_template('index.html')
    items = Items.objects.all()
    context = {'items': items}
    if request.user.is_authenticated:
        html_template = get_template('homepage.html')
    return HttpResponse(html_template.render(context, request))


class HomePageView(TemplateView):
    template_name = "homepage.html"

