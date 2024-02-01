from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_budget_view, name='personal-budget'),
]