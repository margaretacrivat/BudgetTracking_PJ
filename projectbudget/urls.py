from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.project_budget_view, name='project-budget'),

    path('projects/', views.projects_view, name='projects'),
    path('add-project/', views.add_project, name='add-project'),
    path('edit-project/<int:id>/', views.edit_project, name='edit-project'),
    path('delete-project/<int:id>/', views.delete_project, name='delete-project'),

    path('export-projects-csv/', views.export_projects_csv, name='export-projects-csv'),
    path('export-projects-excel/', views.export_projects_excel, name='export-projects-excel'),
    path('export-projects-pdf/', views.export_projects_pdf, name='export-projects-pdf'),

    path('project-stages/', views.project_stages_view, name='project-stages'),
    path('add-project-stage/', views.add_project_stage, name='add-project-stage'),
    path('edit-project-stage/<int:id>/', views.edit_project_stage, name='edit-project-stage'),
    path('delete-project-stage/<int:id>/', views.delete_project_stage, name='delete-project-stage'),

    path('export-project-stages-csv/', views.export_project_stages_csv, name='export-project-stages-csv'),
    path('export-project-stages-excel/', views.export_project_stages_excel, name='export-project-stages-excel'),
    path('export-project-stages-pdf/', views.export_project_stages_pdf, name='export-project-stages-pdf'),

    path('logistic/', views.logistic_view, name='logistic'),
    path('add-acquisition/', views.add_acquisition, name='add-acquisition'),
    path('edit-acquisition/<int:id>/', views.edit_acquisition, name='edit-acquisition'),
    path('delete-acquisition/<int:id>/', views.delete_acquisition, name='delete-acquisition'),

    path('export-acquisitions-csv/', views.export_acquisitions_csv, name='export-acquisitions-csv'),
    path('export-acquisitions-excel/', views.export_acquisitions_excel, name='export-acquisitions-excel'),
    path('export-acquisitions-pdf/', views.export_acquisitions_pdf, name='export-acquisitions-pdf'),

    path('displacement/', views.displacement_view, name='displacement'),
    path('add-displacement/', views.add_displacement, name='add-displacement'),
    path('edit-displacement/<int:id>/', views.edit_displacement, name='edit-displacement'),
    path('delete-displacement/<int:id>/', views.delete_displacement, name='delete-displacement'),

    path('export-displacements-csv/', views.export_displacements_csv, name='export-displacements-csv'),
    path('export-displacements-excel/', views.export_displacements_excel, name='export-displacements-excel'),
    path('export-displacements-pdf/', views.export_displacements_pdf, name='export-displacements-pdf'),
]
