from django.urls import path
from . import views

urlpatterns = [
    path('', views.preferences_view, name='preferences'),
    path('settings', views.settings_view, name='settings'),

    path('projects-preferences', views.project_preferences_view, name='projects-preferences'),
    path('projects-settings', views.project_settings_view, name='projects-settings'),
]
