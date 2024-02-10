from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
import json
from .models import Expense, Category, Source, Income
from preferences.models import Currency
from django.db.models import Count, Sum
import datetime
import csv
import xlwt
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# Create your views here.


# ---->>>>>>>>>> PERSONAL BUDGET - PAGE VIEW <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def personal_budget_view(request):
    return render(request, 'personalbudget/index.html')


@login_required(login_url='/authentication/login')
def budget_main_view(request):
    todays_date = datetime.date.today()
    first_day_of_month = todays_date.replace(day=1)
    last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month + 1) - datetime.timedelta(days=1)

    expenses = Expense.objects.filter(owner=request.user, date__range=[first_day_of_month, last_day_of_month])
    incomes = Income.objects.filter(owner=request.user, date__range=[first_day_of_month, last_day_of_month])

    category_data = expenses.values('category').annotate(amount=Sum('amount'))
    source_data = incomes.values('source').annotate(amount=Sum('amount'))

    this_month_total_expenses = expenses.aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0
    this_month_total_income = incomes.aggregate(total_income=Sum('amount'))['total_income'] or 0
    remaining_budget = this_month_total_income - this_month_total_expenses

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    return render(request, 'personalbudget/personal_budget.html', {'category_data': category_data,
                                                               'source_data': source_data, 'currency': currency,
                                                               'this_month_total_expenses': this_month_total_expenses,
                                                               'this_month_total_income': this_month_total_income,
                                                               'remaining_budget': remaining_budget})


