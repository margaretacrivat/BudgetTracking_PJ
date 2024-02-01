from audioop import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Items

# Create your views here.

# ---->>>>>>>>>> HOMEPAGE VIEWS <<<<<<<<<<<<----#
# Logica pentru vizualizarea paginii principale #


def home(request):
    html_template = get_template('index.html')
    items = Items.objects.all()
    context = {'items': items}

    if request.user.is_authenticated:
        html_template = get_template('homepage.html')

    return HttpResponse(html_template.render(context, request))

