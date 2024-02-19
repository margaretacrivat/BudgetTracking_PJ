from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
import json
from reportlab.lib.units import inch
from .forms import ProjectForm, ProjectStageForm, LogisticForm, DisplacementForm, WorkforceForm
from .models import (Project, ProjectType, ProjectStage, Person, Logistic, AcquisitionType, Displacement,
                     DisplacementType, Workforce)
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


# ---->>>>>>>>>> PROJECT STAGES - EXPORT FILES VIEWS <<<<<<<<<<<<----#

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


def export_project_stages_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ProjectStages' + \
                                      str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ProjectStages')
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

    columns = ['Project Name', 'Project Stage', f'Budget ({currency})', f'Reimbursed Amount ({currency})',
               'Start Date', 'End Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style_bold)

    rows = ProjectStage.objects.filter(owner=request.user).values_list(
        'project_name__project_name', 'project_stage', 'budget', 'reimbursed_amount', 'start_date', 'end_date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 4 or col_num == 5:
                ws.write(row_num, col_num, row[col_num], date_style)
            elif col_num == 2 or col_num == 3:
                formatted_value = "{:.2f}".format(row[col_num])
                amount_style = xlwt.easyxf('align: horiz right')
                ws.write(row_num, col_num, formatted_value, amount_style)
            else:
                ws.write(row_num, col_num, str(row[col_num]))

    wb.save(response)

    return response


def export_project_stages_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=ProjectStages' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = SimpleDocTemplate(response,  pagesize=A4, title='PDF Project_Stages_Report', topMargin=0.5*inch)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = 1
    title_style.fontSize = 18

    elements = []

    # Add a title
    title_text = 'Project Stages Report'
    elements.append(Paragraph(title_text, title_style))

    # Add spacer to create space between title and table header
    elements.append(Spacer(1, 24))

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    headers = ['Project\nName', 'Project\nStages', f'Budget\n({currency})', f'Reimbursed Amount\n({currency})',
               'Start Date', 'End Date']
    data = [headers]

    project_stages = ProjectStage.objects.filter(owner=request.user)

    for project_stage in project_stages:
        formatted_start_date = project_stage.start_date.strftime('%d-%m-%Y')
        formatted_end_date = project_stage.end_date.strftime('%d-%m-%Y')
        data.append([
            project_stage.project_name.project_name, project_stage.project_stage, project_stage.budget,
            project_stage.reimbursed_amount, formatted_start_date, formatted_end_date
        ])

    # Define style for table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
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


# ---->>>>>>>>>> LOGISTIC - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def logistic_view(request):
    acquisition = Logistic.objects.filter(owner=request.user).select_related('project_name')
    today = datetime.date.today()

    paginator = Paginator(acquisition, 7)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'acquisition': acquisition,
        'today': today,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'projectbudget/logistic/project_logistic.html', context)


@login_required(login_url='/authentication/login')
def add_acquisition(request):
    acquisition_type = AcquisitionType.objects.values_list('name', flat=True).distinct()

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    # transmit the existing projects and project stages as options
    projects = Project.objects.all()
    project_stages = ProjectStage.objects.all()

    if request.method == 'POST':
        form_acquisition = LogisticForm(request.POST)
        if form_acquisition.is_valid():
            acquisition_instance = form_acquisition.save(commit=False)
            acquisition_instance.owner = request.user
            acquisition_instance.save()
            messages.success(request, 'Acquisition saved successfully')
            return redirect('logistic')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form_acquisition = LogisticForm()

    context = {
        'acquisition_type': acquisition_type,
        'projects': projects,
        'project_stages': project_stages,
        'form_acquisition': form_acquisition,
        'currency': currency,
    }

    return render(request, 'projectbudget/logistic/add_acquisition.html', context)


@login_required(login_url='/authentication/login')
def edit_acquisition(request, id):
    acquisition = Logistic.objects.get(pk=id)
    acquisition_type = AcquisitionType.objects.values_list('name', flat=True).distinct()

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    projects = Project.objects.all()
    project_stages = ProjectStage.objects.all()

    if request.method == 'POST':
        form_acquisition = LogisticForm(request.POST, instance=acquisition)
        if form_acquisition.is_valid():
            acquisition_instance = form_acquisition.save(commit=False)
            acquisition_instance.owner = request.user
            acquisition_instance.save()
            messages.success(request, 'Acquisition updated successfully')
            return redirect('logistic')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form_acquisition = LogisticForm(instance=acquisition)

    context = {
        'acquisition': acquisition,
        'acquisition_type': acquisition_type,
        'projects': projects,
        'project_stages': project_stages,
        'form_acquisition': form_acquisition,
        'date': acquisition.date,
        'currency': currency
    }

    return render(request, 'projectbudget/logistic/edit_acquisition.html', context)


@login_required(login_url='/authentication/login')
def delete_acquisition(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        acquisition = Logistic.objects.get(pk=id)
        acquisition.delete()
        return JsonResponse({'message': 'Acquisition deleted'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


# ---->>>>>>>>>> ACQUISITIONS - EXPORT FILES VIEWS <<<<<<<<<<<<----#

def export_acquisitions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Acquisitions' + \
                                      str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    writer.writerow(['Project Name', 'Project Stage', 'Acquisition Name', 'Acquisition Type', 'Document Type',
                     'Document Series', 'Supplier Name', 'Acquisition Description', 'Acquisition Owner',
                     f'Amount ({currency})', 'Date'])

    acquisitions = Logistic.objects.filter(owner=request.user)

    for acquisition in acquisitions:
        writer.writerow([acquisition.project_name.project_name, acquisition.project_stage,
                         acquisition.acquisition_name, acquisition.acquisition_type, acquisition.document_type,
                         acquisition.document_series, acquisition.supplier_name,
                         acquisition.acquisition_description, acquisition.acquisition_owner,
                         acquisition.amount, acquisition.date])
    return response


def export_acquisitions_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Acquisitions' + \
                                      str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Acquisitions')
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

    columns = ['Project Name', 'Project Stage', 'Acquisition Name', 'Acquisition Type', 'Document Type',
               'Document Series', 'Supplier Name', 'Acquisition Description', 'Acquisition Owner',
               f'Amount ({currency})', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style_bold)

    rows = Logistic.objects.filter(owner=request.user).values_list(
        'project_name__project_name', 'project_stage', 'acquisition_name', 'acquisition_type', 'document_type',
        'document_series', 'supplier_name', 'acquisition_description', 'acquisition_owner', 'amount', 'date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 10:
                ws.write(row_num, col_num, row[col_num], date_style)
            elif col_num == 9:
                formatted_value = "{:.2f}".format(row[col_num])
                amount_style = xlwt.easyxf('align: horiz right')
                ws.write(row_num, col_num, formatted_value, amount_style)
            else:
                ws.write(row_num, col_num, str(row[col_num]))

    wb.save(response)

    return response


def export_acquisitions_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Logistic' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = SimpleDocTemplate(response,  pagesize=landscape(A4), title='PDF Logistic_Report', topMargin=0.5*inch)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = 1
    title_style.fontSize = 18

    elements = []

    # Add a title
    title_text = 'Logistic Report'
    elements.append(Paragraph(title_text, title_style))

    # Add spacer to create space between title and table header
    elements.append(Spacer(1, 24))

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    headers = ['Project\nName', 'Project\nStage', 'Acquisition\nName', 'Acquisition\nType', 'Document\nType',
               'Document\nSeries', 'Supplier\nName', 'Acquisition\nDescription', 'Acquisition\nOwner',
               f'Amount\n({currency})', 'Date']
    data = [headers]

    acquisitions = Logistic.objects.filter(owner=request.user)

    for acquisition in acquisitions:
        formatted_date = acquisition.date.strftime('%d-%m-%Y')
        data.append([
            acquisition.project_name.project_name, acquisition.project_stage, acquisition.acquisition_name,
            acquisition.acquisition_type, acquisition.document_type, acquisition.document_series,
            acquisition.supplier_name, acquisition.acquisition_description, acquisition.acquisition_owner,
            acquisition.amount, formatted_date
        ])

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


# ---->>>>>>>>>> PROJECT DISPLACEMENT - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def displacement_view(request):
    displacement = Displacement.objects.filter(owner=request.user).select_related('project_name')
    today = datetime.date.today()

    paginator = Paginator(displacement, 7)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'displacement': displacement,
        'today': today,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'projectbudget/displacement/project_displacement.html', context)


@login_required(login_url='/authentication/login')
def add_displacement(request):
    displacement_type = DisplacementType.objects.values_list('name', flat=True).distinct()

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    projects = Project.objects.all()
    project_stages = ProjectStage.objects.all()

    if request.method == 'POST':
        form_displacement = DisplacementForm(request.POST)
        if form_displacement.is_valid():
            displacement_instance = form_displacement.save(commit=False)
            displacement_instance.owner = request.user
            displacement_instance.save()
            messages.success(request, 'Displacement saved successfully')
            return redirect('displacement')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form_displacement = DisplacementForm()

    context = {
        'displacement_type': displacement_type,
        'projects': projects,
        'project_stages': project_stages,
        'form_displacement': form_displacement,
        'currency': currency,
    }

    return render(request, 'projectbudget/displacement/add_displacement.html', context)


@login_required(login_url='/authentication/login')
def edit_displacement(request, id):
    displacement = Displacement.objects.get(pk=id)
    displacement_type = DisplacementType.objects.values_list('name', flat=True).distinct()

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    projects = Project.objects.all()
    project_stages = ProjectStage.objects.all()

    if request.method == 'POST':
        form_displacement = DisplacementForm(request.POST, instance=displacement)
        if form_displacement.is_valid():
            displacement_instance = form_displacement.save(commit=False)
            displacement_instance.owner = request.user
            displacement_instance.save()
            messages.success(request, 'Displacement updated successfully')
            return redirect('displacement')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form_displacement = DisplacementForm(instance=displacement)

    context = {
        'displacement': displacement,
        'displacement_type': displacement_type,
        'projects': projects,
        'project_stages': project_stages,
        'form_displacement': form_displacement,
        'start_date': displacement.start_date,
        'end_date': displacement.end_date,
        'currency': currency
    }

    return render(request, 'projectbudget/displacement/edit_displacement.html', context)


@login_required(login_url='/authentication/login')
def delete_displacement(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        displacement = Displacement.objects.get(pk=id)
        displacement.delete()
        return JsonResponse({'message': 'Displacement deleted'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


# ---->>>>>>>>>> DISPLACEMENTS - EXPORT FILES VIEWS <<<<<<<<<<<<----#

def export_displacements_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Displacements' + \
                                      str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    writer.writerow(['Institution', 'Person Name', 'Project Name', 'Project Stage', 'Document Series', 'Displaced To...',
                     'Displacement Type', f'Amount ({currency})', 'Days No...', 'Start Date', 'End Date'])

    displacements = Displacement.objects.filter(owner=request.user)

    for displacement in displacements:
        writer.writerow([displacement.institution, displacement.person_name, displacement.project_name.project_name, displacement.project_stage,
                         displacement.document_series, displacement.displaced_to, displacement.displacement_type,
                         displacement.amount, displacement.days_no, displacement.start_date, displacement.end_date])
    return response


def export_displacements_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Displacements' + \
                                      str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Displacements')
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

    columns = ['Institution', 'Person Name', 'Project Name', 'Project Stage', 'Document Series', 'Displaced To...',
               'Displacement Type', f'Amount ({currency})', 'Days No...', 'Start Date', 'End Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style_bold)

    rows = Displacement.objects.filter(owner=request.user).values_list(
        'institution', 'person_name', 'project_name__project_name', 'project_stage', 'document_series', 'displaced_to',
        'displacement_type', 'amount', 'days_no', 'start_date', 'end_date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 9 or col_num == 10:
                ws.write(row_num, col_num, row[col_num], date_style)
            elif col_num == 7:
                formatted_value = "{:.2f}".format(row[col_num])
                amount_style = xlwt.easyxf('align: horiz right')
                ws.write(row_num, col_num, formatted_value, amount_style)
            else:
                ws.write(row_num, col_num, str(row[col_num]))

    wb.save(response)

    return response


def export_displacements_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Displacements' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = SimpleDocTemplate(response,  pagesize=landscape(A4), title='PDF Displacement_Report', topMargin=0.5*inch)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = 1
    title_style.fontSize = 18

    elements = []

    # Add a title
    title_text = 'Displacement Report'
    elements.append(Paragraph(title_text, title_style))

    # Add spacer to create space between title and table header
    elements.append(Spacer(1, 24))

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    headers = ['Institution', 'Person\nName', 'Project\nName', 'Project\nStage', 'Document\nSeries', 'Displaced\nTo...',
               'Displacement\nType', f'Amount\n({currency})', 'Days\nNo...', 'Start\nDate', 'End\nDate']
    data = [headers]

    displacements = Displacement.objects.filter(owner=request.user)

    for displacement in displacements:
        formatted_start_date = displacement.start_date.strftime('%d-%m-%Y')
        formatted_end_date = displacement.end_date.strftime('%d-%m-%Y')
        data.append([
            displacement.institution, displacement.person_name, displacement.project_name.project_name,
            displacement.project_stage,
            displacement.document_series, displacement.displaced_to, displacement.displacement_type,
            displacement.amount, displacement.days_no, formatted_start_date, formatted_end_date
        ])

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


# ---->>>>>>>>>> PROJECT WORKFORCE - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def workforce_view(request):
    workforce = Workforce.objects.filter(owner=request.user).select_related('project_name')

    paginator = Paginator(workforce, 7)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'workforce': workforce,
        # 'today': today,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'projectbudget/workforce/project_workforce.html', context)


@login_required(login_url='/authentication/login')
def add_workforce(request):
    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    projects = Project.objects.all()
    project_stages = ProjectStage.objects.all()

    if request.method == 'POST':
        form_workforce = WorkforceForm(request.POST)
        if form_workforce.is_valid():
            workforce_instance = form_workforce.save(commit=False)
            workforce_instance.owner = request.user
            workforce_instance.save()
            messages.success(request, 'Workforce saved successfully')
            return redirect('workforce')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form_workforce = WorkforceForm()

    context = {
        'projects': projects,
        'project_stages': project_stages,
        'form_workforce': form_workforce,
        'currency': currency,
    }

    return render(request, 'projectbudget/workforce/add_workforce.html', context)


@login_required(login_url='/authentication/login')
def edit_workforce(request, id):
    workforce = Workforce.objects.get(pk=id)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    except Currency.DoesNotExist:
        currency = 'RON'

    projects = Project.objects.all()
    project_stages = ProjectStage.objects.all()

    if request.method == 'POST':
        form_workforce = WorkforceForm(request.POST, instance=workforce)
        if form_workforce.is_valid():
            workforce_instance = form_workforce.save(commit=False)
            workforce_instance.owner = request.user
            workforce_instance.save()
            messages.success(request, 'Workforce updated successfully')
            return redirect('workforce')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form_workforce = WorkforceForm(instance=workforce)

    context = {
        'workforce': workforce,
        'projects': projects,
        'project_stages': project_stages,
        'form_workforce': form_workforce,
        'currency': currency
    }

    return render(request, 'projectbudget/workforce/edit_workforce.html', context)


@login_required(login_url='/authentication/login')
def delete_workforce(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        workforce = Workforce.objects.get(pk=id)
        workforce.delete()
        return JsonResponse({'message': 'Workforce deleted'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)