# ---->>>>>>>>>> EXPENSES - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def expenses_view(request):
    expenses = Expense.objects.filter(owner=request.user).values()

    paginator = Paginator(expenses, 7)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'personalbudget/expenses/user_expenses.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'personalbudget/expenses/add_expense.html', context)

    if request.method == 'POST':
        item = request.POST['item']
        category = request.POST['category']
        description = request.POST['description']
        cost = request.POST['cost']
        qty = request.POST['qty']
        amount = request.POST['amount']
        date = request.POST['expense_date']

        if not item:
            messages.error(request, 'Item is required')
            return render(request, 'personalbudget/expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personalbudget/expenses/add_expense.html', context)
        if not cost:
            messages.error(request, 'Cost is required')
            return render(request, 'personalbudget/expenses/add_expense.html', context)
        if not qty:
            messages.error(request, 'Quantity is required')
            return render(request, 'personalbudget/expenses/add_expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personalbudget/expenses/add_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personalbudget/expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, item=item, category=category,
                               description=description, cost=cost, qty=qty,
                               amount=amount, date=date)

        messages.success(request, 'Item saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()

    formatted_date = expense.date.strftime('%Y-%m-%d')

    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
        'formatted_date': formatted_date
    }
    if request.method == 'GET':
        return render(request, 'personalbudget/expenses/edit_expense.html', context)

    if request.method == 'POST':
        item = request.POST['item']
        category = request.POST['category']
        description = request.POST['description']
        cost = request.POST['cost']
        qty = request.POST['qty']
        amount = request.POST['amount']
        date = request.POST['expense_date']

        if not item:
            messages.error(request, 'Item is required')
            return render(request, 'personalbudget/expenses/edit_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personalbudget/expenses/add_expense.html', context)
        if not cost:
            messages.error(request, 'Cost is required')
            return render(request, 'personalbudget/expenses/edit_expense.html', context)
        if not qty:
            messages.error(request, 'Quantity is required')
            return render(request, 'personalbudget/expenses/edit_expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personalbudget/expenses/edit_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personalbudget/expenses/edit_expense.html', context)

        expense.owner = request.user
        expense.item = item
        expense.category = category
        expense.description = description
        expense.cost = cost
        expense.qty = qty
        expense.amount = amount
        expense.date = date

        expense.save()
        messages.success(request, 'Item updated successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        expense = Expense.objects.get(pk=id)
        expense.delete()
        return JsonResponse({'message': 'Item deleted'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            item__icontains=search_str,
            owner=request.user) | Expense.objects.filter(
            category__icontains=search_str,
            owner=request.user) | Expense.objects.filter(
            description__icontains=search_str,
            owner=request.user) | Expense.objects.filter(
            cost__istartswith=search_str,
            owner=request.user) | Expense.objects.filter(
            qty__istartswith=search_str,
            owner=request.user) | Expense.objects.filter(
            amount__istartswith=search_str,
            owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


# ---->>>>>>>>>> EXPENSES - EXPORT Table VIEWS <<<<<<<<<<<<----#

def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
                                      str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    writer.writerow(['Item', 'Category', 'Description', f'Amount ({currency})', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.item, expense.category, expense.description,
                         expense.amount, expense.date])
    return response


def export_expenses_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
                                      str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style_bold = xlwt.XFStyle()
    font_style_bold.font.bold = True

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    columns = ['Item', 'Category', 'Description', f'Amount ({currency})', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style_bold)

    rows = Expense.objects.filter(owner=request.user).values_list(
        'item', 'category', 'description', 'amount', 'date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]))

    wb.save(response)

    return response


def export_expenses_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = SimpleDocTemplate(response, pagesize=A4, title='PDF Expenses_Report')
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = 1
    title_style.fontSize = 18

    elements = []

    # Add a title
    title_text = 'Expenses Report'
    elements.append(Paragraph(title_text, title_style))

    # Add spacer to create space between title and table header
    elements.append(Spacer(1, 24))

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    headers = ['Item', 'Category', 'Description', f'Amount\n({currency})', 'Date']
    data = [headers]

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        data.append([expense.item, expense.category, expense.description,
                     expense.amount, expense.date])

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
        ('LEFTPADDING', (0, 0), (-1, -1), 15),  # Increase left padding for all cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),  # Increase right padding for all cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ])

    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    pdf.build(elements)

    return response


# ---->>>>>>>>>> EXPENSES STATS <<<<<<<<<<<<----#
    # The Logic for expenses visualization from the last 6 months on each category #

def expenses_category_stats_last_6months(request):

    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 3)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago,
                                      date__lte=todays_date)

    def get_categories(expense):
        return expense.category

    expense_category_data = {}
    category_list = list(set(map(get_categories, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            expense_category_data[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': expense_category_data}, safe=False)


def get_expenses_for_period(start_date, end_date, expenses):
    period_data = {str(day): 0 for day in range(1, 32)}

    for expense in expenses.filter(date__gte=start_date, date__lte=end_date):
        day_in_month = expense.date.day
        period_data[str(day_in_month)] += expense.amount

    return period_data


def expenses_stats_last_3months(request):
    today = datetime.date.today()
    last_month = today - relativedelta(months=1)
    last_2_month = today - relativedelta(months=2)

    # Calculate the date ranges for each three-month period
    today_start = today.replace(day=1)
    last_month_start = last_month.replace(day=1)
    last_2_month_start = last_2_month.replace(day=1)

    today_end = today + relativedelta(day=31)
    last_month_end = last_month + relativedelta(day=31)
    last_2_month_end = last_2_month + relativedelta(day=31)

    # Fetch expenses data for each month
    this_month_expenses = Expense.objects.filter(owner=request.user, date__range=(today_start, today_end))
    last_month_expenses = Expense.objects.filter(owner=request.user, date__range=(last_month_start, last_month_end))
    prev_month_expenses = Expense.objects.filter(owner=request.user, date__range=(last_2_month_start, last_2_month_end))

    # Fetch and organize data for each period
    this_month_data = get_expenses_for_period(today_start, today_end, this_month_expenses)
    last_month_data = get_expenses_for_period(last_month_start, last_month_end, last_month_expenses)
    prev_month_data = get_expenses_for_period(last_2_month_start, last_2_month_end, prev_month_expenses)

    # Organize data for JavaScript
    keyed_data = [
        {str(today_start): this_month_data},
        {str(last_month_start): last_month_data},
        {str(last_2_month_start): prev_month_data},
    ]

    return JsonResponse({'cumulative_expenses_data': keyed_data}, safe=False)


# ---->>>>>>>>>> INCOME - PAGE VIEWS <<<<<<<<<<<<----#
# Logica pentru vizualizarea veniturilor

@login_required(login_url='/authentication/login')
def income_view(request):
    # The Logic for income visualization
    sources = Source.objects.all()
    income = Income.objects.filter(owner=request.user).values()

    paginator = Paginator(income, 7)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'sources': sources,
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'personalbudget/income/user_income.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    # The Logic for adding income
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'personalbudget/income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personalbudget/income/add_income.html', context)

        source = request.POST['source']
        description = request.POST['description']
        date = request.POST['income_date']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personalbudget/income/add_income.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personalbudget/income/add_income.html', context)

        Income.objects.create(owner=request.user, amount=amount, source=source,
                              description=description, date=date)

        messages.success(request, 'Record saved successfully')

        return redirect('income')


@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()

    # Format the date as "yyyy-MM-dd"
    formatted_date = income.date.strftime('%Y-%m-%d')

    context = {
        'income': income,
        'values': income,
        'sources': sources,
        'formatted_date': formatted_date
    }

    if request.method == 'GET':
        return render(request, 'personalbudget/income/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personalbudget/income/edit_income.html', context)

        source = request.POST['source']
        description = request.POST['description']
        date = request.POST['income_date']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personalbudget/income/edit_income.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personalbudget/income/edit_income.html', context)

        income.amount = amount
        income.source = source
        income.description = description
        income.date = date

        income.save()
        messages.success(request, 'Record updated successfully')

        return redirect('income')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Record removed')
    return redirect('income')


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str,
            owner=request.user) | Income.objects.filter(
            source__icontains=search_str,
            owner=request.user) | Income.objects.filter(
            description__icontains=search_str,
            owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


# ---->>>>>>>>>> INCOME - EXPORT FILES VIEWS <<<<<<<<<<<<----#

def export_income_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Incomes' + \
                                      str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    # currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    writer.writerow(['Source', 'Description', f'Amount ({currency})', 'Date'])

    incomes = Income.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.source, income.description, income.amount, income.date])
    return response


def export_income_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Incomes' + \
                                      str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income')
    row_num = 0
    font_style_bold = xlwt.XFStyle()
    font_style_bold.font.bold = True

    # currency = Currency.objects.get(owner=request.user).currency.split('-')[0].strip()
    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    columns = ['Source', 'Description', f'Amount ({currency})', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style_bold)

    rows = Income.objects.filter(owner=request.user).values_list(
        'source', 'description', 'amount', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]))

    wb.save(response)

    return response


