from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from .models import Expense, Category, Source, Income
from preferences.models import Currency
# from .filters import ExpenseFilter

from django.db.models import Count, F, Sum
import datetime
import csv
import xlwt
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle


# Create your views here.


# ---->>>>>>>>>> PERSONAL BUDGET - PAGE VIEW <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def personal_budget_view(request):
    return render(request, 'personal_budget/index.html')


@login_required(login_url='/authentication/login')
def budget_main_view(request):
    todays_date = datetime.date.today()
    first_day_of_month = todays_date.replace(day=1)
    last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month + 1) - datetime.timedelta(days=1)

    expenses = Expense.objects.filter(owner=request.user, date__range=[first_day_of_month, last_day_of_month])
    incomes = Income.objects.filter(owner=request.user, date__range=[first_day_of_month, last_day_of_month])

    def get_categories_expenses(expense):
        return expense.category

    category_list = list(set(map(get_categories_expenses, expenses)))

    def get_sources_income(income):
        return income.source

    source_list = list(set(map(get_sources_income, incomes)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    category_data = [{'category': category, 'amount': get_expense_category_amount(category)} for category in
                     category_list]
    source_data = [{'source': source, 'amount': get_income_source_amount(source)} for source in
                   source_list]

    this_month_total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    this_month_total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_budget = this_month_total_income - this_month_total_expenses

    try:
        currency = Currency.objects.get(user=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON - Romanian  Leu'

    return render(request, 'personal_budget/budget_main.html',{'category_data': category_data,
                                                               'source_data': source_data, 'currency': currency,
                                                               'this_month_total_expenses': this_month_total_expenses,
                                                               'this_month_total_income': this_month_total_income,
                                                               'remaining_budget': remaining_budget})

# ---->>>>>>>>>> EXPENSES - PAGE VIEWS <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def expenses_view(request):
    # The Logic for expenses visualization
    expenses = Expense.objects.filter(owner=request.user).order_by('date').values()

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(user=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON - Romanian  Leu'

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'personal_budget/expenses/user_expenses.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    # The Logic for adding expenses
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'personal_budget/expenses/add_expense.html', context)

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
            return render(request, 'personal_budget/expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personal_budget/expenses/add_expense.html', context)
        if not cost:
            messages.error(request, 'Cost is required')
            return render(request, 'personal_budget/expenses/add_expense.html', context)
        if not qty:
            messages.error(request, 'Quantity is required')
            return render(request, 'personal_budget/expenses/add_expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_budget/expenses/add_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_budget/expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, item=item, category=category,
                               description=description, cost=cost, qty=qty,
                               amount=amount, date=date)

        messages.success(request, 'Item saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    # The Logic for editing expenses
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'personal_budget/expenses/edit_expense.html', context)

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
            return render(request, 'personal_budget/expenses/edit_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personal_budget/expenses/add_expense.html', context)
        if not cost:
            messages.error(request, 'Cost is required')
            return render(request, 'personal_budget/expenses/edit_expense.html', context)
        if not qty:
            messages.error(request, 'Quantity is required')
            return render(request, 'personal_budget/expenses/edit_expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_budget/expenses/edit_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_budget/expenses/edit_expense.html', context)

        expense.owner = request.user
        expense.item = item
        expense.category = category
        expense.description = category
        expense.cost = cost
        expense.qty = qty
        expense.amount = amount
        expense.date = date

        expense.save()
        messages.success(request, 'Item updated successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Item deleted')
    return redirect('expenses')


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


# ---->>>>>>>>>> EXPENSES - EXPORT FILES VIEWS <<<<<<<<<<<<----#

def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
                                      str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Item', 'Category', 'Description', 'Amount', 'Date'])

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

    columns = ['Item', 'Category', 'Description', 'Amount', 'Date']

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

    pdf = canvas.Canvas(response, pagesize=A4)
    pdf.setTitle('PDF Expenses_Report')

    # Add a title
    title_text = 'Expenses Report'
    pdf.setFont('Helvetica-Bold', 16)

    # Adjust the Y-coordinate for the title to add space above
    title_y = A4[1] - 70
    pdf.drawCentredString(A4[0] / 2, title_y, title_text)

    headers = ['Item', 'Category', 'Description', 'Amount', 'Date']
    data = [headers]

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        data.append([expense.item, expense.category, expense.description,
                     expense.amount, expense.date])

    table = Table(data)
    table.setStyle(TableStyle(
        [('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
         ('GRID', (0, 0), (-1, -1), 1, colors.black),
         ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
         ('FONTSIZE', (0, 0), (-1, 0), 14),
         ('TEXTFONT', (0, 0), (-1, 0), 'Times-Bold'),
         ('RIGHTPADDING', (0, 0), (-1, 0), 30),
         ('LEFTPADDING', (0, 0), (-1, 0), 30),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
         ('TOPPADDING', (0, 0), (-1, 0), 10)]
    ))

    canvas_width = 600
    canvas_height = 600

    # Increase the X-coordinate value to move the table more to the right
    # Increase the Y-coordinate value for more space at the top
    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 45, canvas_height - len(data) * 8)  # Adjust the multiplier as needed

    pdf.save()
    return response


# ---->>>>>>>>>> EXPENSES STATS <<<<<<<<<<<<----#

def expenses_category_stats_last_6months(request):
    # The Logic for expenses visualization from the last 6 months on each category #
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
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    last_2_month = last_month - datetime.timedelta(days=30)

    last_month_expenses = Expense.objects.filter(owner=request.user)
    prev_month_expenses = Expense.objects.filter(owner=request.user)
    prev_prev_month_expenses = Expense.objects.filter(owner=request.user)

    # Calculate the date ranges for each three-month period
    today_start = today.replace(day=1)
    last_month_start = last_month.replace(day=1)
    last_2_month_start = last_2_month.replace(day=1)

    today_end = today
    last_month_end = last_month
    last_2_month_end = last_2_month

    this_month_data = get_expenses_for_period(today_start, today_end, last_month_expenses)
    prev_month_data = get_expenses_for_period(last_month_start, last_month_end, prev_month_expenses)
    prev_prev_month_data = get_expenses_for_period(last_2_month_start, last_2_month_end, prev_prev_month_expenses)

    keyed_data = [
        {str(today_start): this_month_data},
        {str(last_month_start): prev_month_data},
        {str(last_2_month_start): prev_prev_month_data},
    ]

    return JsonResponse({'cumulative_expenses_data': keyed_data}, safe=False)


# ---->>>>>>>>>> INCOME - PAGE VIEWS <<<<<<<<<<<<----#
# Logica pentru vizualizarea veniturilor

@login_required(login_url='/authentication/login')
def income_view(request):
    # The Logic for income visualization
    sources = Source.objects.all()
    income = Income.objects.filter(owner=request.user).order_by('date').values()

    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = Currency.objects.get(user=request.user).currency.split('-')[0]
    except Currency.DoesNotExist:
        currency = 'RON - Romanian  Leu'

    context = {
        'sources': sources,
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'personal_budget/income/user_income.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    # The Logic for adding income
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'personal_budget/income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_budget/income/add_income.html', context)

        source = request.POST['source']
        description = request.POST['description']
        date = request.POST['income_date']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personal_budget/income/add_income.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_budget/income/add_income.html', context)

        Income.objects.create(owner=request.user, amount=amount, source=source,
                              description=description, date=date)

        messages.success(request, 'Record saved successfully')

        return redirect('income')


@login_required(login_url='/authentication/login')
def edit_income(request, id):
    # The Logic for editing income
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'personal_budget/income/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_budget/income/edit_income.html', context)

        source = request.POST['source']
        description = request.POST['description']
        date = request.POST['income_date']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personal_budget/income/edit_income.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_budget/income/edit_income.html', context)

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
    writer.writerow(['Amount', 'Source', 'Description', 'Date'])

    incomes = Income.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.amount, income.source, income.description,
                         income.date])
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

    columns = ['Amount', 'Source', 'Description', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style_bold)

    rows = Income.objects.filter(owner=request.user).values_list(
        'amount', 'source', 'description', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]))

    wb.save(response)

    return response


