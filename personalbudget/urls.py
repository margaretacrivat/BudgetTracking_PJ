from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import (personal_budget_home,
                    preferences_view, add_expense, expenses_view, edit_expense, delete_expense,
                    search_expenses, income_view, add_income, edit_income,
                    delete_income, search_income, export_csv, export_excel, export_pdf,
                    expense_category_summary, expenses_stats_view)

urlpatterns = [
    path('', views.personal_budget_home, name='personal-budget'),
    path('preferences/', views.preferences_view, name='preferences'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('edit-expense/<int:id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>', views.delete_expense, name='delete-expense'),
    path('search-expenses', csrf_exempt(views.search_expenses),
         name='search-expenses'),


    path('income/', views.income_view, name='income'),
    path('add-income/', views.add_income, name='add-income'),
    path('edit-income/<int:id>', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>', views.delete_income,
         name='delete-income'),
    path('search-income', csrf_exempt(views.search_income),
         name='search-income'),

    path('export-csv/', views.export_csv, name='export-csv'),
    path('export-excel/', views.export_excel, name='export-excel'),
    path('export-pdf/', views.export_pdf, name='export-pdf'),

    path('expenses-summary', views.expense_category_summary, name='expenses-summary'),
    path('expenses-stats', views.expenses_stats_view, name='expenses-stats'),
]
