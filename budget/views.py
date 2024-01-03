from datatable import dt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import auth
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from rest_framework import serializers
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Items, Expense, Category
from .forms import LoginForm, SignUpForm


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


def user_signup(request):
    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'User was successfully created')
            return redirect('login')

        else:
            messages.error(request, 'Form is not valid')
    else:
        user_form = SignUpForm()
    return render(request, "user/signup.html",
                  {"user_form": user_form})


def user_login(request):
    login_msg = ""
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return redirect('login')
            else:
                condition = 'invalid credentials'
                context = {'condition': condition}
                return render(request, 'user/login.html', context)
    else:
        login_form = LoginForm()
    return render(request, 'user/login.html',
                  {'login_form': login_form, "login_msg": login_msg})


def user_logout(request):
    logout(request)
    return redirect('home')


def table_purchase(request):
    # Logica pentru pagina de inserare a datelor in tabel
    expenses = Expense.objects.all()
    return render(request, 'personal_page/tb_purchase.html', {'expenses': expenses})


@login_required(login_url='/authentication/login')
def expenses_view(request):
    # Logica pentru vizualizarea cheltuielilor
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,  page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj
    }
    return render(request, 'personal_page/expenses.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    # Logica pentru adaugarea cheltuielilor
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'personal_page/add_expense.html', context)

    if request.method == 'POST':
        item = request.POST['item']
        category = request.POST['category']
        cost = request.POST['cost']
        qty = request.POST['qty']
        amount = request.POST['amount']
        date = request.POST['expense_date']

        if not item:
            messages.error(request, 'Item is required')
            return render(request, 'personal_page/add_expense.html', context)
        if not cost:
            messages.error(request, 'Cost is required')
            return render(request, 'personal_page/add_expense.html', context)
        if not qty:
            messages.error(request, 'Quantity is required')
            return render(request, 'personal_page/add_expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_page/add_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_page/add_expense.html', context)

        Expense.objects.create(owner=request.user, item=item, category=category,
                               cost=cost, qty=qty, amount=amount, date=date)

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
        return render(request, 'personal_page/edit_expense.html', context)
    if request.method == 'POST':
        item = request.POST['item']
        category = request.POST['category']
        cost = request.POST['cost']
        qty = request.POST['qty']
        amount = request.POST['amount']
        date = request.POST['expense_date']

        if not item:
            messages.error(request, 'Item is required')
            return render(request, 'personal_page/edit_expense.html', context)
        if not cost:
            messages.error(request, 'Cost is required')
            return render(request, 'personal_page/edit_expense.html', context)
        if not qty:
            messages.error(request, 'Quantity is required')
            return render(request, 'personal_page/edit_expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'personal_page/edit_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'personal_page/edit_expense.html', context)

        expense.owner = request.user
        expense.item = item
        expense.category = category
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


def income_view(request):
    # Logica pentru vizualizarea veniturilor
    return render(request, 'personal_page/income.html')








