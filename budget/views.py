from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template import loader

from .models import Items


# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile

from django.db.models import Sum

# Create your views here.


def home(request):
    # Logica pentru vizualizarea paginii principale
    html_template = loader.get_template('index.html')
    items = Items.objects.all()
    context = {'items': items}
    if request.user.is_authenticated:
        html_template = loader.get_template('homepage.html')
    return HttpResponse(html_template.render(context, request))


class HomePageView(TemplateView):
    template_name = "homepage.html"



# # _____________________________________________________________________________#
# # PERSONAL BUDGET PAGE
#
# def table_purchase(request):
#     # Logica pentru pagina de inserare a datelor in tabel
#     expenses = Expense.objects.all()
#     return render(request, 'personal_budget/index.html',
#                   {'expenses': expenses})
#
#
# def preferences_view(request):
#     # Logica pentru pagina de inserare a datelor in tabel
#     currency = Currency.objects.all()
#     return render(request, 'personal_budget/general/preferences.html',
#                   {'currency': currency})
#
#
# # _____________________________________________________________________________#
# # EXPENSE page - # Logica pentru vizualizarea cheltuielilor
#
# @login_required(login_url='/authentication/login')
# def expenses_view(request):
#     categories = Category.objects.all()
#     expenses = Expense.objects.filter(owner=request.user)
#     paginator = Paginator(expenses, 5)
#     page_number = request.GET.get('page')
#     page_obj = Paginator.get_page(paginator, page_number)
#     try:
#         currency = Currency.objects.get(user=request.user).currency
#     except Currency.DoesNotExist:
#         currency = 'RON - Romanian  Leu'
#
#     context = {
#         'expenses': expenses,
#         'page_obj': page_obj,
#         'currency': currency
#     }
#
#     return render(request, 'personal_budget/expenses/user_expenses.html',
#                   context)
#
#
# @login_required(login_url='/authentication/login')
# def add_expense(request):
#     # Logica pentru adaugarea cheltuielilor
#     categories = Category.objects.all()
#     context = {
#         'categories': categories,
#         'values': request.POST
#     }
#
#     if request.method == 'GET':
#         return render(request, 'personal_budget/expenses/add_expense.html',
#                       context)
#
#     if request.method == 'POST':
#         item = request.POST['item']
#         category = request.POST['category']
#         description = request.POST['description']
#         cost = request.POST['cost']
#         qty = request.POST['qty']
#         amount = request.POST['amount']
#         date = request.POST['expense_date']
#
#         if not item:
#             messages.error(request, 'Item is required')
#             return render(request, 'personal_budget/expenses/add_expense.html',
#                           context)
#         if not description:
#             messages.error(request, 'Description is required')
#             return render(request, 'personal_budget/expenses/add_expense.html',
#                           context)
#         if not cost:
#             messages.error(request, 'Cost is required')
#             return render(request, 'personal_budget/expenses/add_expense.html',
#                           context)
#         if not qty:
#             messages.error(request, 'Quantity is required')
#             return render(request, 'personal_budget/expenses/add_expense.html',
#                           context)
#         if not amount:
#             messages.error(request, 'Amount is required')
#             return render(request, 'personal_budget/expenses/add_expense.html',
#                           context)
#         if not date:
#             messages.error(request, 'Date is required')
#             return render(request, 'personal_budget/expenses/add_expense.html',
#                           context)
#
#         Expense.objects.create(owner=request.user, item=item, category=category,
#                                description=description, cost=cost, qty=qty,
#                                amount=amount, date=date)
#
#         messages.success(request, 'Item saved successfully')
#
#         return redirect('expenses')
#
#
# @login_required(login_url='/authentication/login')
# def edit_expense(request, id):
#     expense = Expense.objects.get(pk=id)
#     categories = Category.objects.all()
#     context = {
#         'expense': expense,
#         'values': expense,
#         'categories': categories
#     }
#     if request.method == 'GET':
#         return render(request, 'personal_budget/expenses/edit_expense.html',
#                       context)
#     if request.method == 'POST':
#
#         item = request.POST['item']
#         category = request.POST['category']
#         description = request.POST['description']
#         cost = request.POST['cost']
#         qty = request.POST['qty']
#         amount = request.POST['amount']
#         date = request.POST['expense_date']
#
#         if not item:
#             messages.error(request, 'Item is required')
#             return render(request, 'personal_budget/expenses/edit_expense.html',
#                           context)
#         if not description:
#             messages.error(request, 'Description is required')
#             return render(request, 'personal_budget/expenses/add_expense.html',
#                           context)
#         if not cost:
#             messages.error(request, 'Cost is required')
#             return render(request, 'personal_budget/expenses/edit_expense.html',
#                           context)
#         if not qty:
#             messages.error(request, 'Quantity is required')
#             return render(request, 'personal_budget/expenses/edit_expense.html',
#                           context)
#         if not amount:
#             messages.error(request, 'Amount is required')
#             return render(request, 'personal_budget/expenses/edit_expense.html',
#                           context)
#         if not date:
#             messages.error(request, 'Date is required')
#             return render(request, 'personal_budget/expenses/edit_expense.html',
#                           context)
#
#         expense.owner = request.user
#         expense.item = item
#         expense.category = category
#         expense.description = category
#         expense.cost = cost
#         expense.qty = qty
#         expense.amount = amount
#         expense.date = date
#
#         expense.save()
#         messages.success(request, 'Item updated successfully')
#
#         return redirect('expenses')
#
#
# @login_required(login_url='/authentication/login')
# def delete_expense(request, id):
#     expense = Expense.objects.get(pk=id)
#     expense.delete()
#     messages.success(request, 'Item deleted')
#     return redirect('expenses')
#
#
# def search_expenses(request):
#     if request.method == 'POST':
#         search_str = json.loads(request.body).get('searchText')
#         expenses = Expense.objects.filter(
#             item__icontains=search_str,
#             owner=request.user) | Expense.objects.filter(
#             category__icontains=search_str,
#             owner=request.user) | Expense.objects.filter(
#             description__icontains=search_str,
#             owner=request.user) | Expense.objects.filter(
#             cost__istartswith=search_str,
#             owner=request.user) | Expense.objects.filter(
#             qty__istartswith=search_str,
#             owner=request.user) | Expense.objects.filter(
#             amount__istartswith=search_str,
#             owner=request.user) | Expense.objects.filter(
#             date__istartswith=search_str, owner=request.user)
#         data = expenses.values()
#         return JsonResponse(list(data), safe=False)
#
#
# # _____________________________________________________________________________#
# # INCOME page - # Logica pentru vizualizarea veniturilor
#
# @login_required(login_url='/authentication/login')
# def income_view(request):
#     sources = Source.objects.all()
#     income = Income.objects.filter(owner=request.user)
#     paginator = Paginator(income, 5)
#     page_number = request.GET.get('page')
#     page_obj = Paginator.get_page(paginator, page_number)
#     try:
#         currency = Currency.objects.get(user=request.user).currency
#     except Currency.DoesNotExist:
#         currency = 'RON - Romanian  Leu'
#
#     context = {
#         'sources': sources,
#         'income': income,
#         'page_obj': page_obj,
#         'currency': currency
#     }
#
#     return render(request, 'personal_budget/income/user_income.html', context)
#
#
# @login_required(login_url='/authentication/login')
# def add_income(request):
#     sources = Source.objects.all()
#     context = {
#         'sources': sources,
#         'values': request.POST
#     }
#     if request.method == 'GET':
#         return render(request, 'personal_budget/income/add_income.html',
#                       context)
#
#     if request.method == 'POST':
#         amount = request.POST['amount']
#
#         if not amount:
#             messages.error(request, 'Amount is required')
#             return render(request, 'personal_budget/income/add_income.html',
#                           context)
#
#         source = request.POST['source']
#         description = request.POST['description']
#         date = request.POST['income_date']
#
#         if not description:
#             messages.error(request, 'Description is required')
#             return render(request, 'personal_budget/income/add_income.html',
#                           context)
#
#         if not date:
#             messages.error(request, 'Date is required')
#             return render(request, 'personal_budget/income/add_income.html',
#                           context)
#
#         Income.objects.create(owner=request.user, amount=amount, source=source,
#                               description=description, date=date)
#
#         messages.success(request, 'Record saved successfully')
#
#         return redirect('income')
#
#
# @login_required(login_url='/authentication/login')
# def edit_income(request, id):
#     income = Income.objects.get(pk=id)
#     sources = Source.objects.all()
#     context = {
#         'income': income,
#         'values': income,
#         'sources': sources
#     }
#     if request.method == 'GET':
#         return render(request, 'personal_budget/income/edit_income.html',
#                       context)
#
#     if request.method == 'POST':
#         amount = request.POST['amount']
#
#         if not amount:
#             messages.error(request, 'Amount is required')
#             return render(request, 'personal_budget/income/edit_income.html',
#                           context)
#
#         source = request.POST['source']
#         description = request.POST['description']
#         date = request.POST['income_date']
#
#         if not description:
#             messages.error(request, 'Description is required')
#             return render(request, 'personal_budget/income/edit_income.html',
#                           context)
#
#         if not date:
#             messages.error(request, 'Date is required')
#             return render(request, 'personal_budget/income/edit_income.html',
#                           context)
#
#         income.amount = amount
#         income.source = source
#         income.description = description
#         income.date = date
#
#         income.save()
#         messages.success(request, 'Record updated successfully')
#
#         return redirect('income')
#
#
# def delete_income(request, id):
#     income = Income.objects.get(pk=id)
#     income.delete()
#     messages.success(request, 'Record removed')
#     return redirect('income')
#
#
# def search_income(request):
#     if request.method == 'POST':
#         search_str = json.loads(request.body).get('searchText')
#         income = Income.objects.filter(
#             amount__istartswith=search_str,
#             owner=request.user) | Income.objects.filter(
#             source__icontains=search_str,
#             owner=request.user) | Income.objects.filter(
#             description__icontains=search_str,
#             owner=request.user) | Income.objects.filter(
#             date__istartswith=search_str, owner=request.user)
#         data = income.values()
#         return JsonResponse(list(data), safe=False)
#
#
# # _____________________________________________________________________________#
# # EXPENSES CHART
#
# def expense_category_summary(request):
#     todays_date = datetime.date.today()
#     six_months_ago = todays_date - datetime.timedelta(days=30 * 6)
#     expenses = Expense.objects.filter(owner=request.user,
#                                       date__gte=six_months_ago,
#                                       date__lte=todays_date)
#     finalrep = {}
#
#     def get_category(expense):
#         return expense.category
#
#     category_list = list(set(map(get_category, expenses)))
#
#     def get_expense_category_amount(category):
#         amount = 0
#         filtered_by_category = expenses.filter(category=category)
#
#         for item in filtered_by_category:
#             amount += item.amount
#         return amount
#
#     for x in expenses:
#         for y in category_list:
#             finalrep[y] = get_expense_category_amount(y)
#
#     return JsonResponse({'expense_category_data': finalrep}, safe=False)
#
#
# def expenses_stats_view(request):
#     return render(request, 'personal_budget/expenses/expenses_summary.html')
#
#
# def export_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=Expenses' + \
#                                       str(datetime.datetime.now()) + '.csv'
#
#     writer = csv.writer(response)
#     writer.writerow(['Item', 'Category', 'Description', 'Amount', 'Date'])
#
#     expenses = Expense.objects.filter(owner=request.user)
#
#     for expense in expenses:
#         writer.writerow([expense.item, expense.category, expense.description,
#                          expense.amount, expense.date])
#
#     return response
#
#
# def export_excel(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename=Expenses' + \
#                                       str(datetime.datetime.now()) + '.xls'
#
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Expenses')
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#
#     columns = ['Item', 'Category', 'Description', 'Amount', 'Date']
#
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)
#
#     font_style.font.bold = xlwt.XFStyle()
#
#     rows = Expense.objects.filter(owner=request.user).values_list(
#         'item', 'category', 'description', 'amount', 'date')
#
#     for row in rows:
#         row_num += 1
#
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, str(row[col_num]), font_style)
#
#     wb.save(response)
#
#     return response
#
#
# def export_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; attachment; filename=Expenses' + \
#                                       str(datetime.datetime.now()) + '.pdf'
#
#     pdf = canvas.Canvas(response, pagesize=A4)
#     pdf.setTitle('PDF Report')
#
#
#     # styleSheet = getSampleStyleSheet()
#     # style = styleSheet["BodyText"]
#     # P = Paragraph('This is an example', style)
#
#     headers = ['item', 'category', 'description', 'amount', 'date']
#     data = [headers]
#
#     expenses = Expense.objects.filter(owner=request.user)
#
#     sum = expenses.aggregate(Sum('amount'))
#
#     for expense in expenses:
#         data.append([expense.item, expense.category, expense.description,
#                      expense.amount, expense.date])
#
#     table = Table(data)
#     table.setStyle(TableStyle(
#         [('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#          ('GRID', (0, 0), (-1, -1), 1, colors.black),
#          ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#          ('ALIGN', (1, 1), (-1,-1), 'CENTER'),
#          ('FONTSIZE', (0, 0), (-1, 0), 14),
#          ('TEXTFONT', (0, 0), (-1, 0), 'Times-Bold'),
#          ('RIGHTPADDING', (0, 0), (-1, 0), 50),
#          ('TOPPADDING', (0, 0), (-1, 0), 10)]
#     ))
#
#     # canvas.drawString(10, 150, "Basic data")
#
#
#     canvas_width = 600
#     canvas_height = 600
#
#     table.wrapOn(pdf, canvas_width, canvas_height)
#     table.drawOn(pdf, 45, canvas_height - len(data))
#
#     pdf.save()
#     return response
#
#
#
#     # response = HttpResponse(content_type='application/pdf')
#     # response['Content-Disposition'] = 'attachment; filename=Expenses' + \
#     #                                   str(datetime.datetime.now()) + '.pdf'
#     #
#     # response['Content-Transfer-Encoding'] = 'binary'
#     #
#     # html_string = render_to_string('personal_budget/expenses/pdf_output.html',
#     #                                {'expenses': [], 'total': 0})
#     # html = HTML(string=html_string)
#     #
#     # result = html.write_pdf()
#     #
#     # with tempfile.NamedTemporaryFile(delete=True) as output:
#     #     output.write(result)
#     #     output.flush()
#     #     output = open(output.name, 'rb')
#     #     response.write(output.read())
#     #
#     # return response
