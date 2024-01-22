from django.db.models import Sum, ExpressionWrapper, F
from django.db.models import FloatField
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from .models import Expense, Category, Source, Income
from .forms import ExpenseForm
# from .filters import ExpenseFilter
from preferences.models import Currency
import datetime
import csv
import xlwt
import io
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph
# from settings.models import Setting

# Create your views here.


# ---->>>>>>>>>> PERSONAL BUDGET - HOMEPAGE VIEW <<<<<<<<<<<<----#


def personal_budget_home(request):
    # Logica pentru pagina de inserare a datelor in tabel
    expenses = Expense.objects.all()
    return render(request, 'personal_budget/index.html',
                  {'expenses': expenses})


# ---->>>>>>>>>> EXPENSES - PAGE VIEWS <<<<<<<<<<<<----#
# Logica pentru vizualizarea cheltuielilor

@login_required(login_url='/authentication/login')
def expenses_view(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    expenses.extra(
        select={'amount': 'cost * qty'})
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = Currency.objects.get(user=request.user).currency
    except Currency.DoesNotExist:
        currency = 'RON - Romanian  Leu'

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }

    return render(request, 'personal_budget/expenses/user_expenses.html',
                  context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    # Logica pentru adaugarea cheltuielilor
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'personal_budget/expenses/add_expense.html',
                      context)

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
            return render(request, 'personal_budget/expenses/add_expense.html',
                          context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personal_budget/expenses/add_expense.html',
                          context)
        if not cost:
            messages.error(request, 'Cost is required')
            return render(request, 'personal_budget/expenses/add_expense.html',
                          context)
        if not qty:
            messages.error(request, 'Quantity is required')
            return render(request, 'personal_budget/expenses/add_expense.html',
                          context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_budget/expenses/add_expense.html',
                          context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_budget/expenses/add_expense.html',
                          context)

        Expense.objects.create(owner=request.user, item=item, category=category,
                               description=description, cost=cost, qty=qty,
                               amount=amount, date=date)

        messages.success(request, 'Item saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'personal_budget/expenses/edit_expense.html',
                      context)
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
            return render(request, 'personal_budget/expenses/edit_expense.html',
                          context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personal_budget/expenses/add_expense.html',
                          context)
        if not cost:
            messages.error(request, 'Cost is required')
            return render(request, 'personal_budget/expenses/edit_expense.html',
                          context)
        if not qty:
            messages.error(request, 'Quantity is required')
            return render(request, 'personal_budget/expenses/edit_expense.html',
                          context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_budget/expenses/edit_expense.html',
                          context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_budget/expenses/edit_expense.html',
                          context)

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
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Item', 'Category', 'Description', 'Amount', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style.font.bold = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list(
        'item', 'category', 'description', 'amount', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


def export_expenses_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = canvas.Canvas(response, pagesize=A4)
    pdf.setTitle('PDF Report')

    # styleSheet = getSampleStyleSheet()
    # style = styleSheet["BodyText"]
    # P = Paragraph('This is an example', style)

    headers = ['item', 'category', 'description', 'amount', 'date']
    data = [headers]

    expenses = Expense.objects.filter(owner=request.user)

    # sum = expenses.aggregate(Sum('amount'))

    for expense in expenses:
        data.append([expense.item, expense.category, expense.description,
                     expense.amount, expense.date])

    table = Table(data)
    table.setStyle(TableStyle(
        [('BACKGROUND', (0, 0), (-1, 0), colors.grey),
         ('GRID', (0, 0), (-1, -1), 1, colors.black),
         ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
         ('FONTSIZE', (0, 0), (-1, 0), 14),
         ('TEXTFONT', (0, 0), (-1, 0), 'Times-Bold'),
         ('RIGHTPADDING', (0, 0), (-1, 0), 50),
         ('TOPPADDING', (0, 0), (-1, 0), 10)]
    ))

    # canvas.drawString(10, 150, "Basic data")

    canvas_width = 600
    canvas_height = 600

    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 45, canvas_height - len(data))

    pdf.save()
    return response

    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename=Expenses' + \
    #                                   str(datetime.datetime.now()) + '.pdf'
    #
    # response['Content-Transfer-Encoding'] = 'binary'
    #
    # html_string = render_to_string('personal_budget/expenses/pdf_output.html',
    #                                {'expenses': [], 'total': 0})
    # html = HTML(string=html_string)
    #
    # result = html.write_pdf()
    #
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name, 'rb')
    #     response.write(output.read())
    #
    # return response


# ---->>>>>>>>>> EXPENSES CHARTS <<<<<<<<<<<<----#

