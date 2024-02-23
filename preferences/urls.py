from django.urls import path
from . import views

urlpatterns = [
    path('', views.preferences_view, name='preferences'),
    path('settings', views.settings_view, name='settings'),

    path('project-preferences', views.project_preferences_view, name='project-preferences'),
    path('project-settings', views.project_settings_view, name='project-settings'),
]
