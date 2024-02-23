from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.project_budget_view, name='projects-budget'),
    path('expenses-centralizer/', views.expenses_centralizer_view, name='expenses-centralizer'),
    path('post-calcul-analysis/', views.post_calcul_analysis_view, name='post-calcul-analysis'),

    path('projects/', views.projects_view, name='projects'),
    path('add-projects/', views.add_project, name='add-projects'),
    path('edit-projects/<int:id>/', views.edit_project, name='edit-projects'),
    path('delete-projects/<int:id>/', views.delete_project, name='delete-projects'),

    path('export-projects-csv/', views.export_projects_csv, name='export-projects-csv'),
    path('export-projects-excel/', views.export_projects_excel, name='export-projects-excel'),
    path('export-projects-pdf/', views.export_projects_pdf, name='export-projects-pdf'),

    path('projects-stages/', views.project_stages_view, name='projects-stages'),
    path('add-projects-stage/', views.add_project_stage, name='add-projects-stage'),
    path('edit-projects-stage/<int:id>/', views.edit_project_stage, name='edit-projects-stage'),
    path('delete-projects-stage/<int:id>/', views.delete_project_stage, name='delete-projects-stage'),

    path('export-projects-stages-csv/', views.export_project_stages_csv, name='export-projects-stages-csv'),
    path('export-projects-stages-excel/', views.export_project_stages_excel, name='export-projects-stages-excel'),
    path('export-projects-stages-pdf/', views.export_project_stages_pdf, name='export-projects-stages-pdf'),

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

    path('workforce/', views.workforce_view, name='workforce'),
    path('add-workforce/', views.add_workforce, name='add-workforce'),
    path('edit-workforce/<int:id>/', views.edit_workforce, name='edit-workforce'),
    path('delete-workforce/<int:id>/', views.delete_workforce, name='delete-workforce'),

    path('export-workforce-csv/', views.export_workforce_csv, name='export-workforce-csv'),
    path('export-workforce-excel/', views.export_workforce_excel, name='export-workforce-excel'),
    path('export-workforce-pdf/', views.export_workforce_pdf, name='export-workforce-pdf'),

    path('persons/', views.persons_view, name='persons'),
    path('add-person/', views.add_person, name='add-person'),
    path('edit-person/<int:id>/', views.edit_person, name='edit-person'),
    path('delete-person/<int:id>/', views.delete_person, name='delete-person'),

    path('export-persons-csv/', views.export_persons_csv, name='export-persons-csv'),
    path('export-persons-excel/', views.export_persons_excel, name='export-persons-excel'),
    path('export-persons-pdf/', views.export_persons_pdf, name='export-persons-pdf'),

]
