from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
import json

from reportlab.lib.units import inch

from .forms import ProjectForm
from .models import (Project, ProjectType, ProjectStage, Person,
                     Logistic, ExpensesType, Displacement,
                     DisplacementType, Workforce, PersonRole)
from preferences.models import Currency
from django.core.paginator import Paginator
import datetime
import csv
import xlwt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet



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
    today = datetime.date.today()

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


@login_required(login_url='/authentication/login')
def edit_project(request, id):
    print("Received project ID:", id)
    project = Project.objects.get(pk=id)
    project_type = ProjectType.objects.values_list('name', flat=True).distinct()

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            form.save()
            messages.success(request, 'Project updated successfully')
            return redirect('projects')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'project': project,
        'project_type': project_type,
        'start_date': project.start_date,
        'end_date': project.end_date
    }

    return render(request, 'projectbudget/projects/edit_project.html', context)


@login_required(login_url='/authentication/login')
def delete_project(request, id):
    project = Project.objects.get(pk=id)
    project.delete()
    messages.success(request, 'Project deleted')
    return redirect('projects')


def search_project(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        project = Project.objects.filter(
            institution__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
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

        data = project.values()
        return JsonResponse(list(data), safe=False)


# ---->>>>>>>>>> PROJECTS - EXPORT FILES VIEWS <<<<<<<<<<<<----#

def export_projects_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Projects' + \
                                      str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    writer.writerow(['Institution', 'Project Title', 'Project', 'Project Stages', 'Project Manager',
                     'Funder', 'Contract', 'Project Type', f'Budget ({currency})', 'Start Date', 'End Date'])

    projects = Project.objects.filter(owner=request.user)

    for project in projects:
        writer.writerow([project.institution, project.project_title, project.project, project.project_stages,
                         project.project_manager, project.funder, project.contract, project.project_type,
                         project.budget, project.start_date, project.end_date])
    return response


def export_projects_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Projects' + \
                                      str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Projects')
    row_num = 0
    font_style_bold = xlwt.XFStyle()
    font_style_bold.font.bold = True

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    columns = ['Institution', 'Project Title', 'Project', 'Project Stages', 'Project Manager', 'Funder',
               'Contract', 'Project Type', f'Budget ({currency})', 'Start Date', 'End Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style_bold)

    rows = Project.objects.filter(owner=request.user).values_list(
        'institution', 'project_title', 'project', 'project_stages', 'project_manager', 'funder',
        'contract', 'project_type', 'budget', 'start_date', 'end_date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]))

    wb.save(response)

    return response


def export_projects_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Projects' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = SimpleDocTemplate(response,  pagesize=landscape(A4), title='PDF Projects_Report', topMargin=0.5*inch)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = 1
    title_style.fontSize = 18

    elements = []

    # Add a title
    title_text = 'Projects Report'
    elements.append(Paragraph(title_text, title_style))

    # Add spacer to create space between title and table header
    elements.append(Spacer(1, 24))

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    headers = ['Institution', 'Project\nTitle', 'Project', 'Project\nStages', 'Project\nManager', 'Funder',
               'Contract', 'Project\nType', f'Budget\n({currency})', 'Start Date', 'End Date']
    data = [headers]

    projects = Project.objects.filter(owner=request.user)

    for project in projects:
        data.append([
            project.institution, project.project_title, project.project, project.project_stages,
            project.project_manager, project.funder, project.contract, project.project_type,
            project.budget, project.start_date, project.end_date
        ])

    # Define style for table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('RIGHTPADDING', (0, 0), (-1, 0), 5),
        ('LEFTPADDING', (0, 0), (-1, 0), 5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ])

    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    pdf.build(elements)

    return response