def expenses_category_chart(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 3)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago,
                                      date__lte=todays_date)

    def get_categories(expense):
        return expense.category

    finalrep = {}
    category_list = list(set(map(get_categories, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def last_3months_expense_source_stats(request):
    todays_date = datetime.date.today()
    last_month = datetime.date.today() - datetime.timedelta(days=0)
    last_2_month = last_month - datetime.timedelta(days=30)
    last_3_month = last_2_month - datetime.timedelta(days=30)

    last_month_expense = Expense.objects.filter(owner=request.user,
                                                date__gte=last_month,
                                                date__lte=todays_date).order_by('date')
    prev_month_expense = Expense.objects.filter(owner=request.user,
                                                date__gte=last_month,
                                                date__lte=last_2_month)
    prev_prev_month_expense = Expense.objects.filter(owner=request.user,
                                                     date__gte=last_2_month,
                                                     date__lte=last_3_month)

    keyed_data = []
    this_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
    prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
    prev_prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}

    for x in last_month_expense:
        month = str(x.date)[:7]
        date_in_month = str(x.date)[:2]
        if int(date_in_month) <= 7:
            this_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            this_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            this_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            this_month_data['29th'] += x.amount

    keyed_data.append({str(last_month): this_month_data})

    for x in prev_month_expense:
        date_in_month = str(x.date)[:2]
        month = str(x.date)[:7]
        if int(date_in_month) <= 7:
            prev_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            prev_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            prev_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            prev_month_data['29th'] += x.amount

    keyed_data.append({str(last_2_month): prev_month_data})

    for x in prev_prev_month_expense:
        date_in_month = str(x.date)[:2]
        month = str(x.date)[:7]
        if int(date_in_month) <= 7:
            prev_prev_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            prev_prev_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            prev_prev_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            prev_prev_month_data['29th'] += x.amount

    keyed_data.append({str(last_3_month): prev_prev_month_data})
    return JsonResponse({'cumulative_expenses_data': keyed_data}, safe=False)


# ---->>>>>>>>>> EXPENSES SUMMARY / CHARTS - PAGE VIEWS <<<<<<<<<<<<----#

def expenses_summary_rest(request):
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
            if x == day_ and month == month_ and year_ == today_year:
                if not day_ > today_day:
                    day_amount += one.amount
        return day_amount

    for x in range(1, 8):
        today_day, today_month, today_year = datetime.datetime.today(
        ).isoweekday(), datetime.datetime.today(
        ).month, datetime.datetime.today().year
        for one in all_expenses:
            week_days_data[x] = get_amount_for_day(
                x, today_day, today_month, today_year)

    data = {"months": months_data, "days": week_days_data}
    return JsonResponse({'data': data}, safe=False)


@login_required(login_url='/authentication/login')
def expenses_summary_view(request):
    all_expenses = Expense.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()
    today2 = datetime.date.today().replace(day=1)

    week_ago = today - datetime.timedelta(days=7)
    month_ago = today - datetime.timedelta(days=30)
    year_ago = today - datetime.timedelta(days=366)

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

        if one.date >= week_ago:
            this_week_amount += one.amount
            this_week_count += 1

        if today2.replace(day=1) <= one.date <= today:
            this_month_amount += one.amount
            this_month_count += 1

        if one.date >= year_ago:
            this_year_amount += one.amount
            this_year_count += 1

    context = {
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
    return render(request, 'personal_budget/expenses/expenses_summary.html', context)


# ---->>>>>>>>>> INCOME - PAGE VIEWS <<<<<<<<<<<<----#
# Logica pentru vizualizarea veniturilor

@login_required(login_url='/authentication/login')
def income_view(request):
    sources = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = Currency.objects.get(user=request.user).currency
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
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'personal_budget/income/add_income.html',
                      context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_budget/income/add_income.html',
                          context)

        source = request.POST['source']
        description = request.POST['description']
        date = request.POST['income_date']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personal_budget/income/add_income.html',
                          context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_budget/income/add_income.html',
                          context)

        Income.objects.create(owner=request.user, amount=amount, source=source,
                              description=description, date=date)

        messages.success(request, 'Record saved successfully')

        return redirect('income')


@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'personal_budget/income/edit_income.html',
                      context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_budget/income/edit_income.html',
                          context)

        source = request.POST['source']
        description = request.POST['description']
        date = request.POST['income_date']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'personal_budget/income/edit_income.html',
                          context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_budget/income/edit_income.html',
                          context)

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
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Source', 'Description', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style.font.bold = xlwt.XFStyle()

    rows = Income.objects.filter(owner=request.user).values_list(
        'amount', 'source', 'description', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


def export_income_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Income' + \
                                      str(datetime.datetime.now()) + '.pdf'

    pdf = canvas.Canvas(response, pagesize=A4)
    pdf.setTitle('PDF Report')

    headers = ['amount', 'source', 'description', 'date']
    data = [headers]

    incomes = Income.objects.filter(owner=request.user)

    for income in incomes:
        data.append([income.amount, income.source, income.description, income.date])

    table = Table(data)
    table.setStyle(TableStyle(
        [('BACKGROUND', (0, 0), (-1, 0), colors.grey),
         ('GRID', (0, 0), (-1, -1), 1, colors.black),
         ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
         ('FONTSIZE', (0, 0), (-1, 0), 14),
         ('TEXTFONT', (0, 0), (-1, 0), 'Times-Bold'),
         ('RIGHTPADDING', (0, 0), (-1, 0), 50),
         ('TOPPADDING', (0, 0), (-1, 0), 10)]
    ))

    canvas_width = 600
    canvas_height = 600

    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 45, canvas_height - len(data))

    pdf.save()
    return response