def export_income_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Incomes' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = SimpleDocTemplate(response, pagesize=A4, title='PDF Incomes_Report')
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = 1
    title_style.fontSize = 18

    elements = []

    # Add a title
    title_text = 'Incomes Report'
    elements.append(Paragraph(title_text, title_style))

    # Add spacer to create space between title and table header
    elements.append(Spacer(1, 24))

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    headers = ['Source', 'Description', f'Amount ({currency})', 'Date']
    data = [headers]

    incomes = Income.objects.filter(owner=request.user)
    for income in incomes:
        data.append([income.source, income.description, income.amount, income.date])

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
        ('LEFTPADDING', (0, 0), (-1, -1), 25),  # Increase left padding for all cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 25),  # Increase right padding for all cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ])

    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    pdf.build(elements)

    return response


# ---->>>>>>>>>> INCOME STATS <<<<<<<<<<<<----#

def income_source_stats_last_6months(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 3)
    income = Income.objects.filter(owner=request.user,
                                      date__gte=six_months_ago,
                                      date__lte=todays_date)

    def get_sources(income):
        return income.source

    income_source_data = {}
    source_list = list(set(map(get_sources, income)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in income:
        for y in source_list:
            income_source_data[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data': income_source_data}, safe=False)


def get_income_for_period(start_date, end_date, incomes):
    period_data = {str(day): 0 for day in range(1, 32)}

    for income in incomes.filter(date__gte=start_date, date__lte=end_date):
        day_in_month = income.date.day
        period_data[str(day_in_month)] += income.amount

    return period_data


def income_stats_last_3months(request):
    today = datetime.date.today()
    last_month = today - relativedelta(months=1)
    last_2_month = today - relativedelta(months=2)

    # Calculate the date ranges for each three-month period
    today_start = today.replace(day=1)
    last_month_start = last_month.replace(day=1)
    last_2_month_start = last_2_month.replace(day=1)

    today_end = today + relativedelta(day=31)
    last_month_end = last_month + relativedelta(day=31)
    last_2_month_end = last_2_month + relativedelta(day=31)

    # Fetch income data for each month
    this_month_income = Income.objects.filter(owner=request.user, date__range=(today_start, today_end))
    last_month_income = Income.objects.filter(owner=request.user, date__range=(last_month_start, last_month_end))
    prev_month_income = Income.objects.filter(owner=request.user, date__range=(last_2_month_start, last_2_month_end))

    # Fetch and organize data for each period
    this_month_data = get_income_for_period(today_start, today_end, this_month_income)
    last_month_data = get_income_for_period(last_month_start, last_month_end, last_month_income)
    prev_month_data = get_income_for_period(last_2_month_start, last_2_month_end, prev_month_income)

    # Organize data for JavaScript
    keyed_data = [
        {str(today_start): this_month_data},
        {str(last_month_start): last_month_data},
        {str(last_2_month_start): prev_month_data},
    ]

    return JsonResponse({'cumulative_income_data': keyed_data}, safe=False)


# ---->>>>>>>>>> SUMMARY - PAGE VIEWS <<<<<<<<<<<<----#

def summary_budget_main_view(request):
    all_incomes = Income.objects.filter(owner=request.user)
    all_expenses = Expense.objects.filter(owner=request.user)

    today = datetime.datetime.today().date()

    todays_amount = 0
    this_month_income_amount = 0
    this_month_expenses_amount = 0
    this_year_income_amount = 0
    this_year_expenses_amount = 0

    for one in all_incomes:
        if one.date.month == today.month and one.date.year == today.year:
            this_month_income_amount += one.amount

        if one.date.year == today.year:
            this_year_income_amount += one.amount

    for one in all_expenses:
        if one.date.month == today.month and one.date.year == today.year:
            this_month_expenses_amount += one.amount

        if one.date.year == today.year:
            this_year_expenses_amount += one.amount

    this_month_balance_amount = this_month_income_amount - this_month_expenses_amount
    this_year_balance_amount = this_year_income_amount - this_year_expenses_amount

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'


    context = {
        'currency': currency,
        'today': {
            'amount': todays_amount,
        },
        'this_month_income': {
            'amount': this_month_income_amount,
        },
        'this_month_expenses': {
            'amount': this_month_expenses_amount,
        },
        'this_month_balance': {
            'amount': this_month_balance_amount,
        },
        'this_year_income': {
            'amount': this_year_income_amount,
        },
        'this_year_expenses': {
            'amount': this_year_expenses_amount,
        },
        'this_year_balance': {
            'amount': this_year_balance_amount,
        },
    }

    return render(request, 'personalbudget/summary/summary_budget.html', context)


def current_month_balance_stats(request):
    today = datetime.date.today()

    income_month_data = Income.objects.filter(
        owner=request.user, date__month=today.month, date__year=today.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    expenses_month_data = Expense.objects.filter(
        owner=request.user, date__month=today.month, date__year=today.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance_month_data = income_month_data - expenses_month_data

    current_month_data = {
        'income': income_month_data,
        'balance': balance_month_data,
    }

    return JsonResponse({'current_month_data': current_month_data}, safe=False)


def current_year_balance_stats(request):
    today = datetime.date.today()
    current_year_start = today.replace(month=1, day=1)
    current_year_end = today.replace(month=12, day=31)

    income_year_data = Income.objects.filter(owner=request.user,
                                             date__range=[current_year_start, current_year_end]).aggregate(
                                             Sum('amount'))['amount__sum'] or 0
    expenses_year_data = Expense.objects.filter(owner=request.user,
                                                date__range=[current_year_start, current_year_end]).aggregate(
                                                Sum('amount'))['amount__sum'] or 0
    balance_year_data = income_year_data - expenses_year_data

    current_year_data = {
        'income': income_year_data,
        'balance': balance_year_data,
    }
    return JsonResponse({'current_year_data': current_year_data}, safe=False)


# ---->>>>>>>>>> EXPENSES SUMMARY / STATS - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def expenses_summary_view(request):
    all_expenses = Expense.objects.filter(owner=request.user)

    today = datetime.datetime.today().date()
    today_start = today.replace(day=1)

    todays_data = all_expenses.filter(date=today).aggregate(amount=Sum('amount'), count=Count('id'))

    this_week_data = all_expenses.filter(
        date__gte=today - datetime.timedelta(days=today.weekday()),
        date__lte=today + datetime.timedelta(days=(6 - today.weekday()))
    ).aggregate(amount=Sum('amount'), count=Count('id'))

    this_month_data = all_expenses.filter(date__gte=today_start).aggregate(amount=Sum('amount'), count=Count('id'))

    this_year_data = all_expenses.filter(date__year=today.year).aggregate(amount=Sum('amount'), count=Count('id'))

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'currency': currency,
        'today': todays_data,
        'this_week': this_week_data,
        'this_month': this_month_data,
        'this_year': this_year_data,
    }
    return render(request, 'personalbudget/summary/expenses_summary.html', context)


def expenses_summary_rest_stats(request):
    all_expenses = Expense.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()

    today_amount = 0

    months_data = {}
    week_days_data = {}

    def get_amount_for_month(month):
        month_amount = 0
        for one in all_expenses:
            month_, year = one.date.month, one.date.year
            if month == month_ and year == today_year:
                month_amount += one.amount
        return month_amount

    for x in range(1, 13):
        today_month, today_year = x, datetime.datetime.today().year
        for one in all_expenses:
            months_data[x] = get_amount_for_month(x)

    def get_amount_for_day(x, today_day, month, today_year):
        day_amount = 0
        for one in all_expenses:
            day_, date_, month_, year_ = one.date.isoweekday(
            ), one.date.day, one.date.month, one.date.year

            # Check if the expense date falls within the current week
            if today - datetime.timedelta(days=today_day) <= one.date <= today + datetime.timedelta(days=(6 - today_day)):
                if x == day_ and month == month_ and year_ == today_year:
                    if not day_ > today_day:
                        day_amount += one.amount
        return day_amount

    for x in range(1, 8):
        today_day, today_month, today_year = (datetime.datetime.today().isoweekday(),
                                              datetime.datetime.today().month,
                                              datetime.datetime.today().year)
        week_days_data[x] = get_amount_for_day(x, today_day, today_month, today_year)
        for one in all_expenses:
            week_days_data[x] = get_amount_for_day(
                x, today_day, today_month, today_year)

    data = {'months': months_data, 'days': week_days_data}
    return JsonResponse({'data': data}, safe=False)


# ---->>>>>>>>>> INCOME SUMMARY / STATS - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def income_summary_view(request):
    all_incomes = Income.objects.filter(owner=request.user)

    today = datetime.datetime.today().date()
    today_start = today.replace(day=1)

    todays_data = all_incomes.filter(date=today).aggregate(amount=Sum('amount'), count=Count('id'))

    this_week_data = all_incomes.filter(
        date__gte=today - datetime.timedelta(days=today.weekday()),
        date__lte=today + datetime.timedelta(days=(6 - today.weekday()))
    ).aggregate(amount=Sum('amount'), count=Count('id'))

    this_month_data = all_incomes.filter(date__gte=today_start).aggregate(amount=Sum('amount'), count=Count('id'))

    this_year_data = all_incomes.filter(date__year=today.year).aggregate(amount=Sum('amount'), count=Count('id'))

    try:
        currency = Currency.objects.get(owner=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON'

    context = {
        'currency': currency,
        'today': todays_data,
        'this_week': this_week_data,
        'this_month': this_month_data,
        'this_year': this_year_data,
    }

    return render(request, 'personalbudget/summary/income_summary.html', context)


def income_summary_rest_stats(request):
    all_incomes = Income.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()

    months_data = {}
    week_days_data = {}

    def get_amount_for_month(month):
        month_amount = 0
        for one in all_incomes:
            month_, year = one.date.month, one.date.year
            if month == month_ and year == today_year:
                month_amount += one.amount
        return month_amount

    for x in range(1, 13):
        today_month, today_year = x, datetime.datetime.today().year
        for one in all_incomes:
            months_data[x] = get_amount_for_month(x)

    def get_amount_for_day(x, today_day, month, today_year):
        day_amount = 0
        for one in all_incomes:
            day_, date_, month_, year_ = one.date.isoweekday(
            ), one.date.day, one.date.month, one.date.year

            # Check if the expense date falls within the current week
            if today - datetime.timedelta(days=today_day) <= one.date <= today + datetime.timedelta(
                    days=(6 - today_day)):
                if x == day_ and month == month_ and year_ == today_year:
                    if not day_ > today_day:
                        day_amount += one.amount
        return day_amount

    for x in range(1, 8):
        today_day, today_month, today_year = (datetime.datetime.today().isoweekday(),
                                              datetime.datetime.today().month,
                                              datetime.datetime.today().year)
        week_days_data[x] = get_amount_for_day(x, today_day, today_month, today_year)
        for one in all_incomes:
            week_days_data[x] = get_amount_for_day(
                x, today_day, today_month, today_year)

    data = {'months': months_data, 'days': week_days_data}
    return JsonResponse({'data': data}, safe=False)


