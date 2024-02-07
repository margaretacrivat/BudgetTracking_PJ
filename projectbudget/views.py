import json
from datetime import date

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProjectForm
from .models import (Project, ProjectType, ProjectStage, Person,
                     Logistic, ExpensesType, Displacement,
                     DisplacementType, Workforce, PersonRole)
from preferences.models import Currency
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


# ---->>>>>>>>>> PROJECT BUDGET - PAGE VIEW <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def project_budget_view(request):
    return render(request, 'projectbudget/index.html')


# ---->>>>>>>>>> EXPENSES - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def projects_view(request):
    # The Logic for expenses visualization
    projects = Project.objects.filter(owner=request.user).values()
    today = date.today()

    paginator = Paginator(projects, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'projects': projects,
        'today': today,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'projectbudget/projects/user_projects.html', context)


@login_required(login_url='/authentication/login')
def add_project(request):
    project_type = ProjectType.objects.values_list('name', flat=True).distinct()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            form.save()
            messages.success(request, 'Project saved successfully')
            return redirect('projects')
        else:
            messages.error(request, 'Invalid form data')
    else:
        # Initialize the form with initial data for the budget field
        form = ProjectForm(initial={'budget': '0.0'})

    context = {
        'project_type': project_type,
        'form': form
    }

    return render(request, 'projectbudget/projects/add_project.html', context)


def search_project(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Project.objects.filter(
            project_title__icontains=search_str,
            owner=request.user) | Project.objects.filter(
            project__icontains=search_str,
            owner=request.user) | Project.objects.filter(
            project_stages__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            project_manager__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            funder__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            contract__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            project_type__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            budget__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            start_date__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            end_date__istartswith=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)