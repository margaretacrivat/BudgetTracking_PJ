from django.urls import path
from . import views

urlpatterns = [
    path('', views.preferences_view, name='preferences'),
    path('account-currency', views.account_currency, name='account-currency'),
]
