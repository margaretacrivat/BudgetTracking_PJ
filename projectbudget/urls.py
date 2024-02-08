from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.project_budget_view, name='project-budget'),

    path('projects/', views.projects_view, name='projects'),
    path('add-project/', views.add_project, name='add-project'),
    path('edit-project/<int:id>/', views.edit_project, name='edit-project'),
    path('delete-project/<int:id>/', views.delete_project, name='delete-project'),
    path('search-project/', csrf_exempt(views.search_project),
         name='search-project'),


]