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
from .views import home, SignupCreateView, LoginCreateView

urlpatterns = [
    path('', home, name='homepage'),
    path('signup/', SignupCreateView.as_view(), name='signup'),
    # path('login/', home_login, name='login')
    path('login/', LoginCreateView.as_view(), name='login'),
]


