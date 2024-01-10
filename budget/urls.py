"""
URL configuration for BudgetTracking_PJ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views
from . import views
from .views import home, HomePageView


urlpatterns = [
    path('', home, name='home'),
    path('homepage/', HomePageView.as_view(), name='homepage'),

    # path('tb_purchase/', views.table_purchase, name='tb-purchase'),
    # path('preferences/', views.preferences_view, name='preferences'),
    # path('expenses/', views.expenses_view, name='expenses'),
    # path('add-expense/', views.add_expense, name='add-expense'),
    # path('edit-expense/<int:id>', views.edit_expense, name='edit-expense'),
    # path('delete-expense/<int:id>', views.delete_expense, name='delete-expense'),
    # path('search-expenses', csrf_exempt(views.search_expenses),
    #      name='search-expenses'),
    #
    #
    # path('income/', views.income_view, name='income'),
    # path('add-income/', views.add_income, name='add-income'),
    # path('edit-income/<int:id>', views.edit_income, name='edit-income'),
    # path('delete-income/<int:id>', views.delete_income,
    #      name='delete-income'),
    # path('search-income', csrf_exempt(views.search_income),
    #      name='search-income'),
    #
    # path('export-csv/', views.export_csv, name='export-csv'),
    # path('export-excel/', views.export_excel, name='export-excel'),
    # path('export-pdf/', views.export_pdf, name='export-pdf'),
    #
    # path('expenses-summary', views.expense_category_summary, name='expenses-summary'),
    # path('expenses-stats', views.expenses_stats_view, name='expenses-stats'),

]