def export_income_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Income' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = canvas.Canvas(response, pagesize=A4)
    pdf.setTitle('PDF Income_Report')

    # Add a title
    title_text = 'Incomes Report'
    pdf.setFont('Helvetica-Bold', 16)

    # Adjust the Y-coordinate for the title to add space above
    title_y = A4[1] - 80
    pdf.drawCentredString(A4[0] / 2, title_y, title_text)

    headers = ['Amount', 'Source', 'Description', 'Date']
    data = [headers]

    incomes = Income.objects.filter(owner=request.user)

    for income in incomes:
        data.append([income.amount, income.source, income.description, income.date])

    table = Table(data)
    table.setStyle(TableStyle(
        [('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
         ('GRID', (0, 0), (-1, -1), 1, colors.black),
         ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
         ('FONTSIZE', (0, 0), (-1, 0), 14),
         ('TEXTFONT', (0, 0), (-1, 0), 'Times-Bold'),
         ('RIGHTPADDING', (0, 0), (-1, 0), 30),
         ('LEFTPADDING', (0, 0), (-1, 0), 30),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
         ('TOPPADDING', (0, 0), (-1, 0), 10)]
    ))

    canvas_width = 600
    canvas_height = 600

    # Increase the X-coordinate value to move the table more to the right
    # Increase the Y-coordinate value for more space at the top
    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 85, canvas_height - len(data) * 1)

    pdf.save()
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
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    last_2_month = last_month - datetime.timedelta(days=30)

    last_month_income = Income.objects.filter(owner=request.user)
    prev_month_income = Income.objects.filter(owner=request.user)
    prev_prev_month_income = Income.objects.filter(owner=request.user)

    # Calculate the date ranges for each three-month period
    today_start = today.replace(day=1)
    last_month_start = last_month.replace(day=1)
    last_2_month_start = last_2_month.replace(day=1)

    today_end = today
    last_month_end = last_month
    last_2_month_end = last_2_month

    this_month_data = get_expenses_for_period(today_start, today_end, last_month_income)
    prev_month_data = get_expenses_for_period(last_month_start, last_month_end, prev_month_income)
    prev_prev_month_data = get_expenses_for_period(last_2_month_start, last_2_month_end, prev_prev_month_income)

    keyed_data = [
        {str(today_start): this_month_data},
        {str(last_month_start): prev_month_data},
        {str(last_2_month_start): prev_prev_month_data},
    ]

    return JsonResponse({'cumulative_income_data': keyed_data}, safe=False)


