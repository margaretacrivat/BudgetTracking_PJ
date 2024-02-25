from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .models import PersonalDescription, ProjectDescription

# Create your views here.

# ---->>>>>>>>>> HOMEPAGE VIEWS <<<<<<<<<<<<----#

def home(request):
    html_template = get_template('index.html')
    personal_description = PersonalDescription.objects.all()
    project_description = ProjectDescription.objects.all()
    context = {
        'personal_description': personal_description,
        'project_description': project_description,
    }

    if request.user.is_authenticated:
        html_template = get_template('homepage.html')

    return HttpResponse(html_template.render(context, request))


def access_page_view(request):
    return render(request, 'access_page.html')