# ---->>>>>>>>>> INCOME CHARTS <<<<<<<<<<<<----#

def income_source_chart(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 3)
    income = Income.objects.filter(owner=request.user,
                                      date__gte=six_months_ago,
                                      date__lte=todays_date)

    def get_sources(income):
        return income.source

    finalrep = {}
    source_list = list(set(map(get_sources, income)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in income:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data': finalrep}, safe=False)


def last_3months_income_source_stats(request):
    todays_date = datetime.date.today()
    last_month = datetime.date.today() - datetime.timedelta(days=0)
    last_2_month = last_month - datetime.timedelta(days=30)
    last_3_month = last_2_month - datetime.timedelta(days=30)

    last_month_income = Income.objects.filter(owner=request.user,
                                                date__gte=last_month,
                                                date__lte=todays_date).order_by('date')
    prev_month_income = Income.objects.filter(owner=request.user,
                                                date__gte=last_month,
                                                date__lte=last_2_month)
    prev_prev_month_income = Income.objects.filter(owner=request.user,
                                                     date__gte=last_2_month,
                                                     date__lte=last_3_month)

    keyed_data = []
    this_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
    prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
    prev_prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}

    for x in last_month_income:
        month = str(x.date)[:7]
        date_in_month = str(x.date)[:2]
        if int(date_in_month) <= 7:
            this_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            this_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            this_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            this_month_data['29th'] += x.amount

    keyed_data.append({str(last_month): this_month_data})

    for x in prev_month_income:
        date_in_month = str(x.date)[:2]
        month = str(x.date)[:7]
        if int(date_in_month) <= 7:
            prev_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            prev_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            prev_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            prev_month_data['29th'] += x.amount

    keyed_data.append({str(last_2_month): prev_month_data})

    for x in prev_prev_month_income:
        date_in_month = str(x.date)[:2]
        month = str(x.date)[:7]
        if int(date_in_month) <= 7:
            prev_prev_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            prev_prev_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            prev_prev_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            prev_prev_month_data['29th'] += x.amount

    keyed_data.append({str(last_3_month): prev_month_data})
    return JsonResponse({'cumulative_income_data': keyed_data}, safe=False)


# ---->>>>>>>>>> INCOME SUMMARY / CHARTS - PAGE VIEWS <<<<<<<<<<<<----#

def income_summary_rest(request):
    all_incomes = Income.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()

    today_amount = 0

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
            if x == day_ and month == month_ and year_ == today_year:
                if not day_ > today_day:
                    day_amount += one.amount
        return day_amount

    for x in range(1, 8):
        today_day, today_month, today_year = datetime.datetime.today(
        ).isoweekday(), datetime.datetime.today(
        ).month, datetime.datetime.today().year
        for one in all_incomes:
            week_days_data[x] = get_amount_for_day(
                x, today_day, today_month, today_year)

    data = {"months": months_data, "days": week_days_data}
    return JsonResponse({'data': data}, safe=False)


@login_required(login_url='/authentication/login')
def income_summary_view(request):

    all_incomes = Income.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()
    today2 = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    month_ago = today - datetime.timedelta(days=30)
    year_ago = today - datetime.timedelta(days=366)

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

        if one.date >= week_ago:
            this_week_amount += one.amount
            this_week_count += 1

        if one.date >= month_ago:
            this_month_amount += one.amount
            this_month_count += 1

        if one.date >= year_ago:
            this_year_amount += one.amount
            this_year_count += 1

    # currency = Setting.objects.get(user=request.user).currency
    context = {
        # 'currency': currency.split('-')[0],
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
    return render(request, 'personal_budget/income/income_summary.html', context)