# ---->>>>>>>>>> SUMMARY - PAGE VIEWS <<<<<<<<<<<<----#

def summary_budget_view(request):
    all_incomes = Income.objects.filter(owner=request.user)
    all_expenses = Expense.objects.filter(owner=request.user)

    today = datetime.datetime.today().date()
    today2 = datetime.date.today().replace(day=1)
    year_ago = today.replace(month=1, day=1)

    todays_amount = 0
    this_month_income_amount = 0
    this_month_expenses_amount = 0
    this_year_income_amount = 0
    this_year_expenses_amount = 0

    for one in all_incomes:
        if today2.replace(day=1) <= one.date <= today:
            this_month_income_amount += one.amount

        if year_ago <= one.date <= today:
            this_year_income_amount += one.amount

    for one in all_expenses:

        if today2.replace(day=1) <= one.date <= today:
            this_month_expenses_amount += one.amount

        if year_ago <= one.date <= today:
            this_year_expenses_amount += one.amount

    this_month_balance_amount = this_month_income_amount - this_month_expenses_amount
    this_year_balance_amount = this_year_income_amount - this_year_expenses_amount

    context = {
        'currency': Currency.objects.get(user=request.user).currency.split('-')[0],
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

    return render(request, 'personal_budget/summary/summary_budget.html', context)


def current_month_balance_stats(request):
    today = datetime.date.today()
    current_month_start = today.replace(day=1)
    current_month_end = today.replace(day=1) + datetime.timedelta(days=32) - datetime.timedelta(days=1)

    income_month_data = Income.objects.filter(owner=request.user,
                                              date__range=[current_month_start, current_month_end]).aggregate(
                                              Sum('amount'))['amount__sum'] or 0
    expenses_month_data = Expense.objects.filter(owner=request.user,
                                                 date__range=[current_month_start, current_month_end]).aggregate(
                                                 Sum('amount'))['amount__sum'] or 0

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
    today2 = datetime.date.today().replace(day=1)
    year_ago = today.replace(month=1, day=1)

    todays_amount = 0
    todays_count = 0
    this_week_amount = 0
    this_week_count = 0
    this_month_amount = 0
    this_month_count = 0
    this_year_amount = 0
    this_year_count = 0

    for one in all_expenses:
        if one.date == today:
            todays_amount += one.amount
            todays_count += 1

        # Calculate the day of the week for today (Monday=0, Sunday=6)
        today_day_of_week = today.weekday()

        if one.date >= today - datetime.timedelta(days=today_day_of_week) and one.date <= today + datetime.timedelta(days=(6 - today_day_of_week)):
            this_week_amount += one.amount
            this_week_count += 1

        if today2.replace(day=1) <= one.date <= today:
            this_month_amount += one.amount
            this_month_count += 1

        if year_ago <= one.date <= today:
            this_year_amount += one.amount
            this_year_count += 1

    context = {
        'currency': Currency.objects.get(user=request.user).currency.split('-')[0],
        'today': {
            'amount': todays_amount,
            'count': todays_count,

        },
        'this_week': {
            'amount': this_week_amount,
            'count': this_week_count,

        },
        'this_month': {
            'amount': this_month_amount,
            'count': this_month_count,

        },
        'this_year': {
            'amount': this_year_amount,
            'count': this_year_count,

        },
    }
    return render(request, 'personal_budget/summary/expenses_summary.html', context)


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


@login_required(login_url='/authentication/login')
def income_summary_view(request):
    all_incomes = Income.objects.filter(owner=request.user)

    today = datetime.datetime.today().date()
    today2 = datetime.date.today().replace(day=1)
    year_ago = today.replace(month=1, day=1)

    todays_amount = 0
    todays_count = 0
    this_week_amount = 0
    this_week_count = 0
    this_month_amount = 0
    this_month_count = 0
    this_year_amount = 0
    this_year_count = 0

    for one in all_incomes:
        if one.date == today:
            todays_amount += one.amount
            todays_count += 1

        # Calculate the day of the week for today (Monday=0, Sunday=6)
        today_day_of_week = today.weekday()

        if one.date >= today - datetime.timedelta(days=today_day_of_week) and one.date <= today + datetime.timedelta(days=(6 - today_day_of_week)):
            this_week_amount += one.amount
            this_week_count += 1

        if today2.replace(day=1) <= one.date <= today:
            this_month_amount += one.amount
            this_month_count += 1

        if year_ago <= one.date <= today:
            this_year_amount += one.amount
            this_year_count += 1

    context = {
        'currency': Currency.objects.get(user=request.user).currency.split('-')[0],
        'today': {
            'amount': todays_amount,
            "count": todays_count,

        },
        'this_week': {
            'amount': this_week_amount,
            "count": this_week_count,

        },
        'this_month': {
            'amount': this_month_amount,
            "count": this_month_count,

        },
        'this_year': {
            'amount': this_year_amount,
            "count": this_year_count,

        },
    }
    return render(request, 'personal_budget/summary/income_summary.html', context)





