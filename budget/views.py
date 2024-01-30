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

    if not request.user.is_authenticated and request.path == reverse('personalbudget/index.html'):
        messages.warning(request, 'You need to register to access this page.')
        return redirect('login')

    if request.user.is_authenticated:
        html_template = get_template('homepage.html')

    return HttpResponse(html_template.render(context, request))

