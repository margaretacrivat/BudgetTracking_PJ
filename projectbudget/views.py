from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
import json
from reportlab.lib.units import inch
from .forms import ProjectForm, ProjectStageForm
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


# ---->>>>>>>>>> PROJECTS - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def projects_view(request):
    projects = Project.objects.filter(owner=request.user).values()
    today = datetime.date.today()

    paginator = Paginator(projects, 7)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'projects': projects,
        'today': today,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'projectbudget/project/user_projects.html', context)


@login_required(login_url='/authentication/login')
def add_project(request):
    project_type = ProjectType.objects.values_list('name', flat=True).distinct()

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

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
        form = ProjectForm()

    context = {
        'project_type': project_type,
        'form': form,
        'currency': currency
    }

    return render(request, 'projectbudget/project/add_project.html', context)


@login_required(login_url='/authentication/login')
def edit_project(request, id):
    project = Project.objects.get(pk=id)
    project_type = ProjectType.objects.values_list('name', flat=True).distinct()

    # formatted_date = project.date.strftime('%Y-%m-%d')

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

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
        'end_date': project.end_date,
        'currency': currency
    }

    return render(request, 'projectbudget/project/edit_project.html', context)


@login_required(login_url='/authentication/login')
def delete_project(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        project = Project.objects.get(pk=id)
        project.delete()
        return JsonResponse({'message': 'Project deleted'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def search_project(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        project = Project.objects.filter(
            institution__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            project_name__icontains=search_str,
            owner=request.user) | Project.objects.filter(
            project_title__icontains=search_str,
            owner=request.user) | Project.objects.filter(
            project_stages__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            project_manager__icontains=search_str,
            owner=request.user) | Project.objects.filter(
            funder__icontains=search_str,
            owner=request.user) | Project.objects.filter(
            contract__istartswith=search_str,
            owner=request.user) | Project.objects.filter(
            project_type__icontains=search_str,
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
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    writer.writerow(['Institution', 'Project Name', 'Project Title', 'Project Stages', 'Project Manager',
                     'Funder', 'Contract', 'Project Type', f'Budget ({currency})', 'Start Date', 'End Date'])

    projects = Project.objects.filter(owner=request.user)

    for project in projects:
        writer.writerow([project.institution, project.project_name, project.project_title, project.project_stages,
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

    # Alignment style for header titles
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    font_style_bold.alignment = alignment

    date_style = xlwt.XFStyle()
    date_style.num_format_str = 'MM/DD/YYYY'

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    columns = ['Institution', 'Project Name', 'Project Title', 'Project Stages', 'Project Manager', 'Funder',
               'Contract', 'Project Type', f'Budget ({currency})', 'Start Date', 'End Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style_bold)

    rows = Project.objects.filter(owner=request.user).values_list(
        'institution', 'project_name', 'project_title', 'project_stages', 'project_manager', 'funder',
        'contract', 'project_type', 'budget', 'start_date', 'end_date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 9 or col_num == 10:
                ws.write(row_num, col_num, row[col_num], date_style)
            elif col_num == 8:
                formatted_value = "{:.2f}".format(row[col_num])  # Format the value with two decimals
                amount_style = xlwt.easyxf('align: horiz right')
                ws.write(row_num, col_num, formatted_value, amount_style)
            else:
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
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    headers = ['Institution', 'Project\nName', 'Project\nTitle', 'Project\nStages', 'Project\nManager', 'Funder',
               'Contract', 'Project\nType', f'Budget\n({currency})', 'Start Date', 'End Date']
    data = [headers]

    projects = Project.objects.filter(owner=request.user)

    for project in projects:
        formatted_start_date = project.start_date.strftime('%d-%m-%Y')
        formatted_end_date = project.end_date.strftime('%d-%m-%Y')
        data.append([
            project.institution, project.project_name, project.project_title, project.project_stages,
            project.project_manager, project.funder, project.contract, project.project_type,
            project.budget, formatted_start_date, formatted_end_date
        ])

    # Define style for table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('RIGHTPADDING', (0, 0), (-1, 0), 5),
        ('LEFTPADDING', (0, 0), (-1, 0), 5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
    ])

    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    pdf.build(elements)

    return response


# ---->>>>>>>>>> PROJECT STAGES - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def project_stages_view(request):
    project_stages = ProjectStage.objects.filter(owner=request.user).select_related('project_name')
    today = datetime.date.today()

    paginator = Paginator(project_stages, 7)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'project_stages': project_stages,
        'today': today,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'projectbudget/projectstages/project_stages.html', context)


@login_required(login_url='/authentication/login')
def add_project_stage(request):
    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    if request.method == 'POST':
        form_stage = ProjectStageForm(request.POST)
        if form_stage.is_valid():
            project = form_stage.save(commit=False)
            project.owner = request.user
            form_stage.save()
            messages.success(request, 'Project Stage saved successfully')
            return redirect('project-stages')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form_stage = ProjectStageForm()
        # transmit the existing projects as options
        projects = Project.objects.all()
        form_stage.fields['project_name'].queryset = projects

    context = {
        'form_stage': form_stage,
        'currency': currency
    }

    return render(request, 'projectbudget/projectstages/add_project_stage.html', context)


@login_required(login_url='/authentication/login')
def edit_project_stage(request, id):
    project_stage = ProjectStage.objects.get(pk=id)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    if request.method == 'POST':
        form_stage = ProjectStageForm(request.POST, instance=project_stage)
        if form_stage.is_valid():
            project = form_stage.save(commit=False)
            project.owner = request.user
            form_stage.save()
            messages.success(request, 'Project Stage updated successfully')
            return redirect('project-stages')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form_stage = ProjectStageForm(instance=project_stage)

    context = {
        'project_stage': project_stage,
        'form_stage': form_stage,
        'start_date': project_stage.start_date,
        'end_date': project_stage.end_date,
        'currency': currency
    }

    return render(request, 'projectbudget/projectstages/edit_project_stage.html', context)


@login_required(login_url='/authentication/login')
def delete_project_stage(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        project_stage = ProjectStage.objects.get(pk=id)
        project_stage.delete()
        return JsonResponse({'message': 'Project Stage deleted'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


# ---->>>>>>>>>> PROJECTS - EXPORT FILES VIEWS <<<<<<<<<<<<----#

def export_project_stages_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ProjectStages' + \
                                      str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    writer.writerow(['Project Name', 'Project Stage', f'Budget ({currency})', f'Reimbursed Amount ({currency})',
                     'Start Date', 'End Date'])

    project_stages = ProjectStage.objects.filter(owner=request.user)

    for project_stage in project_stages:
        writer.writerow([project_stage.project_name.project_name, project_stage.project_stage, project_stage.budget,
                         project_stage.reimbursed_amount, project_stage.start_date, project_stage.end_date])
    return response