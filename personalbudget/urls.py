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


    path('income/', views.income_view, name='income'),
    path('add-income/', views.add_income, name='add-income'),
    path('edit-income/<int:id>/', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>/', views.delete_income,
         name='delete-income'),
    path('search-income/', csrf_exempt(views.search_income),
         name='search-income'),

    path('export-csv/', views.export_csv, name='export-csv'),
    path('export-excel/', views.export_excel, name='export-excel'),
    path('export-pdf/', views.export_pdf, name='export-pdf'),

    path('expenses-category-chart/', views.expenses_category_chart,
         name='expenses-category-chart'),
    path('last_3months_expense_source_stats/',
         views.last_3months_expense_source_stats,
         name="last_3months_expense_source_stats"),
    path('expenses-summary/', views.expenses_summary_view, name='expenses-summary'),
]


