from django.contrib import admin
from .models import (Project, ProjectType, ProjectStage,
                     Person, Logistic, AcquisitionType, Displacement,
                     DisplacementType, Workforce, PersonRole)

# Register your models here.


admin.site.register(Project)
admin.site.register(ProjectType)
admin.site.register(ProjectStage)
admin.site.register(Person)
admin.site.register(Logistic)
admin.site.register(AcquisitionType)
admin.site.register(Displacement)
admin.site.register(DisplacementType)
admin.site.register(Workforce)
admin.site.register(PersonRole)