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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from personalbudget import views

urlpatterns = [
    # Path to access the admin panel
    path('admin/', admin.site.urls),

    # Path to render the urls apps
    path('', include('budget.urls')),
    path('personalbudget/', include('personalbudget.urls')),
    path('projectbudget/', include('projectbudget.urls')),
    path('preferences/', include('preferences.urls')),
    path('authentication/', include('authentication.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
