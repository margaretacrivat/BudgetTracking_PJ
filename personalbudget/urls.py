from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.personal_budget_home, name='personal-budget'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete-expense'),
    path('search-expenses/', csrf_exempt(views.search_expenses),
         name='search-expenses'),

    path('export-expenses-csv/', views.export_expenses_csv, name='export-expenses-csv'),
    path('export-expenses-excel/', views.export_expenses_excel, name='export-expenses-excel'),
    path('export-expenses-pdf/', views.export_expenses_pdf, name='export-expenses-pdf'),

    path('expenses-category-chart/', views.expenses_category_chart,
         name='expenses-category-chart'),
    path('expenses-for-period/', views.get_expenses_for_period,
         name='expenses-for-period'),
    path('last_3months_expense_source_stats/',
         views.last_3months_expense_source_stats,
         name="last_3months_expense_source_stats"),

    path('income/', views.income_view, name='income'),
    path('add-income/', views.add_income, name='add-income'),
    path('edit-income/<int:id>/', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>/', views.delete_income,
         name='delete-income'),
    path('search-income/', csrf_exempt(views.search_income),
         name='search-income'),

    path('export-income-csv/', views.export_income_csv, name='export-income-csv'),
    path('export-income-excel/', views.export_income_excel, name='export-income-excel'),
    path('export-income-pdf/', views.export_income_pdf, name='export-income-pdf'),

    path('income-source-chart/', views.income_source_chart,
         name='income-source-chart'),
    path('income-for-period/', views.get_income_for_period,
         name='income-for-period'),
    path('last_3months_income_source_stats/',
         views.last_3months_income_source_stats,
         name='last_3months_income_source_stats'),

    path('summary-budget/', views.summary_budget_view, name='summary-budget'),
    path('current_month_balance_stats/', views.current_month_balance_stats, name='current_month_balance_stats'),
    path('current_year_balance_stats/', views.current_year_balance_stats, name='current_year_balance_stats'),
    path('expenses-summary-rest/', views.expenses_summary_rest, name='expenses-summary-rest'),
    path('expenses-summary/', views.expenses_summary_view, name='expenses-summary'),
    path('income-summary-rest/', views.income_summary_rest, name='income-summary-rest'),
    path('income-summary/', views.income_summary_view, name='income-summary'),
]


