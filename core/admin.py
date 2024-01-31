from django.contrib import admin
from .models import *

admin.site.register(Storage)
admin.site.register(Service)
admin.site.register(Bed)
admin.site.register(DrugType)
admin.site.register(Drug)
admin.site.register(StoragedDrug)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(LabMaterial)
admin.site.register(StoragedLabMaterial)
admin.site.register(Sample)
admin.site.register(Blood)


# ALL MASTERS AND FUNCTIONALITY MODELS
# ONLY FOR ADMIN USE