from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.personal_budget_view, name='personal-budget'),
    path('budget-main/', views.budget_main_view, name='budget-main'),

    path('expenses/', views.expenses_view, name='expenses'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>/', csrf_exempt(views.delete_expense), name='delete-expense'),
    path('search-expenses/', csrf_exempt(views.search_expenses),
         name='search-expenses'),

    path('export-expenses-csv/', views.export_expenses_csv, name='export-expenses-csv'),
    path('export-expenses-excel/', views.export_expenses_excel, name='export-expenses-excel'),
    path('export-expenses-pdf/', views.export_expenses_pdf, name='export-expenses-pdf'),

    path('expenses-category-stats/', views.expenses_category_stats_last_6months,
         name='expenses-category-stats'),
    path('expenses-for-period/', views.get_expenses_for_period,
         name='expenses-for-period'),
    path('expenses-stats/', views.expenses_stats_last_3months,
         name="expenses-stats"),

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

    path('income-source-stats/', views.income_source_stats_last_6months,
         name='income-source-stats'),
    path('income-for-period/', views.get_income_for_period,
         name='income-for-period'),
    path('income-stats/', views.income_stats_last_3months,
         name='income-stats'),

    path('summary-budget/', views.summary_budget_main_view, name='summary-budget'),
    path('current_month_balance_stats/', views.current_month_balance_stats, name='current_month_balance_stats'),
    path('current_year_balance_stats/', views.current_year_balance_stats, name='current_year_balance_stats'),

    path('expenses-summary/', views.expenses_summary_view, name='expenses-summary'),
    path('expenses-summary-rest-stats/', views.expenses_summary_rest_stats, name='expenses-summary-rest-stats'),

    path('income-summary/', views.income_summary_view, name='income-summary'),
    path('income-summary-rest-stats/', views.income_summary_rest_stats, name='income-summary-rest-stats'),
]


